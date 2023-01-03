import sys
from custom_components.ams import AmsHub
from .common_test_data import TestData

sys.path.append('../')


def test_find_parser_kamstrup():
    pkg = TestData.KAMSTRUP
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kamstrup"

def test_find_parser_aidon_short():
    pkg = TestData.AIDON_SHORT
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "aidon"

def test_find_parser_aidon_se_3ph():
    pkg = TestData.AIDON_SE_3PH
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "aidon_se"

def test_find_parser_kaifa_long():
    # Kaifa MA304H4D Swedish
    pkg = TestData.KAIFA_MA304H4D_LONG
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa"

def test_find_parser_kaifa_hourly():
    pkg = TestData.KAIFA_HOURLY
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa"

def test_find_parser_kaifa_se():
    pkg = TestData.KAIFA_MA304H4_SE
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa_se"

def test_find_no_parser():
    pkg = [1, 2, 3, 4, 5]
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == None