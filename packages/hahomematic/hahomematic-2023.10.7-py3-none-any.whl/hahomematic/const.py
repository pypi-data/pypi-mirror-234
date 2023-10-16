"""Constants used by hahomematic."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum, StrEnum
from typing import Final

DEFAULT_CONNECTION_CHECKER_INTERVAL: Final = 15  # check if connection is available via rpc ping
DEFAULT_ENCODING: Final = "UTF-8"
DEFAULT_JSON_SESSION_AGE: Final = 90
DEFAULT_PING_PONG_MISMATCH_COUNT: Final = 10
DEFAULT_RECONNECT_WAIT: Final = 120  # wait with reconnect after a first ping was successful
DEFAULT_TIMEOUT: Final = 60  # default timeout for a connection
DEFAULT_TLS: Final = False
DEFAULT_VERIFY_TLS: Final = False

REGA_SCRIPT_FETCH_ALL_DEVICE_DATA: Final = "fetch_all_device_data.fn"
REGA_SCRIPT_GET_SERIAL: Final = "get_serial.fn"
REGA_SCRIPT_PATH: Final = "../rega_scripts"
REGA_SCRIPT_SET_SYSTEM_VARIABLE: Final = "set_system_variable.fn"
REGA_SCRIPT_SYSTEM_VARIABLES_EXT_MARKER: Final = "get_system_variables_ext_marker.fn"

DEFAULT_DEVICE_DESCRIPTIONS_DIR: Final = "export_device_descriptions"
DEFAULT_PARAMSET_DESCRIPTIONS_DIR: Final = "export_paramset_descriptions"

# Password can be empty.
# Allowed characters: A-Z, a-z, 0-9, .!$():;#-
# The CCU WebUI also supports ÄäÖöÜüß, but these characters are not supported by the XmlRPC servers
CCU_PASSWORD_PATTERN: Final = r"[A-Za-z0-9.!$():;#-]{0,}"

IDENTIFIER_SEPARATOR: Final = "@"
INIT_DATETIME: Final = datetime.strptime("01.01.1970 00:00:00", "%d.%m.%Y %H:%M:%S")
IP_ANY_V4: Final = "0.0.0.0"
PORT_ANY: Final = 0

PATH_JSON_RPC: Final = "/api/homematic.cgi"

HOMEGEAR_SERIAL = "Homegear_SN0815"

PROGRAM_ADDRESS: Final = "program"
SYSVAR_ADDRESS: Final = "sysvar"

CONF_PASSWORD: Final = "password"
CONF_USERNAME: Final = "username"

EVENT_ADDRESS: Final = "address"
EVENT_INSTANCE_NAME: Final = "instance_name"
EVENT_AVAILABLE: Final = "available"
EVENT_CHANNEL_NO: Final = "channel_no"
EVENT_DATA: Final = "data"
EVENT_DEVICE_TYPE: Final = "device_type"
EVENT_INTERFACE_ID: Final = "interface_id"
EVENT_PARAMETER: Final = "parameter"
EVENT_SECONDS_SINCE_LAST_EVENT: Final = "seconds_since_last_event"
EVENT_TYPE: Final = "type"
EVENT_VALUE: Final = "value"

FILE_DEVICES: Final = "homematic_devices.json"
FILE_PARAMSETS: Final = "homematic_paramsets.json"

MAX_CACHE_AGE: Final = 60

NO_CACHE_ENTRY: Final = "NO_CACHE_ENTRY"


class Backend(StrEnum):
    """Enum with supported hahomematic backends."""

    CCU = "CCU"
    HOMEGEAR = "Homegear"
    PYDEVCCU = "PyDevCCU"


class CallBackSource(StrEnum):
    """Enum with sources for registered callbacks."""

    HA: Final = "ha_callback"
    INTERNAL: Final = "hm_initernal"


class CallSource(StrEnum):
    """Enum with sources for calls."""

    HA_INIT: Final = "ha_init"
    HM_INIT: Final = "hm_init"
    MANUAL_OR_SCHEDULED: Final = "manual_or_scheduled"


class DataOperationResult(Enum):
    """Enum with data operation results."""

    LOAD_FAIL: Final = 0
    LOAD_SUCCESS: Final = 1
    SAVE_FAIL: Final = 10
    SAVE_SUCCESS: Final = 11
    NO_LOAD: Final = 20
    NO_SAVE: Final = 21


class Description(StrEnum):
    """Enum with homematic device/paramset description attributes."""

    ADDRESS = "ADDRESS"
    AVAILABLE_FIRMWARE = "AVAILABLE_FIRMWARE"
    CHILDREN = "CHILDREN"
    DEFAULT = "DEFAULT"
    FIRMWARE = "FIRMWARE"
    FIRMWARE_UPDATABLE = "UPDATABLE"
    FIRMWARE_UPDATE_STATE = "FIRMWARE_UPDATE_STATE"
    FLAGS = "FLAGS"
    MAX = "MAX"
    MIN = "MIN"
    NAME = "NAME"
    OPERATIONS = "OPERATIONS"
    PARAMSETS = "PARAMSETS"
    PARENT = "PARENT"
    PARENT_TYPE = "PARENT_TYPE"
    SPECIAL = "SPECIAL"  # Which has the following keys
    SUBTYPE = "SUBTYPE"
    TYPE = "TYPE"
    UNIT = "UNIT"
    VALUE_LIST = "VALUE_LIST"


class DeviceFirmwareState(StrEnum):
    """Enum with homematic device firmware states."""

    UP_TO_DATE: Final = "UP_TO_DATE"
    LIVE_UP_TO_DATE: Final = "LIVE_UP_TO_DATE"
    NEW_FIRMWARE_AVAILABLE: Final = "NEW_FIRMWARE_AVAILABLE"
    LIVE_NEW_FIRMWARE_AVAILABLE: Final = "LIVE_NEW_FIRMWARE_AVAILABLE"
    DELIVER_FIRMWARE_IMAGE: Final = "DELIVER_FIRMWARE_IMAGE"
    LIVE_DELIVER_FIRMWARE_IMAGE: Final = "LIVE_DELIVER_FIRMWARE_IMAGE"
    READY_FOR_UPDATE: Final = "READY_FOR_UPDATE"
    DO_UPDATE_PENDING: Final = "DO_UPDATE_PENDING"
    PERFORMING_UPDATE: Final = "PERFORMING_UPDATE"


class EntityUsage(StrEnum):
    """Enum with information about usage in Home Assistant."""

    CE_PRIMARY: Final = "ce_primary"
    CE_SECONDARY: Final = "ce_secondary"
    CE_VISIBLE: Final = "ce_visible"
    ENTITY: Final = "entity"
    EVENT: Final = "event"
    NO_CREATE: Final = "entity_no_create"


class EventType(StrEnum):
    """Enum with hahomematic event types."""

    DEVICE_AVAILABILITY: Final = "homematic.device_availability"
    DEVICE_ERROR: Final = "homematic.device_error"
    IMPULSE: Final = "homematic.impulse"
    INTERFACE: Final = "homematic.interface"
    KEYPRESS: Final = "homematic.keypress"


class Flag(IntEnum):
    """Enum with homematic flags."""

    VISIBLE = 1
    INTERNAL = 2
    TRANSFORM = 4  # not used
    SERVICE = 8
    STICKY = 10  # This might be wrong. Documentation says 0x10 # not used


class ForcedDeviceAvailability(StrEnum):
    """Enum with hahomematic event types."""

    FORCE_FALSE: Final = "forced_not_available"
    FORCE_TRUE: Final = "forced_available"
    NOT_SET: Final = "not_set"


class Manufacturer(StrEnum):
    """Enum with hahomematic system events."""

    EQ3 = "eQ-3"
    HB = "Homebrew"
    MOEHLENHOFF = "Möhlenhoff"


class Operations(IntEnum):
    """Enum with homematic operations."""

    NONE = 0  # not used
    READ = 1
    WRITE = 2
    EVENT = 4


class Parameter(StrEnum):
    """Enum with homematic params."""

    ACOUSTIC_ALARM_ACTIVE = "ACOUSTIC_ALARM_ACTIVE"
    ACOUSTIC_ALARM_SELECTION = "ACOUSTIC_ALARM_SELECTION"
    ACTIVE_PROFILE = "ACTIVE_PROFILE"
    ACTIVITY_STATE = "ACTIVITY_STATE"
    ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"
    ACTUAL_TEMPERATURE = "ACTUAL_TEMPERATURE"
    AUTO_MODE = "AUTO_MODE"
    BATTERY_STATE = "BATTERY_STATE"
    BOOST_MODE = "BOOST_MODE"
    CHANNEL_OPERATION_MODE = "CHANNEL_OPERATION_MODE"
    COLOR = "COLOR"
    COLOR_BEHAVIOUR = "COLOR_BEHAVIOUR"
    COLOR_TEMPERATURE = "COLOR_TEMPERATURE"
    COMBINED_PARAMETER = "COMBINED_PARAMETER"
    COMFORT_MODE = "COMFORT_MODE"
    CONCENTRATION = "CONCENTRATION"
    CONFIG_PENDING = "CONFIG_PENDING"
    CONTROL_MODE = "CONTROL_MODE"
    CURRENT = "CURRENT"
    CURRENT_ILLUMINATION = "CURRENT_ILLUMINATION"
    DEVICE_OPERATION_MODE = "DEVICE_OPERATION_MODE"
    DIRECTION = "DIRECTION"
    DOOR_COMMAND = "DOOR_COMMAND"
    DOOR_STATE = "DOOR_STATE"
    DURATION_UNIT = "DURATION_UNIT"
    DURATION_VALUE = "DURATION_VALUE"
    DUTYCYCLE = "DUTYCYCLE"
    DUTY_CYCLE = "DUTY_CYCLE"
    EFFECT = "EFFECT"
    ENERGY_COUNTER = "ENERGY_COUNTER"
    ERROR = "ERROR"
    ERROR_JAMMED = "ERROR_JAMMED"
    FREQUENCY = "FREQUENCY"
    HEATING_COOLING = "HEATING_COOLING"
    HUE = "HUE"
    HUMIDITY = "HUMIDITY"
    LED_STATUS = "LED_STATUS"
    LEVEL = "LEVEL"
    LEVEL_2 = "LEVEL_2"
    LEVEL_COMBINED = "LEVEL_COMBINED"
    LEVEL_SLATS = "LEVEL_SLATS"
    LOCK_STATE = "LOCK_STATE"
    LOCK_TARGET_LEVEL = "LOCK_TARGET_LEVEL"
    LOWBAT = "LOWBAT"
    LOWERING_MODE = "LOWERING_MODE"
    LOW_BAT = "LOW_BAT"
    MANU_MODE = "MANU_MODE"
    ON_TIME = "ON_TIME"
    OPEN = "OPEN"
    OPERATING_VOLTAGE = "OPERATING_VOLTAGE"
    OPTICAL_ALARM_ACTIVE = "OPTICAL_ALARM_ACTIVE"
    OPTICAL_ALARM_SELECTION = "OPTICAL_ALARM_SELECTION"
    PARTY_MODE = "PARTY_MODE"
    PONG = "PONG"
    POWER = "POWER"
    PRESS = "PRESS"
    PRESS_CONT = "PRESS_CONT"
    PRESS_LOCK = "PRESS_LOCK"
    PRESS_LONG = "PRESS_LONG"
    PRESS_LONG_RELEASE = "PRESS_LONG_RELEASE"
    PRESS_LONG_START = "PRESS_LONG_START"
    PRESS_SHORT = "PRESS_SHORT"
    PRESS_UNLOCK = "PRESS_UNLOCK"
    PROGRAM = "PROGRAM"
    RAMP_TIME = "RAMP_TIME"
    RAMP_TIME_TO_OFF_UNIT = "RAMP_TIME_TO_OFF_UNIT"
    RAMP_TIME_TO_OFF_VALUE = "RAMP_TIME_TO_OFF_VALUE"
    RAMP_TIME_UNIT = "RAMP_TIME_UNIT"
    RAMP_TIME_VALUE = "RAMP_TIME_VALUE"
    RSSI_DEVICE = "RSSI_DEVICE"
    RSSI_PEER = "RSSI_PEER"
    SABOTAGE = "SABOTAGE"
    SATURATION = "SATURATION"
    SECTION = "SECTION"
    SENSOR = "SENSOR"
    SENSOR_ERROR = "SENSOR_ERROR"
    SEQUENCE_OK = "SEQUENCE_OK"
    SETPOINT = "SETPOINT"
    SET_POINT_MODE = "SET_POINT_MODE"
    SET_POINT_TEMPERATURE = "SET_POINT_TEMPERATURE"
    SET_TEMPERATURE = "SET_TEMPERATURE"
    SMOKE_DETECTOR_ALARM_STATUS = "SMOKE_DETECTOR_ALARM_STATUS"
    SMOKE_DETECTOR_COMMAND = "SMOKE_DETECTOR_COMMAND"
    STATE = "STATE"
    STATUS = "STATUS"
    STICKY_UN_REACH = "STICKY_UNREACH"
    STOP = "STOP"
    TEMPERATURE = "TEMPERATURE"
    TEMPERATURE_MAXIMUM = "TEMPERATURE_MAXIMUM"
    TEMPERATURE_MINIMUM = "TEMPERATURE_MINIMUM"
    UN_REACH = "UNREACH"
    UPDATE_PENDING = "UPDATE_PENDING"
    VALVE_STATE = "VALVE_STATE"
    VOLTAGE = "VOLTAGE"
    WORKING = "WORKING"


class ParamsetKey(StrEnum):
    """Enum with paramset keys."""

    MASTER = "MASTER"
    VALUES = "VALUES"


class HmPlatform(StrEnum):
    """Enum with platforms relevant for Home Assistant."""

    ACTION: Final = "action"
    BINARY_SENSOR: Final = "binary_sensor"
    BUTTON: Final = "button"
    CLIMATE: Final = "climate"
    COVER: Final = "cover"
    EVENT: Final = "event"
    HUB_BINARY_SENSOR: Final = "hub_binary_sensor"
    HUB_BUTTON: Final = "hub_button"
    HUB_NUMBER: Final = "hub_number"
    HUB_SELECT: Final = "hub_select"
    HUB_SENSOR: Final = "hub_sensor"
    HUB_SWITCH: Final = "hub_switch"
    HUB_TEXT: Final = "hub_text"
    LIGHT: Final = "light"
    LOCK: Final = "lock"
    NUMBER: Final = "number"
    SELECT: Final = "select"
    SENSOR: Final = "sensor"
    SIREN: Final = "siren"
    SWITCH: Final = "switch"
    TEXT: Final = "text"
    UPDATE: Final = "update"


class ProductGroup(StrEnum):
    """Enum with homematic product groups."""

    HM: Final = "BidCos-RF"
    HMIP: Final = "HmIP-RF"
    HMIPW: Final = "HmIP-Wired"
    HMW: Final = "BidCos-Wired"
    UNKNOWN: Final = "unknown"
    VIRTUAL: Final = "VirtualDevices"


class InterfaceName(StrEnum):
    """Enum with homematic interface names."""

    BIDCOS_RF = "BidCos-RF"
    BIDCOS_WIRED = "BidCos-Wired"
    HMIP_RF = "HmIP-RF"
    VIRTUAL_DEVICES = "VirtualDevices"


class InterfaceEventType(StrEnum):
    """Enum with hahomematic event types."""

    CALLBACK: Final = "callback"
    PINGPONG: Final = "pingpong"
    PROXY: Final = "proxy"


class ProxyInitState(Enum):
    """Enum with proxy handling results."""

    INIT_FAILED: Final = 0
    INIT_SUCCESS: Final = 1
    DE_INIT_FAILED: Final = 4
    DE_INIT_SUCCESS: Final = 8
    DE_INIT_SKIPPED: Final = 16


class SystemEvent(StrEnum):
    """Enum with hahomematic system events."""

    DELETE_DEVICES = "deleteDevices"
    DEVICES_CREATED = "devicesCreated"
    ERROR = "error"
    HUB_REFRESHED = "hubEntityRefreshed"
    LIST_DEVICES = "listDevices"
    NEW_DEVICES = "newDevices"
    REPLACE_DEVICE = "replaceDevice"
    RE_ADDED_DEVICE = "readdedDevice"
    UPDATE_DEVICE = "updateDevice"


class SysvarType(StrEnum):
    """Enum for homematic sysvar types."""

    ALARM = "ALARM"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    LIST = "LIST"
    LOGIC = "LOGIC"
    NUMBER = "NUMBER"
    STRING = "STRING"


class ParameterType(StrEnum):
    """Enum for homematic parameter types."""

    ACTION = "ACTION"  # Usually buttons, send Boolean to trigger
    BOOL = "BOOL"
    ENUM = "ENUM"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"
    STRING = "STRING"


CLICK_EVENTS: Final[tuple[Parameter, ...]] = (
    Parameter.PRESS,
    Parameter.PRESS_CONT,
    Parameter.PRESS_LOCK,
    Parameter.PRESS_LONG,
    Parameter.PRESS_LONG_RELEASE,
    Parameter.PRESS_LONG_START,
    Parameter.PRESS_SHORT,
    Parameter.PRESS_UNLOCK,
)

DEVICE_ERROR_EVENTS: Final[tuple[Parameter, ...]] = (Parameter.ERROR, Parameter.SENSOR_ERROR)

ENTITY_EVENTS: Final[tuple[EventType, ...]] = (
    EventType.IMPULSE,
    EventType.KEYPRESS,
)

IMPULSE_EVENTS: Final[tuple[Parameter, ...]] = (Parameter.SEQUENCE_OK,)

KEY_CHANNEL_OPERATION_MODE_VISIBILITY: Final[Mapping[str, tuple[str, ...]]] = {
    Parameter.STATE: ("BINARY_BEHAVIOR",),
    Parameter.PRESS_LONG: ("KEY_BEHAVIOR", "SWITCH_BEHAVIOR"),
    Parameter.PRESS_LONG_RELEASE: ("KEY_BEHAVIOR", "SWITCH_BEHAVIOR"),
    Parameter.PRESS_LONG_START: ("KEY_BEHAVIOR", "SWITCH_BEHAVIOR"),
    Parameter.PRESS_SHORT: ("KEY_BEHAVIOR", "SWITCH_BEHAVIOR"),
}


HUB_PLATFORMS: Final[tuple[HmPlatform, ...]] = (
    HmPlatform.HUB_BINARY_SENSOR,
    HmPlatform.HUB_BUTTON,
    HmPlatform.HUB_NUMBER,
    HmPlatform.HUB_SELECT,
    HmPlatform.HUB_SENSOR,
    HmPlatform.HUB_SWITCH,
    HmPlatform.HUB_TEXT,
)

PLATFORMS: Final[tuple[HmPlatform, ...]] = (
    HmPlatform.BINARY_SENSOR,
    HmPlatform.BUTTON,
    HmPlatform.CLIMATE,
    HmPlatform.COVER,
    HmPlatform.EVENT,
    HmPlatform.LIGHT,
    HmPlatform.LOCK,
    HmPlatform.NUMBER,
    HmPlatform.SELECT,
    HmPlatform.SENSOR,
    HmPlatform.SIREN,
    HmPlatform.SWITCH,
    HmPlatform.TEXT,
    HmPlatform.UPDATE,
)

RELEVANT_INIT_PARAMETERS: Final[tuple[Parameter, ...]] = (
    Parameter.CONFIG_PENDING,
    Parameter.STICKY_UN_REACH,
    Parameter.UN_REACH,
)

# virtual remotes device_types
VIRTUAL_REMOTE_TYPES: Final[tuple[str, ...]] = (
    "HM-RCV-50",
    "HMW-RCV-50",
    "HmIP-RCV-50",
)

VIRTUAL_REMOTE_ADDRESSES: Final[tuple[str, ...]] = (
    "BidCoS-RF",
    "HMW-RCV-50",
    "HmIP-RCV-1",
)


@dataclass(slots=True)
class HubData:
    """Dataclass for hub entities."""

    name: str


@dataclass(slots=True)
class ProgramData(HubData):
    """Dataclass for programs."""

    pid: str
    is_active: bool
    is_internal: bool
    last_execute_time: str


@dataclass(slots=True)
class SystemVariableData(HubData):
    """Dataclass for system variables."""

    value: bool | float | int | str | None
    data_type: SysvarType | None = None
    extended_sysvar: bool = False
    max_value: float | int | None = None
    min_value: float | int | None = None
    unit: str | None = None
    values: tuple[str, ...] | None = None


@dataclass(slots=True)
class SystemInformation:
    """System information of the backend."""

    available_interfaces: tuple[str, ...] = field(default_factory=tuple)
    auth_enabled: bool | None = None
    https_redirect_enabled: bool | None = None
    serial: str | None = None
