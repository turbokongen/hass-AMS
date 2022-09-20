""" Test module for manual input of int package from debug messages
    Only to be used in debug console of pyCharm."""
import logging
import pprint
import sys
from homeassistant.core import HomeAssistant
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams.parsers import kaifa
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN

METERTYPE = kaifa # Input parser to use
SWEDISH = True
PACKAGE = [126, 160, 155, 1, 0, 1, 16, 86, 27, 230, 231, 0, 15, 64, 0, 0, 0, 9, 12, 7, 230, 9, 18, 7, 14, 56, 15, 255, 128, 0, 0, 2, 18, 9, 7, 75, 70, 77, 95, 48, 48, 49, 9, 16, 55, 51, 52, 48, 49, 53, 55, 48, 49, 49, 50, 55, 52, 53, 51, 50, 9, 8, 77, 65, 51, 48, 52, 72, 52, 68, 6, 0, 0, 6, 54, 6, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0, 0, 1, 208, 6, 0, 0, 2, 212, 6, 0, 0, 16, 217, 6, 0, 0, 9, 187, 6, 0, 0, 8, 235, 6, 0, 0, 9, 2, 6, 0, 0, 8, 251, 9, 12, 7, 230, 9, 18, 7, 14, 56, 15, 255, 128, 0, 0, 6, 8, 166, 101, 185, 6, 0, 0, 0, 0, 6, 2, 217, 43, 105, 6, 0, 34, 14, 106, 197, 201, 126]
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
meter_data, _ = METERTYPE.parse_data(sensor_data, PACKAGE, SWEDISH)
print("Checking for missing attributes")
print(type(meter_data))
Config = {
    "serial_port": "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB"
                   "-Serial_Controller-if00-port0",
    "meter_manufacturer": "auto",
    "parity": "N",
    "baudrate": 2400
}
hub = AmsHub(HomeAssistant, Config)
hass = HomeAssistant
hass.data = {}
hass.data[DOMAIN] = hub
AmsHub._check_for_new_sensors_and_update(hub, meter_data)
pprint.pprint(meter_data)
