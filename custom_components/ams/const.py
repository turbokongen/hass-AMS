""" Constants for hass-AMS package"""
import serial

HAN_OBIS_CODE = "obis_code"
HAN_PACKET_SIZE = "packet_size"
HAN_METER_MANUFACTURER = "meter_manufacturer"
HAN_METER_LIST_TYPE = "list_type"
HAN_LIST_VER_ID = "obis_list_version"
HAN_METER_SERIAL = "meter_serial"
HAN_METER_TYPE = "meter_type"
HAN_METER_DATETIME = "meter_date_time"
HAN_OBIS_DATETIME = "obis_timedate"
HAN_METER_DAYOFWEEK = "meter_day_of_week"
HAN_ACTIVE_POWER_IMPORT = "ams_active_power_import"
HAN_ACTIVE_POWER_EXPORT = "ams_active_power_export"
HAN_REACTIVE_POWER_IMPORT = "ams_reactive_power_import"
HAN_REACTIVE_POWER_EXPORT = "ams_reactive_power_export"
HAN_ACTIVE_POWER_IMPORT_L1 = "ams_active_power_import_l1"
HAN_ACTIVE_POWER_EXPORT_L1 = "ams_active_power_export_l1"
HAN_REACTIVE_POWER_IMPORT_L1 = "ams_reactive_power_import_l1"
HAN_REACTIVE_POWER_EXPORT_L1 = "ams_reactive_power_export_l1"
HAN_ACTIVE_POWER_IMPORT_L2 = "ams_active_power_import_l2"
HAN_ACTIVE_POWER_EXPORT_L2 = "ams_active_power_export_l2"
HAN_REACTIVE_POWER_IMPORT_L2 = "ams_reactive_power_import_l2"
HAN_REACTIVE_POWER_EXPORT_L2 = "ams_reactive_power_export_l2"
HAN_ACTIVE_POWER_IMPORT_L3 = "ams_active_power_import_l3"
HAN_ACTIVE_POWER_EXPORT_L3 = "ams_active_power_export_l3"
HAN_REACTIVE_POWER_IMPORT_L3 = "ams_reactive_power_import_l3"
HAN_REACTIVE_POWER_EXPORT_L3 = "ams_reactive_power_export_l3"
HAN_CURRENT_L1 = "ams_current_l1"
HAN_CURRENT_L2 = "ams_current_l2"
HAN_CURRENT_L3 = "ams_current_l3"
HAN_VOLTAGE_L1 = "ams_voltage_l1"
HAN_VOLTAGE_L2 = "ams_voltage_l2"
HAN_VOLTAGE_L3 = "ams_voltage_l3"
HAN_ACTIVE_ENERGY_IMPORT = "ams_active_energy_import"
HAN_ACTIVE_ENERGY_EXPORT = "ams_active_energy_export"
HAN_REACTIVE_ENERGY_IMPORT = "ams_reactive_energy_import"
HAN_REACTIVE_ENERGY_EXPORT = "ams_reactive_energy_export"

SENSOR_ICON = "icon"
SENSOR_UOM = "unit_of_measurement"
SENSOR_ATTR = "attributes"
SENSOR_STATE = "state"

AMS_NEW_SENSORS = "ams_new_sensors"
AMS_SENSORS = "ams_sensors"
# Devices that we have read from the serial connection.
AMS_DEVICES = set()
AMS_SENSOR_CREATED_BUT_NOT_READ = set()

CONF_BAUDRATE = "baudrate"
CONF_METER_MANUFACTURER = HAN_METER_MANUFACTURER
CONF_PARITY = "parity"
CONF_SERIAL_PORT = "serial_port"


DOMAIN = "ams"

DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 2400
DEFAULT_METER_MANUFACTURER = "auto"
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0.1

DATA_FLAG = [230, 231, 0, 15]
FRAME_FLAG = b"\x7e"
AIDON_METER_SEQ = [65, 73, 68, 79, 78, 95]
AIDON_SE_METER_SEQ = [126, 162, 67]
KAIFA_METER_SEQ = [75, 102, 109, 95]
KAMSTRUP_METER_SEQ = [75, 97, 109, 115, 116, 114, 117, 112, 95]
LIST_TYPE_1PH_SE = 15
LIST_TYPE_3PH_SE = 27
LIST_TYPE_MINI = 1
LIST_TYPE_SHORT_1PH = 9
LIST_TYPE_LONG_1PH = 14
LIST_TYPE_SHORT_3PH = 13
LIST_TYPE_LONG_3PH = 18
LIST_TYPE_SHORT_3PH_3W = 12
LIST_TYPE_LONG_3PH_3W = 17


