
import unittest
import logging
import pprint
import sys


sys.path.append('../../../')

from custom_components.ams.const import *
import custom_components.ams
from custom_components.ams.parsers import aidon
from custom_components.ams.parsers import aidon_se
from custom_components.ams.parsers import kaifa
from custom_components.ams.parsers import kaifa_se
from custom_components.ams.parsers import kamstrup
from custom_components.ams import AmsHub
from custom_components.ams.const import DOMAIN


from common_test_data import TestData

class TestParserKaifa(unittest.TestCase):

    def test_kaifa_MA304H4_se(self):

        parser = kaifa_se

        pkg = TestData.KAIFA_MA304H4_SE
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg)

        # Test for some parsed values
        self.assertEqual(meter_data['ams_active_power_import']['state'], 297, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

        # Test for missing keys and some attributes
        for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3', 'ams_active_energy_import', 'ams_active_energy_export', 'ams_reactive_energy_import', 'ams_reactive_energy_export']:
            self.assertIn(k, meter_data, msg="Key missing in parsed data")
            self.assertEqual(meter_data[k]['attributes']['meter_manufacturer'], "KFM_001", msg="Missing attribute")
            self.assertIn('unit_of_measurement', meter_data[k]['attributes'], msg="Missing attribute")

    def test_kaifa_MA304H4D_short(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H4D_SHORT
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)
        self.assertEqual(meter_data['ams_active_power_import']['state'], 1590, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

    def test_kaifa_MA304H4D_long(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H4D_LONG
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)

        #pprint.pprint(meter_data)
        # Test for some parsed values
        self.assertEqual(meter_data['ams_active_power_import']['state'], 546, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

        # Test for missing keys and some attributes
        for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
            self.assertIn(k, meter_data, msg="Key missing in parsed data")
            self.assertEqual(meter_data[k]['attributes']['meter_manufacturer'], "Kfm_001", msg="Missing attribute")
            self.assertIn('unit_of_measurement', meter_data[k]['attributes'], msg="Missing attribute")


    def test_kaifa_MA304H4_short(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H4_SHORT
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)
        self.assertEqual(meter_data['ams_active_power_import']['state'], 1415, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

    def test_kaifa_MA304H4_long(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H4_LONG
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)

        #pprint.pprint(meter_data)
        # Test for some parsed values
        self.assertEqual(meter_data['ams_active_power_import']['state'], 546, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

        # Test for missing keys and some attributes
        for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
            self.assertIn(k, meter_data, msg="Key missing in parsed data")
            self.assertEqual(meter_data[k]['attributes']['meter_manufacturer'], "Kfm_001", msg="Missing attribute")
            self.assertIn('unit_of_measurement', meter_data[k]['attributes'], msg="Missing attribute")


    def test_kaifa_MA304H3E_short(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H3E_SHORT
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)

        # Test for parsed values
        self.assertEqual(meter_data['ams_active_power_import']['state'], 549, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")


    def test_kaifa_MA304H3E_long(self):

        parser = kaifa

        pkg = TestData.KAIFA_MA304H3E_LONG
        self.assertTrue(parser.test_valid_data(pkg), msg="Data validity test failed")

        meter_data, _ = parser.parse_data({}, pkg, swedish = False)

        # Test for some parsed values
        self.assertEqual(meter_data['ams_active_power_import']['state'], 546, msg="Parsed ams_active_power_import is not correct")
        self.assertEqual(meter_data['ams_active_power_import']['attributes']['unit_of_measurement'], "W", msg="Missing attribute")

        # Test for missing keys and some attributes
        for k in ['ams_active_power_import', 'ams_active_power_export', 'ams_reactive_power_import', 'ams_reactive_power_export', 'ams_current_l1', 'ams_current_l2', 'ams_current_l3', 'ams_voltage_l1', 'ams_voltage_l2', 'ams_voltage_l3']:
            self.assertIn(k, meter_data, msg="Key missing in parsed data")
            self.assertEqual(meter_data[k]['attributes']['meter_manufacturer'], "Kfm_001", msg="Missing attribute")
            self.assertIn('unit_of_measurement', meter_data[k]['attributes'], msg="Missing attribute")


if __name__ == '__main__':

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    root.addHandler(handler)

    unittest.main()