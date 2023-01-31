"""Tests for config_flow."""
import asyncio
import pytest
import logging
import sys
import serial.tools.list_ports
import serial.tools.list_ports_common
from custom_components.ams.const import DOMAIN
from homeassistant import config_entries, data_entry_flow
from unittest.mock import patch
sys.path.append('../')


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield

MOCK_SERIAL_CONFIG = {
    'protocol': 'serial',
    'serial_port': '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0',
    'meter_manufacturer': 'auto',
    'parity': 'N',
    'baudrate': 2400
}
FIXTURE_USER_INPUT_MANUAL_SERIAL = {'type': 'manual_serial_port'}
FIXTURE_USER_INPUT_SERIAL = {'type': 'serial'}
FIXTURE_USER_INPUT_NETWORK = {'type': 'tcp_ip'}

_LOGGER = logging.getLogger(__name__)


# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch("custom_components.ams.async_setup", return_value=True,), patch(
        "custom_components.ams.async_setup_entry",
        return_value=True,
    ):
        yield

@pytest.fixture()
def testing_event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

def com_port():
    """Mock of a serial port."""
    port = serial.tools.list_ports_common.ListPortInfo("/dev/testUSB1")
    port.serial_number = "1234"
    port.manufacturer = "Mock Inc."
    port.device = "/dev/testUSB1"
    port.description = "Mocked serial port"

    return port


# Here we simulate a successful config flow from the backend.
# Note that we use the `bypass_get_data` fixture here because
# we want the config flow validation to succeed during the test.
async def start_options_flow(hass, entry):
    """Start the options flow with the entry under test."""
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return await hass.config_entries.options.async_init(entry.entry_id)


async def test_select_serial_config_flow(hass):
    """Test a successful select serial port select config flow."""
    # Initialize the first config flow, user step.
    with patch("serial.tools.list_ports.comports", return_value=[com_port()]):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == 'form'
    assert result["step_id"] == "user"

    # If a user were to select 'serial_port' it would result in this function call
    with patch("serial.tools.list_ports.comports", return_value=[com_port()]):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=FIXTURE_USER_INPUT_SERIAL
        )

    # Check that the config flow step is complete and the next schema is loaded with
    # the correct input data
    _LOGGER.debug(result)
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "select_serial_connection"

    fixture_serial_input = {
        'serial_port': "/dev/testUSB1: Mocked serial port",
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400}
    with patch(
            "custom_components.ams.async_setup_entry",
            return_value=True,
    ), patch(
        "serial.tools.list_ports.comports",
        return_value=[com_port()],
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=fixture_serial_input)

    assert result["type"] == "create_entry"
    assert result["title"] == "AMS Reader"
    assert result["data"] == {
        'serial_port': '/dev/testUSB1',
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400,
        'protocol': 'serial',
        'oss_brikken': False,
    }


async def test_enter_serial_config_flow(hass):
    """Test a successful serial port select config flow."""
    # Initialize the first config flow, user step.
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == 'form'
    assert result["step_id"] == "user"

    # If a user were to select 'serial_port' it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=FIXTURE_USER_INPUT_MANUAL_SERIAL
    )

    # Check that the config flow step is complete and the next schema is loaded with
    # the correct input data
    _LOGGER.debug(result)
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "enter_serial_connection"

    fixture_serial_input = {
        'serial_port': '/dev/testUSB1',
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400}
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=fixture_serial_input)

    assert result["type"] == "create_entry"
    assert result["title"] == "AMS Reader"
    assert result["data"] == {
        'serial_port': '/dev/testUSB1',
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400,
        'protocol': 'serial',
        'oss_brikken': False,
    }

async def test_serial_network_config_flow(hass):
    """Test a successful serial network config flow."""
    # Initialize the first config flow, user step.
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == 'form'
    assert result["step_id"] == "user"

    # If a user were to select 'serial_port' it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=FIXTURE_USER_INPUT_NETWORK
    )

    # Check that the config flow step is complete and the next schema is loaded with
    # the correct input data
    _LOGGER.debug(result)
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "network_connection"

    fixture_network_config = {
        'tcp_host': '10.0.0.99',
        'tcp_port': 12345,
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400}
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=fixture_network_config)

    assert result["type"] == "create_entry"
    assert result["title"] == "AMS Reader"
    assert result["data"] == {
        'tcp_host': '10.0.0.99',
        'tcp_port': 12345,
        'meter_manufacturer': 'auto',
        'parity': 'N',
        'baudrate': 2400,
        'protocol': 'tcp_ip'
    }
