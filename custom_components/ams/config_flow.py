"""Adds config flow for hass-HAN."""
import logging

import serial.tools.list_ports as devices
import voluptuous as vol
from homeassistant import config_entries

from .const import (CONF_PARITY, CONF_SERIAL_PORT,
                    DEFAULT_PARITY, DOMAIN)

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
        ports = [(comport.device + ": " + comport.description)
                 for comport in portdata]

        if user_input is not None:
            return self.async_create_entry(
                title="Norwegian AMS", data=user_input)

        return self.async_show_form(step_id="user", data_schema=vol.Schema({
            vol.Required(CONF_SERIAL_PORT,
                         default=None): vol.In(ports),
            vol.Optional(CONF_PARITY, default=DEFAULT_PARITY): vol.All(str)
        }),
            description_placeholders={
                CONF_SERIAL_PORT: ports,
        }, errors=self._errors)

    async def async_step_import(self, user_input=None):
        """Import a config flow from configuration."""
        return self.async_create_entry(title="configuration.yaml", data={})