METER_TYPE = {
    # Aidon
    6484: "RF2-system module Integrated HAN",  # Sweden
    6510: "6510 1-phase Meter",
    6511: "6511 1-phase Meter with CB",
    6515: "6515 1-phase Meter with CB and Earth Fault Current Measurement",
    6520: "6520 3-phase Meter 3 Wire",
    6521: "6521 2-phase Meter 3 Wire with CB",
    6525: (
        "6525 3-phase Meter 3 Wire with CB and Earth Fault Current "
        "Measurement"
    ),
    6530: "6530 3-phase Meter 4 Wire",
    6531: "6531 3-phase Meter 4 Wire with CB",
    6534: "6534 3-phase Meter with CB and Neutral Current Measurement",
    6540: "6540 3-phase CT Meter 3 Wire",
    6550: "6550 3-phase CT Meter 4 Wire",
    6560: "6560 3-phase CT/VT meter 3 Wire",
    # Kaifa
    "MA105H2E": "Domestic 1 Phase 230V/400V meter",
    "MA304H3E": "Domestic/Industrial 3 Phase 230V 3-Wire meter",
    "MA304H4": "Domestic/Industrial 3 Phase 400V 4-Wire meter",
    "MA304T4": "Industrial 3 Phase 230V 3-Wire meter",
    "MA304T3": "Industrial 3 Phase 400V 4-Wire meter",
    # Kamstrup
    6861111: "Omnipower 1 Phase Direct meter",
    6841121: "Omnipower 3 Phase 3-Wire Direct meter",
    6841131: "Omnipower 3 Phase 4-Wire Direct meter",
    6851121: "Omnipower 3 Phase CT 3-Wire Direct meter",
    6851131: "Omnipower 3 Phase CT 4-Wire Direct meter",
}

HOURLY_SENSORS = [
    HAN_ACTIVE_ENERGY_IMPORT,
    HAN_ACTIVE_ENERGY_EXPORT,
    HAN_REACTIVE_ENERGY_IMPORT,
    HAN_REACTIVE_ENERGY_EXPORT,
]

ALL_SENSORS = [
    HAN_REACTIVE_POWER_EXPORT,
    HAN_VOLTAGE_L3,
    HAN_ACTIVE_POWER_EXPORT,
    HAN_VOLTAGE_L2,
    HAN_REACTIVE_POWER_IMPORT,
    HAN_CURRENT_L1,
    HAN_VOLTAGE_L1,
    HAN_CURRENT_L2,
    HAN_ACTIVE_POWER_IMPORT,
    HAN_CURRENT_L3,
] + HOURLY_SENSORS

MANUFACTURER_OPTIONS = ["auto", "aidon", "aidon_se", "kaifa", "kamstrup"]

SIGNAL_UPDATE_AMS = "ams_update"
SIGNAL_NEW_AMS_SENSOR = "ams_new_sensor"

WEEKDAY_MAPPING = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}

