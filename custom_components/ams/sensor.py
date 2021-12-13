"""Support for reading data from a serial port."""
import logging
from datetime import timedelta

from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_utils

from custom_components.ams.const import (
    ACTIVE_ENERGY_DEFAULT_ATTRS,
    ACTIVE_ENERGY_SENSORS,
    AMS_DEVICES,
    AMS_ENERGY_METER,
    AMS_SENSOR_CREATED_BUT_NOT_READ,
    DOMAIN,
    HOURLY_SENSORS,
    SIGNAL_NEW_AMS_SENSOR,
    SIGNAL_UPDATE_AMS
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    # pylint: disable=unused-argument
    """Setup sensor platform for the ui"""

    @callback
    def async_add_sensor():
        """Add AMS Sensor."""
        sensors = []
        data = hass.data[DOMAIN].sensor_data

        for sensor_name in data:
            # Check that we don't add a new sensor that already exists.
            # We only try to update the state for sensors in AMS_DEVICES
            if sensor_name not in AMS_DEVICES:
                AMS_DEVICES.add(sensor_name)
                if sensor_name in AMS_SENSOR_CREATED_BUT_NOT_READ:
                    # The hourly sensors is added manually at the start.
                    continue

                sensor_states = {
                    "name": sensor_name,
                    "state": data.get(sensor_name, {}).get("state"),
                    "attributes": data.get(sensor_name, {}).get("attributes"),
                }
                sensors.append(AmsSensor(hass, sensor_states))

        # Handle the hourly sensors.
        for hourly in HOURLY_SENSORS:
            if hourly not in data and hourly not in (
                    AMS_SENSOR_CREATED_BUT_NOT_READ):
                AMS_SENSOR_CREATED_BUT_NOT_READ.add(hourly)
                _LOGGER.debug(
                    "Hourly sensor %s added so we can attempt to restore"
                    " state", hourly
                )
                sensor_states = {
                    "name": hourly,
                    "state": data.get(hourly, {}).get("state"),
                    "attributes": data.get(hourly, {}).get("attributes"),
                }
                if hourly in ACTIVE_ENERGY_SENSORS:
                    sensor_states = {
                        "name": hourly,
                        "state": data.get(hourly, {}).get("state"),
                        "attributes": data.get(hourly, {}).get("attributes", (
                            ACTIVE_ENERGY_DEFAULT_ATTRS)),
                    }
                sensors.append(AmsSensor(hass, sensor_states))

        if sensors:
            _LOGGER.debug("Trying to add %s sensors: %s", len(sensors),
                          sensors)
            async_add_devices(sensors)

    async_dispatcher_connect(hass, SIGNAL_NEW_AMS_SENSOR, async_add_sensor)

    return True


async def async_remove_entry(hass, entry):
    """Remove config entry from Homeassistant."""
    _LOGGER.debug("async_remove_entry AMS")
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "sensor")
        _LOGGER.info("Successfully removed sensor from the AMS Reader"
                     " integration")
    except ValueError:
        pass


class AmsSensor(RestoreEntity):
    """Representation of a AMS sensor."""

    def __init__(self, hass, sensor_states):
        """Initialize the Serial sensor."""
        self.ams = hass.data[DOMAIN]
        self._hass = hass
        self._name = sensor_states.get("name")
        self._meter_id = self.ams.meter_serial
        self._state = None
        self._attributes = {}
        self._update_properties()
        _LOGGER.debug("Init %s DUMP sensor_states %s", self._name,
                      sensor_states)

    def _update_properties(self):
        """Update all portions of sensor."""
        try:
            self._state = self.ams.sensor_data[self._name].get("state")
            self._attributes = self.ams.sensor_data[self._name].get(
                "attributes")
            self._meter_id = self.ams.meter_serial
            _LOGGER.debug("Updating sensor %s", self._name)
        except KeyError:
            pass

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
    def extra_state_attributes(self):
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
            "name": AMS_ENERGY_METER,
            "identifiers": {(DOMAIN, self._meter_id)},
            "manufacturer": self.ams.meter_manufacturer,
            "model": self.ams.meter_type,
        }

    async def async_added_to_hass(self):
        """Register callbacks and restoring states to hourly sensors."""
        await super().async_added_to_hass()
        async_dispatcher_connect(self._hass, SIGNAL_UPDATE_AMS,
                                 self._update_callback)
        old_state = await self.async_get_last_state()

        if old_state is not None and self._name and self._name in (
                HOURLY_SENSORS):
            if dt_utils.utcnow() - old_state.last_changed < timedelta(
                    minutes=60):
                if old_state.state == STATE_UNKNOWN:
                    _LOGGER.debug(
                        "%s state is unknown, this typically happens if "
                        "ha never never got the real state of %s and the "
                        "users restart ha",
                        self._name,
                        self._name,
                    )
                else:
                    _LOGGER.debug(
                        "The state for %s was set less then a hour ago,"
                        " so its still correct. Restoring state to %s with"
                        " attrs %s",
                        self._name,
                        old_state.state,
                        old_state.attributes,
                    )
                    self._state = old_state.state
                    self._attributes = old_state.attributes
                    self.async_write_ha_state()
            else:
                # I'll rather have unknown then wrong values.
                _LOGGER.debug(
                    "The old state %s was set more then 60 minutes ago %s,"
                    " ignoring it.",
                    old_state.state,
                    old_state.last_changed,
                )
        else:
            _LOGGER.debug("Skipping restore state for %s", self._name)

    @callback
    def _update_callback(self):
        """Update the state."""
        if self._name in AMS_DEVICES:
            self._update_properties()
            self.async_write_ha_state()
