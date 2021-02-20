""" Constants for hass-AMS package"""

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
