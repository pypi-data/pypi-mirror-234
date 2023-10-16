from enum import IntEnum


class ServiceType(IntEnum):
    LIGHT = 0x43
    CURTAIN = 0x8C
    LOCK = 0x45
    SWITCH = 0x49
    OCCUPANCY_SENSOR = 0x86
    STATELESS_PROGRAMMABLE_SWITCH = 0x89
    BATTERY_SERVICE = 0x96
    FAN = 0xB7
    THERMOSTAT = 0x4A
    DOOR = 0x81
    CONTACT_SENSOR = 0x80
    POWER_METER = 0x8B
    CARD_SWITCH = 0x50
    MOTION_SENSOR = 0x65
    DESK = 0x66


class AttrType(IntEnum):
    ONOFF = 0x0100
    BRIGHTNESS = 0x0121
    COLOR_TEMPERATURE = 0x01F1
    HSV = 0x0123
    LIGHT_MODE = 0x01F2
    LIGHT_TYPE = 0x01F0
    STATELESS_PROGRAMMABLE_SWITCH = 0x0B00
    OCCUPANCY_DETECT = 0x0401
    BATTERY_LEVEL = 0x0104
    STATUS_LOW_BATTERY = 0x0105
    LOCK_OPEN = 0x0146
    LOCK_ALARM = 0x0147
    POSITION_TARGET = 0x0130
    POSITION_CURRENT = 0x0131
    POSITION_CONTROL = 0x0132
    RANGE_CONFIG = 0x0137
    CONTACT_SENSOR_STATE = 0x0115

    TEMPERATURE_DISPLAYUNITS = 0x010F
    CURRENT_TEMPERATURE = 0x010D
    TARGET_TEMPERATURE = 0x010E
    THERMOSTAT_CURRENT_WORK_MODE = 0x0801
    THERMOSTAT_TARGET_WORK_MODE = 0x0802
    THERMOSTAT_CURRENT_FAN_SPEED = 0x0111
    THERMOSTAT_TARGET_FAN_SPEED = 0x010A

    CARD_INSERT_STATUS = 0x0702

    MOTION_STATUS = 0x0401
    CONTACT_STATUS = 0x0409

    HEIGHT = 0x0139


AttrTypeFormat = {
    AttrType.ONOFF: "onoff",
    AttrType.BRIGHTNESS: "brightness",
    AttrType.COLOR_TEMPERATURE: "color temperature",
    AttrType.HSV: "hsv",
    AttrType.LIGHT_MODE: "light mode",
    AttrType.LIGHT_TYPE: "light type",
    AttrType.STATELESS_PROGRAMMABLE_SWITCH: "stateless programmable switch",
    AttrType.OCCUPANCY_DETECT: "occupancy detect",
    AttrType.BATTERY_LEVEL: "battery level",
    AttrType.STATUS_LOW_BATTERY: "status low battery",
    AttrType.LOCK_OPEN: "lock open",
    AttrType.LOCK_ALARM: "lock alarm",
    AttrType.POSITION_TARGET: "position target",
    AttrType.POSITION_CURRENT: "position current",
    AttrType.POSITION_CONTROL: "position control",
    AttrType.RANGE_CONFIG: "range config",
    AttrType.CONTACT_SENSOR_STATE: "contact sensor state",
    AttrType.TEMPERATURE_DISPLAYUNITS: "temperature displayunits",
    AttrType.CURRENT_TEMPERATURE: "current temperature",
    AttrType.TARGET_TEMPERATURE: "target temperature",
    AttrType.THERMOSTAT_CURRENT_WORK_MODE: "thermostat current work mode",
    AttrType.THERMOSTAT_TARGET_WORK_MODE: "thermostat target work mode",
    AttrType.THERMOSTAT_CURRENT_FAN_SPEED: "thermostat current fan speed",
    AttrType.THERMOSTAT_TARGET_FAN_SPEED: "thermostat target fan speed",
    AttrType.CARD_INSERT_STATUS: "card insert status",
    AttrType.MOTION_STATUS: "motion status",
    AttrType.HEIGHT: "Height"
}
