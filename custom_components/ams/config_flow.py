"""Adds config flow for hass-AMS."""
import logging
import os

import serial.tools.list_ports as devices
import voluptuous as vol
from homeassistant import config_entries

from custom_components.ams.const import (  # pylint: disable=unused-import
    CONF_BAUDRATE,
    CONF_METER_MANUFACTURER,
    CONF_PARITY,
    CONF_SERIAL_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_METER_MANUFACTURER,
    DEFAULT_PARITY,
    DOMAIN,
    MANUFACTURER_OPTIONS
)

_LOGGER = logging.getLogger(__name__)


class AmsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AMS."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        portdata = await self.hass.async_add_executor_job(devices.comports)
        ports = [(comport.device + ": " + comport.description) for
                 comport in portdata]

        if user_input is not None:
            user_selection = user_input[CONF_SERIAL_PORT]
            port = portdata[ports.index(user_selection)]
            serial_by_id = await self.hass.async_add_executor_job(
                get_serial_by_id, port.device
            )
            user_input[CONF_SERIAL_PORT] = serial_by_id
            return self.async_create_entry(title="AMS Reader",
                                           data=user_input)
        _LOGGER.debug(ports)
        return self.async_show_form(
            step_id="user",
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
            description_placeholders={
                CONF_SERIAL_PORT: ports,
                CONF_METER_MANUFACTURER: MANUFACTURER_OPTIONS,
                CONF_PARITY: DEFAULT_PARITY,
                CONF_BAUDRATE: DEFAULT_BAUDRATE,
            },
            errors=self._errors,
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
