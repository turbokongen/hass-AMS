"""Adds config flow for hass-HAN."""
import logging

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DOMAIN_SCH


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
        _LOGGER.debug("async_step_user, %r", user_input)

        if user_input is not None:
            return self.async_create_entry(title="Norwegian AMS", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(DOMAIN_SCH), errors=self._errors
        )

    async def async_step_import(self, user_input=None):
        """Import a config flow from configuration."""
        return self.async_create_entry(title="configuration.yaml", data={})
