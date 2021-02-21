""" Constants for hass-AMS package"""
from typing import Dict, List
import serial

AIDON_METER_SEQ = [65, 73, 68, 79, 78, 95]
AMS_NEW_SENSORS = "ams_new_sensors"
AMS_SENSORS = "ams_sensors"
# Devices that we have read from the serial connection.
AMS_DEVICES = set()
AMS_SENSOR_CREATED_BUT_NOT_READ = set()

CONF_BAUDRATE = "baudrate"
CONF_METER_MANUFACTURER = "meter_manufacturer"
CONF_PARITY = "parity"
CONF_SERIAL_PORT = "serial_port"

DATA_FLAG = [230, 231, 0, 15]
DOMAIN = "ams"

DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 2400
DEFAULT_METER_MANUFACTURER = "auto"
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0.1

FRAME_FLAG = b"\x7e"
AIDON_SE_3PH_ID = "1b"
AIDON_SE_1PH_ID = "ff"

KAIFA_METER_SEQ = [75, 102, 109, 95]
KAMSTRUP_METER_SEQ = [75, 97, 109, 115, 116, 114, 117, 112, 95]
LIST_TYPE_1PH_SE = 15
LIST_TYPE_3PH_SE = 27
LIST_TYPE_MINI = 1
LIST_TYPE_SHORT_1PH = 9
LIST_TYPE_LONG_1PH = 14
LIST_TYPE_SHORT_3PH = 13
LIST_TYPE_LONG_3PH = 18

HOURLY_SENSORS = [
    "ams_active_energy_import",
    "ams_active_energy_export",
    "ams_reactive_energy_import",
    "ams_reactive_energy_export",
]

