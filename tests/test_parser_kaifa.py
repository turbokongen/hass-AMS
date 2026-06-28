import sys
from custom_components.ams.parsers import kaifa
from .common_test_data import TestData
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
)
sys.path.append('../')


def test_kaifa_MA304H4D_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4D_SHORT #THIS IS EQUAL TO LONG???
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1590
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 464
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.724
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 4.313
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 2.491
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 228.3
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 230.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 229.9
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 145122.745
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 47786.857
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 2231.914
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',
              'ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-9-18 14:56:15'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Poly Phase 3 Phase 230V/400V 4-Wire meter'
        assert a['meter_serial'] == '7340157011274532'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-9-18 14:56:15", "Missing attribute"


def test_kaifa_MA304H4D_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4D_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1590
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 464
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.724
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 4.313
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 2.491
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 228.3
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 230.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 229.9
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 145122.745
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 47786.857
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 2231.914
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',
              'ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-9-18 14:56:15'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Poly Phase 3 Phase 230V/400V 4-Wire meter'
        assert a['meter_serial'] == '7340157011274532'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-9-18 14:56:15", "Missing attribute"

def test_kaifa_MA304H4_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for parsed values    
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1415
    assert a['timestamp'] == '2022-10-29 19:58:56'    
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER


def test_kaifa_MA304H4_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H4_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1418
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 375
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 1.683
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 1.751
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 3.104
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 240.8
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 240.4
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 235.9
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-10-29 19:59:00'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Domestic/Industrial 3 Phase 400V 4-Wire meter'
        assert a['meter_serial'] == '6970631402055385'


def test_kaifa_MA304H3E_short():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H3E_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 549
    assert a['timestamp'] == '2022-11-7 09:44:38'   
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER


def test_kaifa_MA304H3E_long():

    parser = kaifa

    pkg = TestData.KAIFA_MA304H3E_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 546
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 81
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.781
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 1.829
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 2.062
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 232.0
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 234.8
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-11-7 09:44:40'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Domestic/Industrial 3 Phase 230V 3-Wire meter'
        assert a['meter_serial'] == '6970631404129954'


def test_kaifa_hourly():

    parser = kaifa

    pkg = TestData.KAIFA_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 119
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 289
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.678
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 0.808
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 1.019
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 228.7
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 229.8
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 10494.991
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 79.233
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 2059.951
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',  'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2020-2-3 16:00:10'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Domestic/Industrial 3 Phase 230V 3-Wire meter'
        assert a['meter_serial'] == '6970631405808469'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2020-2-3 16:00:10", "Missing attribute"


def test_kaifa_1phase():

    parser = kaifa

    pkg = TestData.KAIFA_1PH_SHORT
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 932
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 79
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 4.224
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 233.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_voltage_l1']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2020-3-31 22:16:40'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Domestic 1 Phase 230V/400V meter'
        assert a['meter_serial'] == '6970631403460324'


def test_kaifa_1phase_hourly():

    parser = kaifa
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"
    pkg = TestData.KAIFA_1PH_HOURLY
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=False)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1655
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 12
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 6.952
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 242.4
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 25591.693
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 4152.622
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 417.719
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_voltage_l1', 'ams_active_energy_import',
              'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-5-5 21:00:10'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Domestic 1 Phase 230V/400V meter'
        assert a['meter_serial'] == '6970631408225928'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-5-5 21:00:10", "Missing attribute"


def test_kaifa_H4PSE():

    parser = kaifa
    pkg = None
    assert not parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Package test for None failed"
    pkg = TestData.KAIFA_MA304H4D_LONG
    assert parser.test_valid_data(pkg, oss=TestData.OSS_FALSE), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg, swedish=True)

    # Test for some parsed values
    d = meter_data['ams_active_power_import']
    a = d['attributes']
    assert d['state'] == 1590
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_active_power_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'W'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    assert a['device_class'] == SensorDeviceClass.POWER

    d = meter_data['ams_reactive_power_import']
    a = d['attributes']
    assert d['state'] == 0
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_reactive_power_export']
    a = d['attributes']
    assert d['state'] == 464
    assert a['unit_of_measurement'] == 'VAr'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_POWER

    d = meter_data['ams_current_l1']
    a = d['attributes']
    assert d['state'] == 0.724
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l2']
    a = d['attributes']
    assert d['state'] == 4.313
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_current_l3']
    a = d['attributes']
    assert d['state'] == 2.491
    assert a['unit_of_measurement'] == 'A'
    assert a['icon'] == 'mdi:current-ac'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.CURRENT

    d = meter_data['ams_voltage_l1']
    a = d['attributes']
    assert d['state'] == 228.3
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l2']
    a = d['attributes']
    assert d['state'] == 230.6
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_voltage_l3']
    a = d['attributes']
    assert d['state'] == 229.9
    assert a['unit_of_measurement'] == 'V'
    assert a['icon'] == 'mdi:flash'
    # assert a['state_class'] == SensorStateClass.MEASUREMENT
    # assert a['device_class'] == SensorDeviceClass.VOLTAGE

    d = meter_data['ams_active_energy_import']
    a = d['attributes']
    assert d['state'] == 145122.745
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_active_energy_export']
    a = d['attributes']
    assert d['state'] == 0.0
    assert a['unit_of_measurement'] == 'kWh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    assert a['device_class'] == SensorDeviceClass.ENERGY

    d = meter_data['ams_reactive_energy_import']
    a = d['attributes']
    assert d['state'] == 47786.857
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    d = meter_data['ams_reactive_energy_export']
    a = d['attributes']
    assert d['state'] == 2231.914
    assert a['unit_of_measurement'] == 'kVArh'
    assert a['icon'] == 'mdi:gauge'
    assert a['state_class'] == SensorStateClass.TOTAL_INCREASING
    # assert a['device_class'] == SensorDeviceClass.REACTIVE_ENERGY

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import',
              'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3',
              'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',
              'ams_active_energy_import', 'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        a = meter_data[k]['attributes']
        assert a['timestamp'] == '2022-9-18 14:56:15'
        assert a['meter_manufacturer'] == 'Kfm_001'
        assert a['meter_type'] == 'Poly Phase 3 Phase 230V/400V 4-Wire meter'
        assert a['meter_serial'] == '7340157011274532'

    # Test for missing keys and some other attributes
    for k in ['ams_active_energy_import', 'ams_active_energy_export',
              'ams_reactive_energy_import', 'ams_reactive_energy_export']:
        a = meter_data[k]['attributes']
        assert a['meter_date_time'] == "2022-9-18 14:56:15", "Missing attribute"


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
