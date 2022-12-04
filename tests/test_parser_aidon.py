
import pytest
import logging
import pprint
import sys


sys.path.append('../')

from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN
from .common_test_data import TestData

def test_aidon_hourly():

    parser = aidon
    pkg = None
    assert not parser.test_valid_data(pkg), "Package test for None failed"

    pkg = TestData.AIDON_HOURLY
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    #pprint.pprint(meter_data)
    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1769, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"
    assert meter_data['ams_active_energy_import']['state'] == 94064.59, "Parsed ams_active_energy_import is not correct"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3',  'ams_active_energy_import', 'ams_reactive_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_export']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"

def test_aidon_short():

    parser = aidon
    pkg = TestData.AIDON_SHORT
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    #pprint.pprint(meter_data)
    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 6942, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"

def test_aidon_mini():

    parser = aidon
    pkg = TestData.AIDON_MINI
    assert parser.test_valid_data(pkg), "Data validity test failed"
    meter_data, _ = parser.parse_data({}, pkg)
    #pprint.pprint("meter_data=%s", meter_data)
    # Test for parsed values
    assert meter_data == {}
    FIXTURE_AIDON_STORED = {
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
    meter_data, _ = parser.parse_data(FIXTURE_AIDON_STORED, pkg)
    assert meter_data['ams_active_power_import']['state'] == 734, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

def test_aidon_invalid_packet_size():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_PKG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect pkg range size"

def test_aidon_invalid_read_packet_size():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_WRONG_SIZE
    assert not parser.test_valid_data(pkg), "Data validity test failed on mismatch between read and decoded pkg size"

def test_aidon_invalid_frame_flag():
    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_FRAME_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect frame flag"

def test_aidon_invalid_data_flag():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INVALID_DATA_FLAG
    assert not parser.test_valid_data(pkg), "Data validity test failed on incorrect data flag"

def test_aidon_invalid_frame_crc():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INCORRECT_PKG_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on frame crc"

def test_aidon_invalid_header_crc():

    parser = aidon
    pkg = TestData.AIDON_HOURLY_INCORRECT_HEADER_CRC
    assert not parser.test_valid_data(pkg), "Data validity test failed on header crc"

