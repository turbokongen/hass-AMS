"""Regression tests for issue #115: reactive energy metadata.

Uses the existing, checked-in meter telegram fixtures. No meter or serial
port is required. Test failures against pre-fix master are expected.
"""

from types import SimpleNamespace

import pytest
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass

from custom_components.ams.const import DOMAIN, SENSOR_UNIT
from custom_components.ams.parsers import aidon, kaifa, kamstrup
from custom_components.ams.sensor import AmsSensor
from .common_test_data import TestData


ENERGY_EXPECTATIONS = (
    ("ams_active_energy_import", SensorDeviceClass.ENERGY, "kWh"),
    ("ams_active_energy_export", SensorDeviceClass.ENERGY, "kWh"),
    ("ams_reactive_energy_import", SensorDeviceClass.REACTIVE_ENERGY, "kvarh"),
    ("ams_reactive_energy_export", SensorDeviceClass.REACTIVE_ENERGY, "kvarh"),
)

@pytest.fixture(params=[
    pytest.param(
        (aidon, TestData.AIDON_HOURLY, {}),
        id="aidon-hourly"
    ),
    pytest.param(
        (kaifa, TestData.KAIFA_HOURLY, {"swedish": False}),
        id="kaifa-hourly"
    ),
    pytest.param(
        (kamstrup, TestData.KAMSTRUP_HOURLY, {}),
        id="kamstrup-hourly"
    ),
])
def hourly_meter_data(request):
    parser, telegram, kwargs = request.param
    assert parser.test_valid_data(telegram, oss=TestData.OSS_FALSE)
    parsed, _ = parser.parse_data({}, telegram, **kwargs)
    return parsed


@pytest.mark.parametrize("key,device_class,unit", ENERGY_EXPECTATIONS)
def test_energy_units_defined_centrally(key, device_class, unit):
    """All parsers share SENSOR_UNIT, so correct it once in const.py."""
    assert SENSOR_UNIT[key] == unit


def test_hourly_packets_contain_all_energy_counters(hourly_meter_data):
    for key, _, unit in ENERGY_EXPECTATIONS:
        assert key in hourly_meter_data
        reading = hourly_meter_data[key]
        assert isinstance(reading["state"], (int, float))
        assert reading["attributes"]["unit_of_measurement"] == unit


@pytest.mark.parametrize("key,device_class,unit", ENERGY_EXPECTATIONS)
def test_sensor_entity_metadata_for_all_meter_types(
    hourly_meter_data, key, device_class, unit
):
    """Check effective HA entity properties, not just parser dictionaries."""
    fake_ams = SimpleNamespace(
        sensor_data=hourly_meter_data,
        meter_serial="test-meter",
        meter_manufacturer="Test manufacturer",
        meter_type="Test model",
    )
    fake_hass = SimpleNamespace(data={DOMAIN: fake_ams})
    sensor = AmsSensor(fake_hass, {"name": key})

    assert sensor.unique_id == f"{key}_test-meter"
    assert sensor.device_class == device_class
    assert sensor.state_class == SensorStateClass.TOTAL_INCREASING
    assert sensor.native_unit_of_measurement == unit
    assert sensor.native_value == hourly_meter_data[key]["state"]


def test_energy_import_export_have_distinct_ids(hourly_meter_data):
    fake_ams = SimpleNamespace(sensor_data=hourly_meter_data, meter_serial="x")
    fake_hass = SimpleNamespace(data={DOMAIN: fake_ams})
    ids = [AmsSensor(fake_hass, {"name": key}).unique_id
           for key, _, _ in ENERGY_EXPECTATIONS]
    assert len(ids) == len(set(ids))
