""" Test module for manual input of int package from debug messages
    Only to be used in debug console of pyCharm."""
import logging
import pprint
import sys
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams.parsers import kaifa
from custom_components.ams.parsers import kaifa_se
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
METERTYPE=kaifa
PACKAGE = [126, 160, 39, 1, 2, 1, 16, 90, 135, 230, 231, 0, 15, 64, 0, 0, 0, 9, 12, 7, 229, 10, 22, 5, 11, 29, 24, 255, 128, 0, 0, 2, 1, 6, 0, 0, 8, 67, 228, 124, 126]
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
parser = AmsHub._find_parser(PKG)
print("Running test_valid_data..................")
meter_validData = METERTYPE.test_valid_data(PACKAGE)
if meter_validData:
    print("Valid data test passed")
print("Running parse_data.......................")
meter_data = METERTYPE.parse_data(sensor_data, PACKAGE)
pprint.pprint(meter_data)

