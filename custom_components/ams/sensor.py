"""Support for reading data from a serial port."""
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
import custom_components.ams as amshub
from .const import _LOGGER, DOMAIN, SIGNAL_NEW_AMS_SENSOR, SIGNAL_UPDATE_AMS


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup sensor platform for the ui"""

    @callback
    def async_add_sensor():
        """Add AMS Sensor."""
        data = hass.data[amshub.AMS_SENSORS]
        _LOGGER.debug('HUB in async_setup_entry-async_add_sensor= %s',
                      hass.data[DOMAIN].data)
        _LOGGER.debug('AMS_SENSORS in async_setup_entry-async_add_sensor= %s',
                      hass.data[amshub.AMS_SENSORS])

        for sensor_name in list(data):
            sensor_states = {
                'name': sensor_name,
                'state': data[sensor_name].get('state'),
                'attributes': data[sensor_name].get('attributes')
                }
            sensors.append(AmsSensor(hass, sensor_states))
        _LOGGER.debug('async_add_sensor in async_setup_entry')
        async_add_devices(sensors, True)

    async_dispatcher_connect(hass, SIGNAL_NEW_AMS_SENSOR, async_add_sensor)
    sensor_states = {}
    sensors = []
    data = hass.data[amshub.AMS_SENSORS]
    _LOGGER.debug('HUB in async_setup_entry= %s', hass.data[DOMAIN].data)
    _LOGGER.debug('AMS_SENSORS in async_setup_entry= %s',
                  hass.data[amshub.AMS_SENSORS])

    for sensor_name in list(data):
        sensor_states = {
            'name': sensor_name,
            'state': data[sensor_name].get('state'),
            'attributes': data[sensor_name].get('attributes')
            }
        sensors.append(AmsSensor(hass, sensor_states))
    _LOGGER.debug('async_add_devices in end of async_setup_entry')
    async_add_devices(sensors)
    return True


async def async_remove_entry(hass, entry):
    """Remove config entry from Homeassistant."""
    _LOGGER.debug("async_remove_entry AMS")
    try:
        await hass.config_entries.async_forward_entry_unload(entry, "sensor")
        _LOGGER.info(
            "Successfully removed sensor from the Norwegian AMS integration")
    except ValueError:
        pass


class AmsSensor(Entity):
    """Representation of a Serial sensor."""

    def __init__(self, hass, sensor_states):
        """Initialize the Serial sensor."""
        self.ams = hass.data[DOMAIN]
        self._hass = hass
        self._name = sensor_states.get('name')
        self._meter_id = None
        self._state = None
        self._attributes = None
        _LOGGER.debug('%s ', sensor_states)
        _LOGGER.debug('%s ', sensor_states.get('state'))
        _LOGGER.debug('%s ', sensor_states.get('attributes'))
        self._update_properties()

    def _update_properties(self):
        """Update all portions of sensor."""
        try:
            self._state = self.ams.data[self._name].get('state')
            self._attributes = self.ams.data[self._name].get('attributes')
            self._meter_id = self._attributes.get('meter_serial')
            _LOGGER.debug('updating sensor %s', self._name)
        except KeyError:
            _LOGGER.debug('Sensor not in hass.data')

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
            "manufacturer": self._attributes.get('meter_manufacturer'),
            "model": self._attributes.get('meter_type'),
        }

    async def async_added_to_hass(self):
        """Register callbacks."""
        async_dispatcher_connect(
            self._hass, SIGNAL_UPDATE_AMS, self._update_callback
        )

    @callback
    def _update_callback(self):
        """Update the state."""
        self._update_properties()
        self.async_schedule_update_ha_state(True)
