
import pytest
import logging
import pprint
import sys


sys.path.append('../../../')

from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN


from common_test_data import TestData


def test_aidon_se_short():

    parser = aidon_se

    pkg = TestData.AIDON_SE_SHORT
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)
    assert meter_data['ams_active_power_import']['state'] == 1590, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

def test_aidon_se_long():

    parser = aidon_se

    pkg = TestData.AIDON_SE_LONG
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    #pprint.pprint(meter_data)
    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 810, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "AIDON_H0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"

