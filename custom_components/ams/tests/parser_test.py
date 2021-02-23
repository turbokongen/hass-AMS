""" Test module for manual input of int package from debug messages
    Only to be used in debug console of pyCharm."""
import logging
import pprint
import sys
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams.parsers import kaifa
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
METERTYPE=aidon
PACKAGE = [126, 161, 138, 65, 8, 131, 19, 235, 253, 230, 231, 0, 15, 64, 0, 0, 0, 0, 1, 18, 2, 2, 9, 6, 1, 1, 0, 2, 129, 255, 10, 11, 65, 73, 68, 79, 78, 95, 86, 48, 48, 48, 49, 2, 2, 9, 6, 0, 0, 96, 1, 0, 255, 10, 16, 55, 51, 53, 57, 57, 57, 50, 56, 57, 53, 57, 49, 51, 49, 57, 53, 2, 2, 9, 6, 0, 0, 96, 1, 7, 255, 10, 4, 54, 53, 51, 52, 2, 3, 9, 6, 1, 0, 1, 7, 0, 255, 6, 0, 0, 6, 233, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 2, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 3, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 4, 7, 0, 255, 6, 0, 0, 3, 179, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 31, 7, 0, 255, 16, 0, 46, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 51, 7, 0, 255, 16, 0, 3, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 71, 7, 0, 255, 16, 0, 32, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 32, 7, 0, 255, 18, 9, 141, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 52, 7, 0, 255, 18, 9, 153, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 72, 7, 0, 255, 18, 9, 142, 2, 2, 15, 255, 22, 35, 2, 2, 9, 6, 0, 0, 1, 0, 0, 255, 9, 12, 7, 228, 7, 21, 2, 21, 0, 0, 255, 0, 0, 0, 2, 3, 9, 6, 1, 0, 1, 8, 0, 255, 6, 0, 143, 135, 251, 2, 2, 15, 1, 22, 30, 2, 3, 9, 6, 1, 0, 2, 8, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 1, 22, 30, 2, 3, 9, 6, 1, 0, 3, 8, 0, 255, 6, 0, 0, 2, 239, 2, 2, 15, 1, 22, 32, 2, 3, 9, 6, 1, 0, 4, 8, 0, 255, 6, 0, 14, 232, 168, 2, 2, 15, 1, 22, 32, 202, 145, 126]
PKG = []
for item in PACKAGE:
    PKG.append(hex(item)[2:].zfill(2))
PKG_STRING = " "
PKG_STRING = ' '.join(map(str, PKG))
PACKAGE_STRING = " "
PACKAGE_STRING = ' '.join(map(str, PACKAGE))
NUMBERED_PACKAGE = {}
n = range(((PACKAGE[1] & 0x0F) << 8 | PACKAGE[2]) + 2)
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
aidonMeter_validData = METERTYPE.test_valid_data(PACKAGE)
if aidonMeter_validData:
    print("Valid data test passed")
print("Running parse_data.......................")
adionMeter_data = METERTYPE.new_parse_data(sensor_data, PACKAGE)
pprint.pprint(adionMeter_data)

