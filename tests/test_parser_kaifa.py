import sys
from custom_components.ams.parsers import kaifa
from .common_test_data import TestData
sys.path.append('../')


def test_kaifa_MA304H4D_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4D_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)
    assert meter_data['ams_active_power_import']['state'] == 1590, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"


def test_kaifa_MA304H4D_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4D_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1590, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_MA304H4_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)
    assert meter_data['ams_active_power_import']['state'] == 1415, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"


def test_kaifa_MA304H4_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1418, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_MA304H3E_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H3E_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for parsed values
    assert meter_data['ams_active_power_import']['state'] == 549, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"


def test_kaifa_MA304H3E_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H3E_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 546, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_hourly():

    parser = kaifa

    pkg = TestData.KAIFA_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 119, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"
    assert meter_data['ams_active_energy_import']['state'] ==\
           10494.991, "Parsed ams_active_energy_import is not correct"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',  'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_1phase():

    parser = kaifa

    pkg = TestData.KAIFA_1PH_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 932, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_voltage_l1']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_1phase_hourly():

    parser = kaifa
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"
    pkg = TestData.KAIFA_1PH_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1655, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"
    assert meter_data['ams_active_energy_import']['state'] ==\
           25591.693, "Parsed ams_active_energy_import is not correct"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_voltage_l1', 'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_H4PSE():

    parser = kaifa
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"
    pkg = TestData.KAIFA_MA304H4D_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=True)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1590, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"
    assert meter_data['ams_active_energy_import']['state'] ==\
           145122.745, "Parsed ams_active_energy_import is not correct"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_voltage_l1', 'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kfm_001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_kaifa_invalid_packet_size():
    parser = kaifa
    pkg = TestData.KAIFA_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on incorrect pkg range size"


def test_kaifa_invalid_read_packet_size():
    parser = kaifa
    pkg = TestData.KAIFA_WRONG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on mismatch between read and decoded pkg size"


def test_kaifa_invalid_frame_flag():
    parser = kaifa
    pkg = TestData.KAIFA_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect frame flag"


def test_kaifa_invalid_data_flag():

    parser = kaifa
    pkg = TestData.KAIFA_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect data flag"


def test_kaifa_invalid_frame_crc():

    parser = kaifa
    pkg = TestData.KAIFA_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on frame crc"


def test_kaifa_invalid_header_crc():

    parser = kaifa
    pkg = TestData.KAIFA_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on header crc"
