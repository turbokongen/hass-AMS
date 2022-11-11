
import pytest
import logging
import pprint
import sys


sys.path.append('../../../')

from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN


from common_test_data import TestData


def test_kamstrup():

    parser = kamstrup

    pkg = TestData.KAMSTRUP
    assert parser.test_valid_data(pkg), "Data validity test failed"

    meter_data, _ = parser.parse_data({}, pkg)

    #pprint.pprint(meter_data)
    # Test for some parsed values
    assert meter_data['ams_active_power_import']['state'] == 1202, "Parsed ams_active_power_import is not correct"
    assert meter_data['ams_active_power_import']['attributes']['unit_of_measurement'] == "W", "Missing attribute"

    # Test for missing keys and some attributes
    for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
        assert k in meter_data, "Key missing in parsed data"
        assert meter_data[k]['attributes']['meter_manufacturer'] == "Kamstrup_V0001", "Missing attribute"
        assert 'unit_of_measurement' in meter_data[k]['attributes'], "Missing attribute"

