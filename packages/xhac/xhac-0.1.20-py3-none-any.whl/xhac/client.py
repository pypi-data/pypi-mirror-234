# Author: Snow Yang
# E-mail: yangsw@mxchip.com
# Since: 2023-07-31
# Version: 1.0
# Description: This file contains the HTTPClient class.
# This file is part of the xHAC project.
# License: MIT License

# Python built-in modules
import sys
import json
import socket
import asyncio
import hashlib
from functools import partial
from threading import Thread, Semaphore

# Third-party modules
import srp
import hkdf
from chacha20poly1305 import ChaCha20Poly1305

# Private modules
from .pyparser import HttpParser
from .model import *

from enum import IntEnum


class HACException(IOError):
    """Base class for HAC related exceptions."""


class HACTimeoutException(HACException):
    """Timeouts give an exception"""


class HACNetworkException(HACException):
    """Network exception"""

    def __init__(self, message):
        super().__init__(message)


class HTTPClient:
    def __init__(self):
        self._is_secure = False
        self._connected = False
        self._connect_sem = Semaphore(0)
        self._disconnect_sem = Semaphore(0)
        self._response_sem = None

        self.on_disconnect = lambda client: None
        self.on_event = lambda event: None

        self._loop = asyncio.new_event_loop()
        Thread(target=self._loop_thread, daemon=True).start()

    def _loop_thread(self):
        self._loop.run_forever()

    def connect(self, host, port, username, password):
        self._loop.call_soon_threadsafe(
            partial(
                self._connect,
                host=host,
                port=port,
                username=username,
                password=password,
            )
        )
        self._connect_sem.acquire()
        if not self._connected:
            raise HACNetworkException("Connect failed")

    def _connect(self, host, port, username, password):
        if self._connected:
            self._connect_sem.release()
            return

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # Linux specific: after 10 idle seconds, start sending keepalives every 2 seconds.
            # Drop connection after 10 failed keepalives
            self._socket.setsockopt(
                socket.IPPROTO_TCP,
                socket.TCP_KEEPALIVE
                if sys.platform == "darwin"
                else socket.TCP_KEEPIDLE,
                10,
            )
            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
            self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10)

            usr = srp.User(username, password, hash_alg=srp.SHA256, ng_type=srp.NG_1024)
            _, A = usr.start_authentication()

            self._socket.settimeout(5)
            self._socket.connect((host, port))

            self._post("/srp", None)
            body = self._recv_response()
            body = json.loads(body)
            s, B = bytes.fromhex(body["salt"]), bytes.fromhex(body["B"])

            M = usr.process_challenge(s, B)
            self._post("/srp", json.dumps({"A": A.hex(), "proof": M.hex()}))
            body = self._recv_response()
            body = json.loads(body)
            proof = bytes.fromhex(body["proof"])
            usr.verify_session(proof)

            sk = usr.get_session_key()

            kdf = hkdf.Hkdf(b"Control-Salt", sk, hash=hashlib.sha512)
            C2S_Key = kdf.expand(b"Control-Write-Encryption-Key", 32)
            self._send_cipher = ChaCha20Poly1305(C2S_Key)
            S2C_Key = kdf.expand(b"Control-Read-Encryption-Key", 32)
            self._recv_cipher = ChaCha20Poly1305(S2C_Key)

            self._send_seq = 0
            self._recv_seq = 0

            self._is_secure = True

            self._socket.setblocking(False)

            self._recv_task = self._loop.create_task(self._run_recv_task())

            self._connected = True
        except:
            self._is_secure = False
            self._socket.close()
        finally:
            self._connect_sem.release()

    def disconnect(self):
        self._loop.call_soon_threadsafe(self._disconnect)
        self._disconnect_sem.acquire()

    def _disconnect(self):
        self._loop.create_task(self._disconnect_task())

    async def _disconnect_task(self):
        if self._connected:
            self._socket.close()
            self._recv_task.cancel()
            await self._recv_task
            self._connected = False
            self._is_secure = False
        self._disconnect_sem.release()

    def _post(self, path, body):
        self._send(
            (
                f"POST {path} HTTP/1.1\r\n"
                f"Content-Type: application/hap+json\r\n"
                f"Content-Length: {len(body) if body else 0}\r\n"
                f"\r\n"
                f'{body if body else ""}'
            )
        )

    def _get(self, path, params=None):
        if params:
            path += "?"
            for key, value in params.items():
                path += f"{key}={value}&"
            path = path[:-1]
        self._response_sem = Semaphore(0)
        self._loop.call_soon_threadsafe(self._send, f"GET {path} HTTP/1.1\r\n\r\n")
        if not self._response_sem.acquire(timeout=10):
            raise HACNetworkException("Get timeout")
        return self._response_body

    def _put(self, path, body):
        self._response_sem = Semaphore(0)
        self._loop.call_soon_threadsafe(
            self._send,
            (
                f"PUT {path} HTTP/1.1\r\n"
                f"Content-Type: application/hap+json\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"\r\n"
                f"{body}"
            ),
        )
        if not self._response_sem.acquire(timeout=5):
            raise HACNetworkException("Put timeout")
        return self._response_body

    def _send(self, data):
        if self._is_secure:
            nonce = b"\x00" * 4 + self._send_seq.to_bytes(8, "little")
            add = len(data).to_bytes(2, "little")
            self._socket.send(
                len(data).to_bytes(2, "little")
                + self._send_cipher.encrypt(nonce, data.encode("utf-8"), add)
            )
            self._send_seq += 1
        else:
            self._socket.send(data.encode("utf-8"))

    def _recv_response(self):
        body = b""
        p = HttpParser()
        while True:
            data = self._socket.recv(1024)
            p.execute(data, len(data))
            if p.is_partial_body():
                body += p.recv_body()
            if p.is_message_complete():
                return body.decode("utf-8")

    async def _recv(self, total_len):
        data = b""
        recved_len = 0
        while True:
            recved_data = await self._loop.sock_recv(
                self._socket, total_len - recved_len
            )
            data += recved_data
            recved_len += len(recved_data)
            if recved_len == total_len:
                return data

    async def _run_recv_task(self):
        body = b""
        p = HttpParser()
        try:
            while True:
                len = int.from_bytes(await self._recv(2), "little")
                msg = await self._recv(len + 16)

                nonce = b"\x00" * 4 + self._recv_seq.to_bytes(8, "little")
                add = len.to_bytes(2, "little")
                data = self._recv_cipher.decrypt(nonce, msg, add)

                self._recv_seq += 1

                p.execute(data, len)
                if p.is_partial_body():
                    body += p.recv_body()

                if p.is_message_complete():
                    if p.protocol == "HTTP":
                        self._response_body = body.decode("utf-8")
                        self._response_sem.release()
                    else:
                        self._loop.run_in_executor(
                            None,
                            partial(
                                self.on_event,
                                client=self,
                                event=json.loads(body.decode("utf-8")),
                            ),
                        )
                    body = b""
                    p = HttpParser()
        except:
            pass
        finally:
            self._socket.close()
            self._connected = False
            self._is_secure = False
            if self._response_sem:
                self._response_sem.release()
            self._loop.run_in_executor(None, self.on_disconnect, self)


