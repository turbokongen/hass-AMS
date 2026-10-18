"""Regression tests for optional Kamstrup 6841138 energy scaling."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.ams import _async_options_updated
from custom_components.ams.const import (
    CONF_KAMSTRUP_6841138_SCALE,
    DOMAIN,
)


@pytest.fixture(autouse=True)
def enable_integration(enable_custom_integrations):
    """Permit loading custom integration in Home Assistant tests."""
    yield


@pytest.mark.parametrize("enabled", [False, True])
async def test_options_form_default_and_save(hass, enabled):
    """Show current option and save user choice using HA options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"protocol": "tcp_ip"},
        options={CONF_KAMSTRUP_6841138_SCALE: enabled},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == "form"
    assert result["step_id"] == "init"
    schema = result["data_schema"]
    assert schema({})[CONF_KAMSTRUP_6841138_SCALE] is enabled

    updated = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_KAMSTRUP_6841138_SCALE: not enabled},
    )
    assert updated["type"] == "create_entry"
    assert updated["data"][CONF_KAMSTRUP_6841138_SCALE] is not enabled


async def test_options_default_disabled(hass):
    """Existing users without the option should see it disabled."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, options={})
    entry.add_to_hass(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] == "form"
    assert result["data_schema"]({})[CONF_KAMSTRUP_6841138_SCALE] is False


@pytest.mark.parametrize("enabled", [False, True])
async def test_options_listener_updates_hub(hass, enabled):
    """Updating options should update the existing hub in memory."""
    hub = SimpleNamespace(kamstrup_6841138_scale=not enabled)
    hass.data[DOMAIN] = hub
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        options={CONF_KAMSTRUP_6841138_SCALE: enabled},
    )
    await _async_options_updated(hass, entry)
    assert hub.kamstrup_6841138_scale is enabled


async def test_options_listener_handles_missing_hub(hass):
    """An update before setup or after unload must not raise."""
    hass.data.pop(DOMAIN, None)
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={},
        options={CONF_KAMSTRUP_6841138_SCALE: True},
    )
    await _async_options_updated(hass, entry)


async def test_setup_passes_selected_option_to_hub(hass):
    """Setup must merge stored options with entry data."""
    from custom_components.ams import async_setup_entry

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={"protocol": "tcp_ip"},
        options={CONF_KAMSTRUP_6841138_SCALE: True},
    )
    entry.add_to_hass(hass)
    with (
        patch("custom_components.ams._setup") as setup,
        patch.object(
            hass.config_entries,
            "async_forward_entry_setups",
            new_callable=AsyncMock,
        ),
    ):
        assert await async_setup_entry(hass, entry)
        setup.assert_called_once()
        config = setup.call_args.args[1]
        assert config[CONF_KAMSTRUP_6841138_SCALE] is True
