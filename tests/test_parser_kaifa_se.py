import sys
from custom_components.ams.parsers import kaifa_se
from .common_test_data import TestData
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)
sys.path.append('../')


def test_kaifa_MA304H4_se():

    parser = kaifa_se
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"

    pkg = TestData.KAIFA_MA304H4_SE
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 297
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
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 107
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.616
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 0.529
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 0.558
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 235.4
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 236.9
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 235.2
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 9732.707
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
    assert d['state'] == 77.766
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 1272.619
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3', 'ams_active_energy_import',
              'ams_active_energy_export', 'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert 'unit_of_measurement' in a, "Missing attribute"
        assert a['meter_manufacturer'] == "KFM_001", "Missing attribute"
        assert a['meter_type'] == "Domestic/Industrial 3 Phase 400V 4-Wire meter", "Missing attribute"
        assert a['meter_serial'] == '7340157030548300', "Missing attribute"

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-10-15-15-08-08-15", "Missing attribute"


def test_kaifa_se_invalid_packet_size():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on incorrect pkg range size"


def test_kaifa_se_invalid_read_packet_size():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_WRONG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), \
        "Data validity test failed on mismatch between read and decoded pkg size"


def test_kaifa_se_invalid_frame_flag():
    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect frame flag"


def test_kaifa_se_invalid_data_flag():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect data flag"


def test_kaifa_se_invalid_frame_crc():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on frame crc"


def test_kaifa_se_invalid_header_crc():

    parser = kaifa_se
    pkg = TestData.KAIFA_SE_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on header crc"