class Device:
    def __init__(self, did, mac, name, zone):
        self.did = did
        self.mac = mac
        self.name = name
        self.zone = zone


class HomeClient(HTTPClient):
    def __init__(self, host, port, username, password):
        super().__init__()
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._home_db = None
        self._ver = 0
        self.on_event = self._on_event
        self.on_home_change = lambda client: None

        self.entities = []
        self.scenes = []

    def _on_event(self, client, event):
        if "home" in event:
            self.sync()
            self.on_home_change(self)
        elif "attributes" in event:
            self._on_attrs(event["attributes"])
        elif "devices" in event:
            devices = event["devices"]
            for device in devices:
                did, reachable = device["did"], device["reachable"]
                for entity in self.entities:
                    if entity.did == did:
                        entity.reachable = reachable
                        entity.on_reachable_change(entity, reachable)

    def _find_entity(self, did, sid):
        for entity in self.entities:
            if entity.did == did and entity.sid == sid:
                return entity
        return None

    def _find_scene(self, sid):
        for scene in self.scenes:
            if scene.sid == sid:
                return scene
        return None

    def _find_zone(self, zid):
        for zone in self._home_db["zones"]:
            if zone["zid"] == zid:
                return zone["name"]
        return "null"

    def connect(self):
        super().connect(self._host, self._port, self._username, self._password)
        self.sync()

    def sync(self):
        self._home_db = json.loads(self._get("/home"))
        self._ver += 1
        for device in self._home_db["devices"]:
            for service in device["services"]:
                did, sid, reachable, zone = (
                    device["did"],
                    service["sid"],
                    device["reachable"],
                    self._find_zone(device["zid"]),
                )

                entity = self._find_entity(did, sid)
                if entity:
                    entity.ver = self._ver
                    entity.reachable = reachable
                    entity.zone = zone
                else:
                    service_type = service["type"]
                    args = (
                        self,
                        service_type,
                        Device(did, device["mac"], device["name"], zone),
                        sid,
                        self._ver,
                        service["attributes"],
                        reachable,
                    )
                    self.entities.append(service_class_map[service_type](*args))

        for entity in self.entities:
            if entity.ver != self._ver:
                self.entities.remove(entity)

        for scene in self._home_db["scenes"]:
            sid = scene["sid"]
            _scene = self._find_scene(sid)
            if _scene:
                _scene.ver = self._ver
            else:
                self.scenes.append(Scene(self, scene["name"], sid, self._ver))

        for scene in self.scenes:
            if scene.ver != self._ver:
                self.scenes.remove(scene)

    def set_scene(self, sid):
        return self._put("/scenes", json.dumps({"scenes": [{"sid": sid}]}))

    def set_attr(self, did, sid, _type, value):
        return self._put(
            "/attributes",
            json.dumps(
                {
                    "attributes": [
                        {"did": did, "sid": sid, "type": _type, "value": value}
                    ]
                }
            ),
        )

    def _on_attrs(self, attrs):
        for entity in self.entities:
            entity.changed_attrs = {}

        for attr in attrs:
            did, sid, _type, value = (
                attr["did"],
                attr["sid"],
                attr["type"],
                attr["value"],
            )

            for entity in self.entities:
                if did == entity.did and sid == entity.sid:
                    if _type == AttrType.ONOFF:
                        entity._onoff = value
                    elif _type == AttrType.BRIGHTNESS:
                        entity._brightness = value
                    elif _type == AttrType.COLOR_TEMPERATURE:
                        entity._color_temperature = value
                    elif _type == AttrType.HSV:
                        entity._hsv = (
                            value["hue"],
                            value["saturation"],
                            value["brightness"],
                        )
                    elif (
                        _type == AttrType.CURRENT_TEMPERATURE
                        or _type == AttrType.TARGET_TEMPERATURE
                    ):
                        entity._temperature = value
                    elif (
                        _type == AttrType.THERMOSTAT_CURRENT_WORK_MODE
                        or _type == AttrType.THERMOSTAT_TARGET_WORK_MODE
                    ):
                        entity._work_mode = value
                    elif (
                        _type == AttrType.THERMOSTAT_CURRENT_FAN_SPEED
                        or _type == AttrType.THERMOSTAT_TARGET_FAN_SPEED
                    ):
                        entity._fan_speed = value
                    elif _type == AttrType.CARD_INSERT_STATUS:
                        entity._card_insert_status = value
                    elif (
                        _type == AttrType.MOTION_STATUS
                        or _type == AttrType.CONTACT_STATUS
                        or _type == AttrType.OCCUPANCY_DETECT
                    ):
                        entity._status = value
                    elif _type == AttrType.POSITION_TARGET:
                        entity._target_position = value
                    elif _type == AttrType.POSITION_CURRENT:
                        entity._current_position = value
                    elif _type == AttrType.HEIGHT:
                        entity._height = value
                    else:
                        continue
                    entity.changed_attrs[_type] = value

        for entity in self.entities:
            if entity.changed_attrs:
                entity.on_state_change(entity, entity.changed_attrs)


