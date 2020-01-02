""" Const """

import serial

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

VERSION = "0.0.1"
AUTHOR = "turbokongen"
ISSUE_URL = "https://github.com/turbokongen/hass-AMS/issue"

DOMAIN = "ams"
DOMAIN_DATA = f"{DOMAIN}_data"
AMS_DEVICES = set()
NEW_DEVICES = set()
SIGNAL_UPDATE_AMS = "update"
SIGNAL_NEW_AMS_SENSOR = "ams_new_sensor"


CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_PARITY = "parity"
CONF_TIMEOUT = "timeout"
CONF_SLEEP = "sleep"

DEFAULT_NAME = "AMS Sensor"
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 2400
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0
DEFAULT_SLEEP = 0.2

FRAME_FLAG = b"\x7e"
DATA_FLAG = b"\xe6\xe7\x00\x0f"
DATA_FLAG_LIST = [230, 231, 0, 15]

LIST_TYPE_SHORT_1PH = 17
LIST_TYPE_LONG_1PH = 27
LIST_TYPE_SHORT_3PH = 25
LIST_TYPE_LONG_3PH = 35

WEEKDAY_MAPPING = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}


# Should we get any comports using pyserial and make a list of possible options..
DOMAIN_SCH = {
    vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT): str,
    vol.Optional(CONF_PARITY, default=DEFAULT_PARITY): str,
    vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): cv.positive_int,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.small_float,
    vol.Optional(CONF_SLEEP, default=DEFAULT_SLEEP): cv.small_float,
    vol.Optional("mode", default="aio"): vol.In(["aio", "thread", "original"]),
}


PLATTFORM_SCH = {}

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
""".format(name=DOMAIN, version=VERSION, issueurl=ISSUE_URL)
