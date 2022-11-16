
import pytest
import logging
import pprint
import sys


sys.path.append('../')

from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN


from .common_test_data import TestData

def test_find_parser():
    pkg = TestData.KAMSTRUP
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kamstrup"

    pkg = TestData.KAIFA_MA304H4_SE
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa_se"

    pkg = TestData.AIDON_SHORT
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "aidon"

    pkg = TestData.AIDON_SE_LONG
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "aidon_se"

    pkg = TestData.KAIFA_MA304H4D_LONG
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa"