SENSOR_OBIS_MAP = {
    HAN_ACTIVE_POWER_IMPORT: [[1, 0, 1, 7, 0, 255], [1, 1, 1, 7, 0, 255]],
    HAN_ACTIVE_POWER_EXPORT: [[1, 0, 2, 7, 0, 255], [1, 1, 2, 7, 0, 255]],
    HAN_REACTIVE_POWER_IMPORT: [[1, 0, 3, 7, 0, 255], [1, 1, 3, 7, 0, 255]],
    HAN_REACTIVE_POWER_EXPORT: [[1, 0, 4, 7, 0, 255], [1, 1, 4, 7, 0, 255]],
    HAN_ACTIVE_POWER_IMPORT_L1: [1, 0, 21, 7, 0, 255],
    HAN_ACTIVE_POWER_EXPORT_L1: [1, 0, 22, 7, 0, 255],
    HAN_REACTIVE_POWER_IMPORT_L1: [1, 0, 23, 7, 0, 255],
    HAN_REACTIVE_POWER_EXPORT_L1: [1, 0, 24, 7, 0, 255],
    HAN_ACTIVE_POWER_IMPORT_L2: [1, 0, 41, 7, 0, 255],
    HAN_ACTIVE_POWER_EXPORT_L2: [1, 0, 42, 7, 0, 255],
    HAN_REACTIVE_POWER_IMPORT_L2: [1, 0, 43, 7, 0, 255],
    HAN_REACTIVE_POWER_EXPORT_L2: [1, 0, 44, 7, 0, 255],
    HAN_ACTIVE_POWER_IMPORT_L3: [1, 0, 61, 7, 0, 255],
    HAN_ACTIVE_POWER_EXPORT_L3: [1, 0, 62, 7, 0, 255],
    HAN_REACTIVE_POWER_IMPORT_L3: [1, 0, 63, 7, 0, 255],
    HAN_REACTIVE_POWER_EXPORT_L3: [1, 0, 64, 7, 0, 255],
    HAN_CURRENT_L1: [[1, 0, 31, 7, 0, 255], [1, 1, 31, 7, 0, 255]],
    HAN_CURRENT_L2: [[1, 0, 51, 7, 0, 255], [1, 1, 51, 7, 0, 255]],
    HAN_CURRENT_L3: [[1, 0, 71, 7, 0, 255], [1, 1, 71, 7, 0, 255]],
    HAN_VOLTAGE_L1: [[1, 0, 32, 7, 0, 255], [1, 1, 32, 7, 0, 255]],
    HAN_VOLTAGE_L2: [[1, 0, 52, 7, 0, 255], [1, 1, 52, 7, 0, 255]],
    HAN_VOLTAGE_L3: [[1, 0, 72, 7, 0, 255], [1, 1, 72, 7, 0, 255]],
    HAN_ACTIVE_ENERGY_IMPORT: [[1, 0, 1, 8, 0, 255], [1, 1, 1, 8, 0, 255]],
    HAN_ACTIVE_ENERGY_EXPORT: [[1, 0, 2, 8, 0, 255], [1, 1, 2, 8, 0, 255]],
    HAN_REACTIVE_ENERGY_IMPORT: [[1, 0, 3, 8, 0, 255], [1, 1, 3, 8, 0, 255]],
    HAN_REACTIVE_ENERGY_EXPORT: [[1, 0, 4, 8, 0, 255], [1, 1, 4, 8, 0, 255]],
}
SENSOR_COMMON_OBIS_MAP = {
    HAN_LIST_VER_ID: [1, 1, 0, 2, 129, 255],
    HAN_METER_SERIAL: [[0, 0, 96, 1, 0, 255], [1, 1, 0, 0, 5, 255]],
    HAN_METER_TYPE: [[0, 0, 96, 1, 7, 255], [1, 1, 96, 1, 1, 255]],
    HAN_METER_DATETIME: [[0, 0, 1, 0, 0, 255], [0, 1, 1, 0, 0, 255]],
}

SENSOR_SCALER = {
    HAN_ACTIVE_POWER_IMPORT: 1,
    HAN_ACTIVE_POWER_EXPORT: 1,
    HAN_REACTIVE_POWER_IMPORT: 1,
    HAN_REACTIVE_POWER_EXPORT: 1,
    HAN_ACTIVE_POWER_IMPORT_L1: 1,
    HAN_ACTIVE_POWER_EXPORT_L1: 1,
    HAN_REACTIVE_POWER_IMPORT_L1: 1,
    HAN_REACTIVE_POWER_EXPORT_L1: 1,
    HAN_ACTIVE_POWER_IMPORT_L2: 1,
    HAN_ACTIVE_POWER_EXPORT_L2: 1,
    HAN_REACTIVE_POWER_IMPORT_L2: 1,
    HAN_REACTIVE_POWER_EXPORT_L2: 1,
    HAN_ACTIVE_POWER_IMPORT_L3: 1,
    HAN_ACTIVE_POWER_EXPORT_L3: 1,
    HAN_REACTIVE_POWER_IMPORT_L3: 1,
    HAN_REACTIVE_POWER_EXPORT_L3: 1,
    HAN_CURRENT_L1: 10,
    HAN_CURRENT_L2: 10,
    HAN_CURRENT_L3: 10,
    HAN_VOLTAGE_L1: 10,
    HAN_VOLTAGE_L2: 10,
    HAN_VOLTAGE_L3: 10,
    HAN_ACTIVE_ENERGY_IMPORT: 1000,
    HAN_ACTIVE_ENERGY_EXPORT: 1000,
    HAN_REACTIVE_ENERGY_IMPORT: 1000,
    HAN_REACTIVE_ENERGY_EXPORT: 1000,
}

