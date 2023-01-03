import sys
from custom_components.ams.parsers import aidon_se
from .common_test_data import TestData

sys.path.append('../')


def test_aidon_se():  # Swedish AMS data pushes all sensor at each transmit. Only one type of package is pushed

    parser = aidon_se
    pkg = None
    assert not parser.test_valid_data(pkg), "Package test for None failed"

    pkg = TestData.AIDON_SE_3PH
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 760, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_H0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_aidon_se_invalid_packet_size():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect pkg range size"


def test_aidon_se_invalid_read_packet_size():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_WRONG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on mismatch between read and decoded pkg size"


def test_aidon_se_invalid_frame_flag():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect frame flag"


def test_aidon_se_invalid_data_flag():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect data flag"


def test_aidon_se_invalid_frame_crc():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on frame crc"


def test_aidon_se_invalid_header_crc():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on header crc"