class Scene:
    def __init__(self, client, name, sid, ver):
        self._client = client
        self.name = name
        self.sid = sid
        self.ver = ver

    def set(self):
        self._client.set_scene(self.sid)


class Entity:
    def __init__(self, _type, client, device, sid, ver, reachable):
        self.type = _type
        self._client = client
        self.name = device.name
        self.did = device.did
        self.mac = device.mac
        self.zone = device.zone
        self.sid = sid
        self.ver = ver
        self.reachable = reachable

        self.changed_attrs = set()
        self.on_state_change = lambda entity, attrs: None
        self.on_reachable_change = lambda entity, reachable: None


class Light(Entity):
    class Mode(IntEnum):
        COLOR_TEMPERATURE = 0x00
        HSV = 0x01

    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self.supported_modes = []

        self._onoff = 0
        self._brightness = 0
        self._color_temperature = 0
        self._hsv = (0, 0, 0)

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.COLOR_TEMPERATURE:
                self._color_temperature = value
                self.supported_modes.append(Light.Mode.COLOR_TEMPERATURE)
            elif _type == AttrType.HSV:
                self._hsv = (value["hue"], value["saturation"], value["brightness"])
                self.supported_modes.append(Light.Mode.HSV)
            elif _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.BRIGHTNESS:
                self._brightness = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.BRIGHTNESS, value)

    @property
    def color_temperature(self):
        return self._color_temperature

    @color_temperature.setter
    def color_temperature(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.COLOR_TEMPERATURE, value)

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, value):
        self._client.set_attr(
            self.did,
            self.sid,
            AttrType.HSV,
            {"hue": value[0], "saturation": value[1], "brightness": value[2]},
        )

    def toggle(self):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, 2)


