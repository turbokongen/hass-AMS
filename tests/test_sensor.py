"""Test sensor for ams integration."""
import sys
from custom_components.ams.const import DOMAIN
from pytest_homeassistant_custom_component.common import MockConfigEntry
from unittest.mock import patch
sys.path.append('../')


MOCK_SERIAL_CONFIG = {
    'protocol': 'serial',
    'serial_port': '/dev/testUSB1',
    'meter_manufacturer': 'auto',
    'parity': 'N',
    'baudrate': 2400
}
MOCK_NETWORK_CONFIG = {
    'protocol': 'tcp_ip',
    'tcp_host': '10.0.0.99',
    'tcp_port': 12345,
    'meter_manufacturer': 'auto',
    'parity': 'N',
    'baudrate': 2400
}


async def test_sensor(hass):
    """Test sensor."""
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_NETWORK_CONFIG)
    with patch("serial.Serial", autospec=True):
        entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.example_temperature")

    assert state
    assert state.state == "23"
