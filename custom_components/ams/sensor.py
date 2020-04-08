"""Support for reading data from a serial port."""
import logging

import custom_components.ams as amshub
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (AMS_DEVICES, DOMAIN, SIGNAL_NEW_AMS_SENSOR,
                    SIGNAL_UPDATE_AMS)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup sensor platform for the ui"""
    _LOGGER.debug("called async_setup_entry to enable async_add_sensor callback")

    @callback
    def async_add_sensor():
        """Add AMS Sensor."""
        _LOGGER.debug("async_add_sensor callback in async_setup_entry")
        sensors = []
        data = hass.data[DOMAIN].sensor_data

        for sensor_name in data:
            # Check that we dont add a new sensor that already exists.
            if sensor_name not in AMS_DEVICES:
                AMS_DEVICES.add(sensor_name)
                sensor_states = {
                    "name": sensor_name,
                    "state": data[sensor_name].get("state"),
                    "attributes": data[sensor_name].get("attributes"),
                }
                sensors.append(AmsSensor(hass, sensor_states))

        if len(sensors):
            _LOGGER.debug("Trying to add %s sensors", len(sensors))
            async_add_devices(sensors, True)

    async_dispatcher_connect(hass, SIGNAL_NEW_AMS_SENSOR, async_add_sensor)

    return True


async def async_remove_entry(hass, entry):
    """Remove config entry from Homeassistant."""
    _LOGGER.debug("async_remove_entry AMS")
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "sensor")
        _LOGGER.info("Successfully removed sensor from the Norwegian AMS integration")
    except ValueError:
        pass


class AmsSensor(RestoreEntity):
    """Representation of a Serial sensor."""

    def __init__(self, hass, sensor_states):
        """Initialize the Serial sensor."""
        self.ams = hass.data[DOMAIN]
        self._hass = hass
        self._name = sensor_states.get("name")
        self._meter_id = None
        self._state = None
        self._attributes = {}
        _LOGGER.debug("Initialize %s", self._name)
        _LOGGER.debug("%s ", sensor_states)
        _LOGGER.debug("%s ", sensor_states.get("state"))
        _LOGGER.debug("%s ", sensor_states.get("attributes"))
        # Force update of atts so the meter_id exist or the enity
        # will not have serial number. (get another unique_id, then the user expects.)
        self._update_properties()

    def _update_properties(self):
        """Update all portions of sensor."""
        try:
            self._state = self.ams.data[self._name].get("state")
            self._attributes = self.ams.data[self._name].get("attributes")
            self._meter_id = self._attributes.get("meter_serial")
            _LOGGER.debug("updating sensor %s", self._name)
        except KeyError as e:
            _LOGGER.debug("Sensor not in hass.data, %s", e)

    @property
    def unique_id(self) -> str:
        """Return the unique id of the sensor."""
        return f"{self._name}_{self._meter_id}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self.unique_id

    @property
    def should_poll(self) -> bool:
        """No polling needed."""
        return False

    @property
    def device_state_attributes(self):
        """Return the attributes of the entity (if any JSON present)."""
        return self._attributes

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self) -> dict:
        """Return the device info."""

        return {
            "name": self.name,
            "identifiers": {(DOMAIN, self.unique_id)},
            "manufacturer": self._attributes.get("meter_manufacturer"),
            "model": self._attributes.get("meter_type"),
        }

    async def async_added_to_hass(self):
        """Register callbacks."""
        await super().async_added_to_hass()
        async_dispatcher_connect(self._hass, SIGNAL_UPDATE_AMS, self._update_callback)
        state = await self.async_get_last_state()
        if state is not None:  
            self._state = state.state
        
    @callback
    def _update_callback(self):
        """Update the state."""
        self._update_properties()
        self.async_schedule_update_ha_state()