SENSOR_UNIT = {
    HAN_ACTIVE_POWER_IMPORT: "W",
    HAN_ACTIVE_POWER_EXPORT: "W",
    HAN_REACTIVE_POWER_IMPORT: "VAr",
    HAN_REACTIVE_POWER_EXPORT: "VAr",
    HAN_ACTIVE_POWER_IMPORT_L1: "W",
    HAN_ACTIVE_POWER_EXPORT_L1: "W",
    HAN_REACTIVE_POWER_IMPORT_L1: "VAr",
    HAN_REACTIVE_POWER_EXPORT_L1: "VAr",
    HAN_ACTIVE_POWER_IMPORT_L2: "W",
    HAN_ACTIVE_POWER_EXPORT_L2: "W",
    HAN_REACTIVE_POWER_IMPORT_L2: "VAr",
    HAN_REACTIVE_POWER_EXPORT_L2: "VAr",
    HAN_ACTIVE_POWER_IMPORT_L3: "W",
    HAN_ACTIVE_POWER_EXPORT_L3: "W",
    HAN_REACTIVE_POWER_IMPORT_L3: "VAr",
    HAN_REACTIVE_POWER_EXPORT_L3: "VAr",
    HAN_CURRENT_L1: "A",
    HAN_CURRENT_L2: "A",
    HAN_CURRENT_L3: "A",
    HAN_VOLTAGE_L1: "V",
    HAN_VOLTAGE_L2: "V",
    HAN_VOLTAGE_L3: "V",
    HAN_ACTIVE_ENERGY_IMPORT: "kWh",
    HAN_ACTIVE_ENERGY_EXPORT: "kWh",
    HAN_REACTIVE_ENERGY_IMPORT: "kVAr",
    HAN_REACTIVE_ENERGY_EXPORT: "kVAr",
}

SENSOR_ICON_MAP = {
    HAN_ACTIVE_POWER_IMPORT: "gauge",
    HAN_ACTIVE_POWER_EXPORT: "gauge",
    HAN_REACTIVE_POWER_IMPORT: "gauge",
    HAN_REACTIVE_POWER_EXPORT: "gauge",
    HAN_ACTIVE_POWER_IMPORT_L1: "gauge",
    HAN_ACTIVE_POWER_EXPORT_L1: "gauge",
    HAN_REACTIVE_POWER_IMPORT_L1: "gauge",
    HAN_REACTIVE_POWER_EXPORT_L1: "gauge",
    HAN_ACTIVE_POWER_IMPORT_L2: "gauge",
    HAN_ACTIVE_POWER_EXPORT_L2: "gauge",
    HAN_REACTIVE_POWER_IMPORT_L2: "gauge",
    HAN_REACTIVE_POWER_EXPORT_L2: "gauge",
    HAN_ACTIVE_POWER_IMPORT_L3: "gauge",
    HAN_ACTIVE_POWER_EXPORT_L3: "gauge",
    HAN_REACTIVE_POWER_IMPORT_L3: "gauge",
    HAN_REACTIVE_POWER_EXPORT_L3: "gauge",
    HAN_CURRENT_L1: "current-ac",
    HAN_CURRENT_L2: "current-ac",
    HAN_CURRENT_L3: "current-ac",
    HAN_VOLTAGE_L1: "flash",
    HAN_VOLTAGE_L2: "flash",
    HAN_VOLTAGE_L3: "flash",
    HAN_ACTIVE_ENERGY_IMPORT: "gauge",
    HAN_ACTIVE_ENERGY_EXPORT: "gauge",
    HAN_REACTIVE_ENERGY_IMPORT: "gauge",
    HAN_REACTIVE_ENERGY_EXPORT: "gauge",
}
