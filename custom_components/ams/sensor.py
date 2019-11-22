"""Support for reading data from a serial port."""
import logging
import voluptuous as vol
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import callback
import custom_components.ams as amshub

DOMAIN = 'ams'
AMS_SENSORS = 'ams_sensors'
SIGNAL_UPDATE_AMS = 'update'

_LOGGER = logging.getLogger(__name__)

CONF_PORT = "port"
CONF_PARITY = "parity"

BAUDRATE = 2400
DEFAULT_PARITY = 'N'
DEFAULT_PORT = '/dev/ttyUSB0'
TIMEOUT = 0
FRAME_FLAG = b'\x7e'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.string,
    vol.Optional(CONF_PARITY, default=DEFAULT_PARITY):
        cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Serial sensor platform."""
    sensor_states = {}
    sensors = []
    data = hass.data[amshub.AMS_SENSORS]
    _LOGGER.debug('HUB= %s', hass.data[DOMAIN].data)
    _LOGGER.debug('AMS_SENSORS= %s', hass.data[AMS_SENSORS])

    for sensor_name in data:
        sensor_states = {
            'name': sensor_name,
            'state': data[sensor_name].get('state'),
            'attributes': data[sensor_name].get('attributes')
            }
        sensors.append(AmsSensor(hass, sensor_states))
        _LOGGER.debug('sensors = %s', sensors)
        _LOGGER.debug('sensor_states: %s', sensor_states)

    add_devices(sensors)


class AmsSensor(Entity):
    """Representation of a Serial sensor."""

    def __init__(self, hass, sensor_states):
        """Initialize the Serial sensor."""
        self.ams = hass.data[DOMAIN]
        self._hass = hass
        self._name = sensor_states.get('name')
        self._unique_id = '{serial}-{name}'.format(
            serial=sensor_states['attributes'].get('meter_serial'),
            name=self._name)
        self._state = None
        self._attributes = None
        _LOGGER.debug('%s ', sensor_states)
        _LOGGER.debug('%s ', sensor_states.get('state'))
        _LOGGER.debug('%s ', sensor_states.get('attributes'))
        _LOGGER.debug('%s ', dir(Entity))
        self._update_properties()

    def _update_properties(self):
        """Update all portions of sensor."""
        try:
            self._state = self.ams.data[self._name].get('state')
            self._attributes = self.ams.data[self._name].get('attributes')
            _LOGGER.debug('updating sensor %s', self._name)
        except KeyError:
            _LOGGER.debug('Sensor not in hass.data')

    @property
    def unique_id(self):
        """Return the uniqe id of the sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
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
