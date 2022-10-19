""" Test module for manual input of int package from debug messages
    Only to be used in debug console of pyCharm."""
import logging
import pprint
import sys
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams.parsers import kaifa
from custom_components.ams.parsers import kaifa_se
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN

METERTYPE = aidon_se # Input parser to use
SWEDISH = None
# MA304H4
# PACKAGE = [126, 161, 29, 1, 0, 1, 16, 176, 174, 230, 231, 0, 15, 64, 0, 0, 0, 0, 2, 36, 9, 6, 1, 0, 0, 2, 129, 255, 9, 7, 75, 70, 77, 95, 48, 48, 49, 9, 6, 0, 0, 96, 1, 0, 255, 9, 16, 55, 51, 52, 48, 49, 53, 55, 48, 51, 48, 53, 52, 56, 51, 48, 48, 9, 6, 0, 0, 96, 1, 7, 255, 9, 7, 77, 65, 51, 48, 52, 72, 52, 9, 6, 1, 0, 1, 7, 0, 255, 6, 0, 0, 1, 41, 9, 6, 1, 0, 2, 7, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 3, 7, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 4, 7, 0, 255, 6, 0, 0, 0, 107, 9, 6, 1, 0, 31, 7, 0, 255, 6, 0, 0, 2, 104, 9, 6, 1, 0, 51, 7, 0, 255, 6, 0, 0, 2, 17, 9, 6, 1, 0, 71, 7, 0, 255, 6, 0, 0, 2, 46, 9, 6, 1, 0, 32, 7, 0, 255, 6, 0, 0, 9, 50, 9, 6, 1, 0, 52, 7, 0, 255, 6, 0, 0, 9, 65, 9, 6, 1, 0, 72, 7, 0, 255, 6, 0, 0, 9, 48, 9, 6, 0, 0, 1, 0, 0, 255, 9, 12, 7, 230, 10, 15, 6, 15, 8, 15, 255, 255, 196, 0, 9, 6, 1, 0, 1, 8, 0, 255, 6, 0, 148, 130, 99, 9, 6, 1, 0, 2, 8, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 3, 8, 0, 255, 6, 0, 1, 47, 198, 9, 6, 1, 0, 4, 8, 0, 255, 6, 0, 19, 107, 43, 188, 84, 126]
# MA304H4D
# PACKAGE = [126, 160, 155, 1, 0, 1, 16, 86, 27, 230, 231, 0, 15, 64, 0, 0, 0, 9, 12, 7, 230, 9, 18, 7, 14, 56, 15, 255, 128, 0, 0, 2, 18, 9, 7, 75, 70, 77, 95, 48, 48, 49, 9, 16, 55, 51, 52, 48, 49, 53, 55, 48, 49, 49, 50, 55, 52, 53, 51, 50, 9, 8, 77, 65, 51, 48, 52, 72, 52, 68, 6, 0, 0, 6, 54, 6, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 1, 208, 6, 0, 0, 2, 212, 6, 0, 0, 16, 217, 6, 0, 0, 9, 187, 6, 0, 0, 8, 235, 6, 0, 0, 9, 2, 6, 0, 0, 8, 251, 9, 12, 7, 230, 9, 18, 7, 14, 56, 15, 255, 128, 0, 0, 6, 8, 166, 101, 185, 6, 0, 0, 0, 0, 6, 2, 217, 43, 105, 6, 0, 34, 14, 106, 197, 201, 126]
PACKAGE = [126, 162, 67, 65, 8, 131, 19, 133, 235, 230, 231, 0, 15, 64, 0, 0, 0, 0, 1, 27, 2, 2, 9, 6, 0, 0, 1, 0, 0, 255, 9, 12, 7, 230, 10, 16, 0, 16, 14, 10, 255, 128, 0, 255, 2, 3, 9, 6, 1, 0, 1, 7, 0, 255, 6, 0, 0, 2, 248, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 2, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 3, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 4, 7, 0, 255, 6, 0, 0, 4, 16, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 31, 7, 0, 255, 16, 255, 246, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 51, 7, 0, 255, 16, 0, 23, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 71, 7, 0, 255, 16, 0, 24, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 32, 7, 0, 255, 18, 9, 44, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 52, 7, 0, 255, 18, 9, 57, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 72, 7, 0, 255, 18, 9, 74, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 21, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 22, 7, 0, 255, 6, 0, 0, 0, 39, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 23, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 24, 7, 0, 255, 6, 0, 0, 0, 242, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 41, 7, 0, 255, 6, 0, 0, 1, 123, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 42, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 43, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 44, 7, 0, 255, 6, 0, 0, 1, 132, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 61, 7, 0, 255, 6, 0, 0, 1, 165, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 62, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 63, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 64, 7, 0, 255, 6, 0, 0, 1, 147, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 1, 8, 0, 255, 6, 2, 71, 16, 87, 2, 2, 15, 0, 22, 30, 2, 3, 9, 6, 1, 0, 2, 8, 0, 255, 6, 0, 151, 1, 103, 2, 2, 15, 0, 22, 30, 2, 3, 9, 6, 1, 0, 3, 8, 0, 255, 6, 0, 1, 85, 202, 2, 2, 15, 0, 22, 32, 2, 3, 9, 6, 1, 0, 4, 8, 0, 255, 6, 0, 143, 201, 175, 2, 2, 15, 0, 22, 32, 106, 221, 126]
PKG = []
for item in PACKAGE:
    PKG.append(hex(item)[2:].zfill(2))
PKG_STRING = " "
PKG_STRING = ' '.join(map(str, PKG))
PACKAGE_STRING = " "
PACKAGE_STRING = ' '.join(map(str, PACKAGE))
NUMBERED_PACKAGE = {}
n = range(((PACKAGE[1] & 0x0F) << 8 | PACKAGE[2]) + 2)
print(n)
for i in n:
    NUMBERED_PACKAGE[i] = PACKAGE[i]
NUMBERED_PKG = {}
for i in n:
    NUMBERED_PKG[i] = PACKAGE[i]

print(PACKAGE)
print(PKG)
print(PKG_STRING)
print(PACKAGE_STRING)
print(NUMBERED_PKG)

root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)
sensor_data = {}
print("Testing for parser.......................")
parser = AmsHub._find_parser(PACKAGE)
print("Running test_valid_data..................")
meter_validData = METERTYPE.test_valid_data(PACKAGE)
if meter_validData:
    print("--------------Valid data test passed----------------")
print("Running parse_data.......................")
if SWEDISH:
    meter_data, _ = METERTYPE.parse_data(sensor_data, PACKAGE, SWEDISH)
else:
    meter_data, _ = METERTYPE.parse_data(sensor_data, PACKAGE)
print("Checking for missing attributes")
print(type(meter_data))
config = {
    "protocol": "serial",
    "serial_port": "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB"
                   "-Serial_Controller-if00-port0",
    "meter_manufacturer": "auto",
    "parity": "N",
    "baudrate": 2400
}

hub = AmsHub(HomeAssistant, config)
hass = HomeAssistant
hass.data = {}
hass.data[DOMAIN] = hub
AmsHub._check_for_new_sensors_and_update(hub, meter_data)
pprint.pprint(meter_data)