ALL_SENSORS = [
    "ams_reactive_power_export",
    "ams_voltage_l3",
    "ams_active_power_export",
    "ams_voltage_l2",
    "ams_reactive_power_import",
    "ams_current_l1",
    "ams_voltage_l1",
    "ams_current_l2",
    "ams_active_power_import",
    "ams_current_l3",
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

HAN_LIST_VER_ID = "obis_list_version"
HAN_METER_SERIAL = "meter_serial"
HAN_METER_TYPE = "meter_type"
HAN_METER_DATETIME = "meter_date_time"
HAN_METER_DAYOFWEEK = "meter_day_of_week"
HAN_ACTIVE_POWER_IMPORT = "active_power_import"
HAN_ACTIVE_POWER_EXPORT = "active_power_export"
HAN_REACTIVE_POWER_IMPORT = "reactive_power_import"
HAN_REACTIVE_POWER_EXPORT = "reactive_power_export"
HAN_ACTIVE_POWER_IMPORT_L1 = "active_power_import_l1"
HAN_ACTIVE_POWER_EXPORT_L1 = "active_power_export_l1"
HAN_REACTIVE_POWER_IMPORT_L1 = "reactive_power_import_l1"
HAN_REACTIVE_POWER_EXPORT_L1 = "reactive_power_export_l1"
HAN_ACTIVE_POWER_IMPORT_L2 = "active_power_import_l2"
HAN_ACTIVE_POWER_EXPORT_L2 = "active_power_export_l2"
HAN_REACTIVE_POWER_IMPORT_L2 = "reactive_power_import_l2"
HAN_REACTIVE_POWER_EXPORT_L2 = "reactive_power_export_l2"
HAN_ACTIVE_POWER_IMPORT_L3 = "active_power_import_l3"
HAN_ACTIVE_POWER_EXPORT_L3 = "active_power_export_l3"
HAN_REACTIVE_POWER_IMPORT_L3 = "reactive_power_import_l3"
HAN_REACTIVE_POWER_EXPORT_L3 = "reactive_power_export_l3"
HAN_CURRENT_L1 = "current_l1"
HAN_CURRENT_L2 = "current_l2"
HAN_CURRENT_L3 = "current_l3"
HAN_VOLTAGE_L1 = "voltage_l1"
HAN_VOLTAGE_L2 = "voltage_l2"
HAN_VOLTAGE_L3 = "voltage_l3"
HAN_ACTIVE_ENERGY_IMPORT = "active_energy_import"
HAN_ACTIVE_ENERGY_EXPORT = "active_energy_export"
HAN_REACTIVE_ENERGY_IMPORT = "reactive_energy_import"
HAN_REACTIVE_ENERGY_EXPORT = "reactive_energy_export"

name_obis_map: Dict[str, List[str]] = {
    HAN_LIST_VER_ID: ["1.1.0.2.129.255"],
    HAN_METER_SERIAL: ["0.0.96.1.0.255", "1.1.0.0.5.255"],
    HAN_METER_TYPE: ["0.0.96.1.7.255", "1.1.96.1.1.255"],
    HAN_ACTIVE_POWER_IMPORT: ["1.0.1.7.0.255", "1.1.1.7.0.255"],
    HAN_ACTIVE_POWER_EXPORT: ["1.0.2.7.0.255", "1.1.2.7.0.255"],
    HAN_REACTIVE_POWER_IMPORT: ["1.0.3.7.0.255", "1.1.3.7.0.255"],
    HAN_REACTIVE_POWER_EXPORT: ["1.0.4.7.0.255", "1.1.4.7.0.255"],
    HAN_ACTIVE_POWER_IMPORT_L1: ["1.0.21.7.0.255"],
    HAN_ACTIVE_POWER_EXPORT_L1: ["1.0.22.7.0.255"],
    HAN_REACTIVE_POWER_IMPORT_L1: ["1.0.23.7.0.255"],
    HAN_REACTIVE_POWER_EXPORT_L1: ["1.0.24.7.0.255"],
    HAN_ACTIVE_POWER_IMPORT_L2: ["1.0.41.7.0.255"],
    HAN_ACTIVE_POWER_EXPORT_L2: ["1.0.42.7.0.255"],
    HAN_REACTIVE_POWER_IMPORT_L2: ["1.0.43.7.0.255"],
    HAN_REACTIVE_POWER_EXPORT_L2: ["1.0.44.7.0.255"],
    HAN_ACTIVE_POWER_IMPORT_L3: ["1.0.61.7.0.255"],
    HAN_ACTIVE_POWER_EXPORT_L3: ["1.0.62.7.0.255"],
    HAN_REACTIVE_POWER_IMPORT_L3: ["1.0.63.7.0.255"],
    HAN_REACTIVE_POWER_EXPORT_L3: ["1.0.64.7.0.255"],
    HAN_CURRENT_L1: ["1.0.31.7.0.255", "1.1.31.7.0.255"],
    HAN_CURRENT_L2: ["1.0.51.7.0.255", "1.1.51.7.0.255"],
    HAN_CURRENT_L3: ["1.0.71.7.0.255", "1.1.71.7.0.255"],
    HAN_VOLTAGE_L1: ["1.0.32.7.0.255", "1.1.32.7.0.255"],
    HAN_VOLTAGE_L2: ["1.0.52.7.0.255", "1.1.52.7.0.255"],
    HAN_VOLTAGE_L3: ["1.0.72.7.0.255", "1.1.72.7.0.255"],
    HAN_METER_DATETIME: ["0.0.1.0.0.255", "0.1.1.0.0.255"],
    HAN_ACTIVE_ENERGY_IMPORT: ["1.0.1.8.0.255", "1.1.1.8.0.255"],
    HAN_ACTIVE_ENERGY_EXPORT: ["1.0.2.8.0.255", "1.1.2.8.0.255"],
    HAN_REACTIVE_ENERGY_IMPORT: ["1.0.3.8.0.255", "1.1.3.8.0.255"],
    HAN_REACTIVE_ENERGY_EXPORT: ["1.0.4.8.0.255", "1.1.4.8.0.255"],
}

obis_name_map: Dict[str, str] = {}
for name, obis_values in name_obis_map.items():
    for obis in obis_values:
        obis_name_map[obis] = name
