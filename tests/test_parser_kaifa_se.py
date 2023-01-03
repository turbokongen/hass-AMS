import sys
from custom_components.ams.parsers import kaifa_se
from .common_test_data import TestData
sys.path.append('../')


def test_kaifa_MA304H4_se():

    parser = kaifa_se
    pkg = None
    assert not parser.test_valid_data(pkg), "Package test for None failed"

    pkg = TestData.KAIFA_MA304H4_SE
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 297, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3', 'ams_active_energy_import',
              'ams_active_energy_export', 'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "KFM_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_se_invalid_packet_size():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect pkg range size"


def test_kaifa_se_invalid_read_packet_size():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_WRONG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on mismatch between read and decoded pkg size"


def test_kaifa_se_invalid_frame_flag():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect frame flag"


def test_kaifa_se_invalid_data_flag():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect data flag"


def test_kaifa_se_invalid_frame_crc():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on frame crc"


def test_kaifa_se_invalid_header_crc():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on header crc"
