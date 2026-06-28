import sys
from custom_components.ams.parsers import kamstrup
from .common_test_data import TestData
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)
sys.path.append('../')


def test_kamstrup():

    parser = kamstrup
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"

    pkg = TestData.KAMSTRUP
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1202
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 32
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 223
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 1.42
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 4.15
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 0.73
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 236
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 237
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 240
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert 'unit_of_measurement' in a, "Missing attribute"
        assert a['meter_manufacturer'] == "Kamstrup_V0001", "Missing attribute"
        assert a['meter_type'] == 'Omnipower 3 Phase Direct meter'
        assert a['meter_serial'] == '5706567275940841'


def test_kamstrup_hourly():

    parser = kamstrup
    pkg = TestData.KAMSTRUP_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on hourly"
    meter_data, _ = parser.parse_data({}, pkg)

    # pprint.pprint(meter_data)
    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 2690
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 218
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 2.84
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 8.96
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 10.21
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 238
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 239
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 240
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 155232.51
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 3242.89
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 7243.62
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    #assert a['state_class'] == SensorStateClass.MEASUREMENT
    #assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1',
              'ams_voltage_l2', 'ams_voltage_l3',  'ams_active_energy_import', 'ams_reactive_energy_import',
              'ams_active_energy_export', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert k in meter_data, "Key missing in parsed data"
        assert 'unit_of_measurement' in a, "Missing attribute"
        assert a['meter_manufacturer'] == "Kamstrup_V0001", "Missing attribute"
        assert a['meter_type'] == 'Omnipower 3 Phase 3-Wire Direct meter'
        assert a['meter_serial'] == '5706567271589419'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-11-26-15-00-00-05", "Missing attribute"

def test_kamstrup_invalid_packet_size():
    parser = kamstrup
    pkg = TestData.KAMSTRUP_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on incorrect pkg range size"


def test_kamstrup_invalid_read_packet_size():
    parser = kamstrup
    pkg = TestData.KAMSTRUP_WRONG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on mismatch between read and decoded pkg size"


def test_kamstrup_invalid_frame_flag():
    parser = kamstrup
    pkg = TestData.KAMSTRUP_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect frame flag"


def test_kamstrup_invalid_data_flag():

    parser = kamstrup
    pkg = TestData.KAMSTRUP_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect data flag"


def test_kamstrup_invalid_frame_crc():

    parser = kamstrup
    pkg = TestData.KAMSTRUP_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on frame crc"


def test_kamstrup_invalid_header_crc():

    parser = kamstrup
    pkg = TestData.KAMSTRUP_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on header crc"
