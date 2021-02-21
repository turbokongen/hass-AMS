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
METERTYPE=aidon_se
PACKAGE = [126, 162, 67, 65, 8, 131, 19, 133, 235, 230, 231, 0, 15, 64, 0, 0, 0, 0, 1, 27, 2, 2, 9, 6, 0, 0, 1, 0, 0, 255, 9, 12, 7, 229, 2, 18, 4, 21, 6, 20, 255, 128, 0, 255, 2, 3, 9, 6, 1, 0, 1, 7, 0, 255, 6, 0, 0, 2, 229, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 2, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 3, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 4, 7, 0, 255, 6, 0, 0, 2, 108, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 31, 7, 0, 255, 16, 0, 11, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 51, 7, 0, 255, 16, 0, 21, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 71, 7, 0, 255, 16, 0, 9, 2, 2, 15, 255, 22, 33, 2, 3, 9, 6, 1, 0, 32, 7, 0, 255, 18, 9, 33, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 52, 7, 0, 255, 18, 9, 22, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 72, 7, 0, 255, 18, 9, 22, 2, 2, 15, 255, 22, 35, 2, 3, 9, 6, 1, 0, 21, 7, 0, 255, 6, 0, 0, 0, 133, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 22, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 23, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 24, 7, 0, 255, 6, 0, 0, 0, 233, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 41, 7, 0, 255, 6, 0, 0, 1, 157, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 42, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 43, 7, 0, 255, 6, 0, 0, 1, 25, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 44, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 61, 7, 0, 255, 6, 0, 0, 0, 191, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 62, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 27, 2, 3, 9, 6, 1, 0, 63, 7, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 64, 7, 0, 255, 6, 0, 0, 0, 110, 2, 2, 15, 0, 22, 29, 2, 3, 9, 6, 1, 0, 1, 8, 0, 255, 6, 1, 80, 16, 31, 2, 2, 15, 0, 22, 30, 2, 3, 9, 6, 1, 0, 2, 8, 0, 255, 6, 0, 0, 0, 0, 2, 2, 15, 0, 22, 30, 2, 3, 9, 6, 1, 0, 3, 8, 0, 255, 6, 0, 107, 237, 54, 2, 2, 15, 0, 22, 32, 2, 3, 9, 6, 1, 0, 4, 8, 0, 255, 6, 0, 32, 48, 18, 2, 2, 15, 0, 22, 32, 109, 58, 126]
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
adionMeter_data = METERTYPE.parse_data(sensor_data, PACKAGE)
pprint.pprint(adionMeter_data)

