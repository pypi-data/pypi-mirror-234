import time

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class HomeServer:
    def __init__(self, name, ip, port, mac, hostname, model, version):
        self.name = name
        self.ip = ip
        self.port = port
        self.mac = mac
        self.hostname = hostname
        self.model = model
        self.version = version


class Listener(ServiceListener):

    def __init__(self, servers) -> None:
        super().__init__()
        self.servers = servers

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        self.servers.append(
            HomeServer(
                info.properties[b'name'].decode(),
                info.parsed_addresses()[0],
                info.port,
                info.properties[b'id'].decode(),
                info.server,
                info.properties[b'md'].decode(),
                info.properties[b'pv'].decode()
            )
        )


class Scanner:

    def __init__(self):
        self.servers = []

    def scan(self):
        zeroconf = Zeroconf()
        listener = Listener(self.servers)
        ServiceBrowser(zeroconf, "_mxchip._tcp.local.", listener)
        time.sleep(1)
        zeroconf.close()
