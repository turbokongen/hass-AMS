""" Constants for hass-AMS package"""

import serial

AMS_NEW_SENSORS = "ams_new_sensors"
AMS_SENSORS = "ams_sensors"
AMS_DEVICES = set()
AMS_SENSOR_CREATED_BUT_NOT_READ = set()

CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_PARITY = "parity"
CONF_METER_MANUFACTURER = "meter_manufacturer"

DATA_FLAG = [230, 231, 0, 15]
DOMAIN = "ams"

DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 2400
DEFAULT_METER_MANUFACTURER = "kamstrup"
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0.1

FRAME_FLAG = b"\x7e"

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
