import sys
from custom_components.ams.parsers import aidon_se
from .common_test_data import TestData
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)
sys.path.append('../')


def test_aidon_se():  # Swedish AMS data pushes all sensor at each transmit. Only one type of package is pushed

    parser = aidon_se
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"

    pkg = TestData.AIDON_SE_3PH
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 760
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
    assert d['state'] == 1040
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_active_power_import_l1']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export_l1']
    a = d['attributes']
    assert d['state'] == 39
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import_l1']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export_l1']
    a = d['attributes']
    assert d['state'] == 242
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_active_power_import_l2']
    a = d['attributes']
    assert d['state'] == 379
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export_l2']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import_l2']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export_l2']
    a = d['attributes']
    assert d['state'] == 388
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_active_power_import_l3']
    a = d['attributes']
    assert d['state'] == 421
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export_l3']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_export_l3']
    a = d['attributes']
    assert d['state'] == 403
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_import_l3']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == -1.0
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 2.3
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 2.4
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 234.8
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 236.1
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 237.8
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 38211.671
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['meter_date_time'] == '2022-10-16-16-14-14-10'
    assert a['device_class'] == SensorDeviceClass.ENERGY
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 9896.295
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['meter_date_time'] == '2022-10-16-16-14-14-10'
    assert a['device_class'] == SensorDeviceClass.ENERGY
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 87.498
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['meter_date_time'] == '2022-10-16-16-14-14-10'
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 9423.279
    assert a['meter_manufacturer'] == 'AIDON_H0001'
    assert a['unit_of_measurement'] == 'kVAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['meter_date_time'] == '2022-10-16-16-14-14-10'
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['meter_manufacturer'] == "AIDON_H0001", "Missing attribute"
        assert 'unit_of_measurement' in a, "Missing attribute"
        assert a['meter_type'] == 'RF2-system module Integrated HAN'
        assert a['meter_serial'] == '00'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-10-16-16-14-14-10", "Missing attribute"

def test_aidon_se_invalid_packet_size():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect pkg range size"


def test_aidon_se_invalid_read_packet_size():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_WRONG_SIZE
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on mismatch between read and decoded pkg size"


def test_aidon_se_invalid_frame_flag():
    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect frame flag"


def test_aidon_se_invalid_data_flag():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on incorrect data flag"


def test_aidon_se_invalid_frame_crc():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on frame crc"


def test_aidon_se_invalid_header_crc():

    parser = aidon_se
    pkg = TestData.AIDON_SE_3PH_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed on header crc"
