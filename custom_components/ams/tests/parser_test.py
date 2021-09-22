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
METERTYPE=kaifa_se
PACKAGE = [126, 161, 29, 1, 0, 1, 16, 176, 174, 230, 231, 0, 15, 64, 0, 0, 0, 0, 2, 36, 9, 6, 1, 0, 0, 2, 129, 255, 9, 7, 75, 70, 77, 95, 48, 48, 49, 9, 6, 0, 0, 96, 1, 0, 255, 9, 16, 55, 51, 52, 48, 49, 53, 55, 48, 51, 48, 53, 52, 56, 51, 48, 48, 9, 6, 0, 0, 96, 1, 7, 255, 9, 7, 77, 65, 51, 48, 52, 72, 52, 9, 6, 1, 0, 1, 7, 0, 255, 6, 0, 0, 6, 242, 9, 6, 1, 0, 2, 7, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 3, 7, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 4, 7, 0, 255, 6, 0, 0, 0, 81, 9, 6, 1, 0, 31, 7, 0, 255, 6, 0, 0, 16, 190, 9, 6, 1, 0, 51, 7, 0, 255, 6, 0, 0, 3, 73, 9, 6, 1, 0, 71, 7, 0, 255, 6, 0, 0, 13, 111, 9, 6, 1, 0, 32, 7, 0, 255, 6, 0, 0, 9, 15, 9, 6, 1, 0, 52, 7, 0, 255, 6, 0, 0, 8, 234, 9, 6, 1, 0, 72, 7, 0, 255, 6, 0, 0, 8, 234, 9, 6, 0, 0, 1, 0, 0, 255, 9, 12, 7, 229, 9, 22, 3, 17, 31, 15, 255, 255, 196, 0, 9, 6, 1, 0, 1, 8, 0, 255, 6, 0, 73, 10, 147, 9, 6, 1, 0, 2, 8, 0, 255, 6, 0, 0, 0, 0, 9, 6, 1, 0, 3, 8, 0, 255, 6, 0, 0, 102, 116, 9, 6, 1, 0, 4, 8, 0, 255, 6, 0, 8, 211, 219, 37, 236, 126]
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
parser = AmsHub._find_parser(AmsHub, PKG)
print("Running test_valid_data..................")
meter_validData = METERTYPE.test_valid_data(PACKAGE)
if meter_validData:
    print("Valid data test passed")
print("Running parse_data.......................")
meter_data = METERTYPE.parse_data(sensor_data, PACKAGE)
pprint.pprint(meter_data)

