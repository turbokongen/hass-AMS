"""Support for reading data from a serial port."""
import logging

from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import callback

from .const import (
    DOMAIN,
    DOMAIN_DATA,
    SIGNAL_UPDATE_AMS,
    PLATTFORM_SCH,
    SIGNAL_NEW_AMS_SENSOR,
    AMS_DEVICES,
)

_LOGGER = logging.getLogger(__name__)

# Is this even used??
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(PLATTFORM_SCH)


async def async_setup_platform(
    hass, config_entry, async_add_devices, discovery_info=None
) -> True:
    """Set up the Serial sensor platform."""

    @callback
    def async_add_sensor() -> bool:
        """Add AMS Sensor."""
        sensors = []
        _LOGGER.info("called async_add_sensor cb")
        data = hass.data[DOMAIN_DATA]["client"].sensor_data
        for sensor_name in data:
            if sensor_name not in AMS_DEVICES:
                AMS_DEVICES.add(sensor_name)
                sensor_states = {
                    "name": sensor_name,
                    "state": data[sensor_name].get("state"),
                    "attributes": data[sensor_name].get("attributes"),
                }
                sens = AmsSensor(hass, sensor_states)
                sensors.append(sens)

        if len(sensors):
            async_add_devices(sensors, True)
            _LOGGER.debug("Added %s sensors", len(sensors))
            return True
        else:
            _LOGGER.debug("No sensorz added.")
            return False

    # Add the cb so the function async_add_sensor is run when SIGNAL_NEW_AMS_SENSOR
    async_dispatcher_connect(hass, SIGNAL_NEW_AMS_SENSOR, async_add_sensor)

    return True


async def async_setup_entry(hass, config_entry, async_add_devices) -> True:
    """Set up the Serial from the webui."""
    # reuse use the yaml method to keep things dry.
    await async_setup_platform(hass, config_entry, async_add_devices, {})
    return True


async def async_remove_entry(hass, entry) -> None:
    """Remove config entry from Homeassistant."""
    _LOGGER.debug("async_remove_entry AMS")
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "sensor")
        _LOGGER.debug("Successfully removed sensor from the Norwegian AMS integration")
    except ValueError:
        pass


class AmsSensor(Entity):
    """Representation of a Serial sensor."""

    def __init__(self, hass, sensor_states) -> None:
        """Initialize the Serial sensor."""
        self.ams = hass.data[DOMAIN_DATA]["client"]
        self._hass = hass
        self._name = sensor_states.get("name")
        self._meter_id = self.ams.meter_serial
        self._state = None
        self._attributes = {}

    def _update_properties(self) -> None:
        """Update all portions of sensor."""
        try:
            self._state = self.ams.data[self._name].get("state")
            self._attributes = self.ams.data[self._name].get("attributes")
            _LOGGER.debug("updating sensor %s, %s", self._name, self._meter_id)
        except KeyError:
            pass

    @property
    def unique_id(self) -> str:
        """Return the uniqe id of the sensor."""
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
            "manufacturer": self.ams.meter_manufacturer,
            "model": self.ams.meter_type,
        }

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        async_dispatcher_connect(self._hass, SIGNAL_UPDATE_AMS, self._update_callback)

    @callback
    def _update_callback(self) -> None:
        """Update the state."""
        _LOGGER.debug("Called _update_callback")
        self._update_properties()
        self.async_schedule_update_ha_state(True)
