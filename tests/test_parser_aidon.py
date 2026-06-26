import sys
from custom_components.ams.parsers import aidon
from .common_test_data import TestData
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)

sys.path.append('../')


def test_aidon_hourly():

    parser = aidon
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"

    pkg = TestData.AIDON_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1769
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 947
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 4.6
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 0.3
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 3.2
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 244.5
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 245.7
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 244.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 94064.59
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['device_class'] == SensorDeviceClass.ENERGY
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['device_class'] == SensorDeviceClass.ENERGY
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 7.51
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 9770.64
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',  'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_type'] == "6534 3-phase Meter with CB and Neutral Current Measurement", "Missing attribute"
        assert a['meter_serial'] == "7359992895913195", "Missing attribute"
        assert a['meter_date_time'] == "2020-7-21-21-00-00-00", "Missing attribute"


def test_aidon_short():

    parser = aidon
    pkg = TestData.AIDON_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 6942
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 630
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 19.3
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 2.3
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 8.1
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
#    assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 234.3
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 238.3
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 235.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
#    assert a['device_class'] == SensorDeviceClass.VOLTAGE

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"


def test_aidon_mini():

    parser = aidon
    pkg = TestData.AIDON_MINI
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"
    meter_data, _ = parser.parse_data({}, pkg)
    # Test for parsed values
    assert meter_data == {}
    fixture_aidon_stored = {
        'ams_active_power_import': {
            'state': 734,
            'attributes': {
                'meter_manufacturer': 'AIDON_V0001',
                'meter_type': '6534 3-phase Meter with CB and Neutral Current Measurement',
                'obis_code': '1.0.1.7.0.255',
                'meter_serial': '7359992921288181',
                'unit_of_measurement': 'W',
                'icon': 'mdi:gauge'
            }
        }
    }
    meter_data, _ = parser.parse_data(fixture_aidon_stored, pkg)
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 734
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
#    assert a['device_class'] == SensorDeviceClass.POWER


def test_aidon_invalid_packet_size():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on incorrect pkg range size"


def test_aidon_invalid_read_packet_size():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_WRONG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on mismatch between read and decoded pkg size"


def test_aidon_invalid_frame_flag():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect frame flag"


def test_aidon_invalid_data_flag():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect data flag"


def test_aidon_invalid_frame_crc():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on frame crc"


def test_aidon_invalid_header_crc():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_TRUE), "Data validity test failed on header crc"


def test_aidon_with_oss_brikken():

    parser = aidon
    pkg = TestData.AIDON_OSS_10SEC
    assert parser.test_valid_data(pkg, oss=TestData.OSS_TRUE), "Data validity test failed on data from OSS brikken"


def test_aidon_with_oss_brikken_hourly():

    parser = aidon
    pkg = TestData.AIDON_OSS_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_TRUE), "Data validity test failed on data from OSS brikken"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 2526, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"