class Switch(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._onoff = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, value)

    def toggle(self):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, 2)


class Thermostat(Entity):
    class WorkMode(IntEnum):
        OFF = 0x00
        COOL = 0x01
        HEAT = 0x02
        FAN = 0x03
        AUTO = 0x04
        DRY = 0x05

    class FanSpeed(IntEnum):
        LOW = 0x00
        MIDDLE = 0x01
        HIGH = 0x02
        OFF = 0x03
        AUTO = 0x04

    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._onoff = 0
        self._temperature = 0
        self._work_mode = 0
        self._fan_speed = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.TARGET_TEMPERATURE:
                self._temperature = value
            elif _type == AttrType.THERMOSTAT_TARGET_WORK_MODE:
                self._work_mode = value
            elif _type == AttrType.THERMOSTAT_TARGET_FAN_SPEED:
                self._fan_speed = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.TARGET_TEMPERATURE, value)

    @property
    def work_mode(self):
        return self._work_mode

    @work_mode.setter
    def work_mode(self, value):
        self._client.set_attr(
            self.did, self.sid, AttrType.THERMOSTAT_TARGET_WORK_MODE, value
        )

    @property
    def fan_speed(self):
        return self._fan_speed

    @fan_speed.setter
    def fan_speed(self, value):
        self._client.set_attr(
            self.did, self.sid, AttrType.THERMOSTAT_TARGET_FAN_SPEED, value
        )


class CardSwitch(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._onoff = 0
        self._card_insert_status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.ONOFF:
                self._onoff = value
            elif _type == AttrType.CARD_INSERT_STATUS:
                self._card_insert_status = value

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.ONOFF, value)

    @property
    def card_insert_status(self):
        return self._card_insert_status


class MotionSensor(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.MOTION_STATUS:
                self._status = value

    @property
    def status(self):
        return self._status


class Curtain(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._current_position = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.POSITION_CURRENT:
                self._current_position = value

    @property
    def position(self):
        return self._current_position

    @position.setter
    def position(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.POSITION_TARGET, value)


class Door(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._target_position = 0
        self._current_position = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.POSITION_CURRENT:
                self._current_position = value
            elif _type == AttrType.POSITION_TARGET:
                self._target_position = value

    @property
    def position(self):
        return self._target_position

    @position.setter
    def position(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.POSITION_TARGET, value)


class Desk(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._height = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.HEIGHT:
                self._height = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._client.set_attr(self.did, self.sid, AttrType.HEIGHT, value)


class ContactSensor(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.CONTACT_STATUS:
                self._status = value

    @property
    def status(self):
        return self._status


class OccupancySensor(Entity):
    def __init__(self, client, service_type, device, sid, ver, attrs, reachable):
        super().__init__(service_type, client, device, sid, ver, reachable)

        self._status = 0

        for attr in attrs:
            _type = attr["type"]
            value = attr["value"] if "value" in attr else None
            if _type == AttrType.OCCUPANCY_DETECT:
                self._status = value

    @property
    def status(self):
        return self._status


service_class_map = {
    ServiceType.LIGHT: Light,
    ServiceType.SWITCH: Switch,
    ServiceType.THERMOSTAT: Thermostat,
    ServiceType.CARD_SWITCH: CardSwitch,
    ServiceType.MOTION_SENSOR: MotionSensor,
    ServiceType.CURTAIN: Curtain,
    ServiceType.DOOR: Door,
    ServiceType.DESK: Desk,
    ServiceType.CONTACT_SENSOR: ContactSensor,
    ServiceType.OCCUPANCY_SENSOR: OccupancySensor,
}
