"""Adds config flow for hass-AMS."""
import logging
import os

import serial.tools.list_ports as devices
import voluptuous as vol
from homeassistant import config_entries

from custom_components.ams.const import (  # pylint: disable=unused-import
    CONF_BAUDRATE,
    CONF_MANUAL_SERIAL_PORT,
    CONF_METER_MANUFACTURER,
    CONF_PARITY,
    CONF_PROTOCOL,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    CONF_SERIAL_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_METER_MANUFACTURER,
    DEFAULT_PARITY,
    DOMAIN,
    NETWORK,
    MANUFACTURER_OPTIONS,
    SERIAL,
)
DATA_SCHEMA_SELECT_PROTOCOL = vol.Schema(
    {vol.Required("type"): vol.In([SERIAL, CONF_MANUAL_SERIAL_PORT, NETWORK])}
)
DATA_SCHEMA_NETWORK_DATA = vol.Schema(
    {
        vol.Required(CONF_TCP_HOST): str,
        vol.Required(CONF_TCP_PORT): vol.All(vol.Coerce(int),
                                             vol.Range(0, 65535)),
        vol.Required(
            CONF_METER_MANUFACTURER,
            default=DEFAULT_METER_MANUFACTURER
        ): vol.In(MANUFACTURER_OPTIONS),
        vol.Optional(
            CONF_PARITY, default=DEFAULT_PARITY
        ): vol.All(str),
        vol.Optional(
            CONF_BAUDRATE, default=DEFAULT_BAUDRATE
        ): vol.All(int),
    }
)
_LOGGER = logging.getLogger(__name__)


class AmsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AMS."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self.connection_type = None

    async def async_step_user(self, user_input=None):
        """Handle selection of protocol."""
        if user_input is not None:
            self.connection_type = user_input["type"]
            if self.connection_type == NETWORK:
                return await self.async_step_network_connection()
            if self.connection_type == SERIAL:
                return await self.async_step_select_serial_connection()
            if self.connection_type == CONF_MANUAL_SERIAL_PORT:
                return await self.async_step_enter_serial_connection()

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA_SELECT_PROTOCOL,
            errors=self._errors
        )

    async def async_step_enter_serial_connection(self, user_input=None):
        """Handle the manual serialport connection step."""

        if user_input is not None:
            user_input[CONF_PROTOCOL] = SERIAL
            entry_result = self.async_create_entry(
                title="AMS Reader", data=user_input,
            )
            if entry_result:
                return entry_result

        return self.async_show_form(
            step_id="enter_serial_connection",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SERIAL_PORT, default=None
                    ): vol.All(str),
                    vol.Required(
                        CONF_METER_MANUFACTURER,
                        default=DEFAULT_METER_MANUFACTURER
                    ): vol.In(MANUFACTURER_OPTIONS),
                    vol.Optional(
                        CONF_PARITY, default=DEFAULT_PARITY
                    ): vol.All(str),
                    vol.Optional(
                        CONF_BAUDRATE, default=DEFAULT_BAUDRATE
                    ): vol.All(int),
                }
            ),
            errors=self._errors,
        )

    async def async_step_select_serial_connection(self, user_input=None):
        """Handle the select serialport connection step."""
        portdata = await self.hass.async_add_executor_job(devices.comports)
        _LOGGER.debug(portdata)
        ports = [(comport.device + ": " + comport.description) for
                 comport in portdata]

        if user_input is not None:
            user_input[CONF_PROTOCOL] = SERIAL
            user_selection = user_input[CONF_SERIAL_PORT]
            port = portdata[ports.index(user_selection)]
            serial_by_id = await self.hass.async_add_executor_job(
                get_serial_by_id, port.device
            )
            user_input[CONF_SERIAL_PORT] = serial_by_id
            entry_result = self.async_create_entry(
                title="AMS Reader", data=user_input,
            )
            if entry_result:
                return entry_result

        _LOGGER.debug(ports)
        return self.async_show_form(
            step_id="select_serial_connection",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SERIAL_PORT, default=None
                    ): vol.In(ports),
                    vol.Required(
                        CONF_METER_MANUFACTURER,
                        default=DEFAULT_METER_MANUFACTURER
                    ): vol.In(MANUFACTURER_OPTIONS),
                    vol.Optional(
                        CONF_PARITY, default=DEFAULT_PARITY
                    ): vol.All(str),
                    vol.Optional(
                        CONF_BAUDRATE, default=DEFAULT_BAUDRATE
                    ): vol.All(int),
                }
            ),
            errors=self._errors,
        )

    async def async_step_network_connection(self, user_input=None):
        """Handle the network connection step."""
        if user_input:
            user_input[CONF_PROTOCOL] = NETWORK
            entry_result = self.async_create_entry(
                title="AMS Reader", data=user_input,
            )
            if entry_result:
                return entry_result

        return self.async_show_form(
            step_id="network_connection",
            data_schema=DATA_SCHEMA_NETWORK_DATA,
            errors={},
        )

    async def async_step_import(self, import_config):
        """Import a config flow from configuration."""
        if self._async_current_entries():
            _LOGGER.warning("Only one configuration of AMS Reader is allowed.")
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml",
                                       data=import_config)


def get_serial_by_id(dev_path):
    """Return a /dev/serial/by-id match for given device if available."""
    by_id = "/dev/serial/by-id"
    if not os.path.isdir(by_id):
        return dev_path

    for path in (entry.path for entry in os.scandir(by_id)
                 if entry.is_symlink()):
        if os.path.realpath(path) == dev_path:
            return path
    return dev_path
