import sys
from custom_components.ams import AmsHub
from .common_test_data import TestData

sys.path.append('../')


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

    pkg = TestData.AIDON_SE_3PH
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "aidon_se"

    pkg = TestData.KAIFA_MA304H4D_LONG
    parser_detected = AmsHub._find_parser(pkg)
    assert parser_detected == "kaifa"
