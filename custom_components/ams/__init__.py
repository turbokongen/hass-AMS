"""AMS hub platform."""
import logging
import threading
import serial
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from . import han_decode


DOMAIN = 'ams'
AMS_SENSORS = 'ams_sensors'
AMS_DEVICES = []
SIGNAL_UPDATE_AMS = 'update'
SIGNAL_NEW_AMS_SENSOR = 'ams_new_sensor'

_LOGGER = logging.getLogger(__name__)

CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_PARITY = "parity"

DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 2400
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0
FRAME_FLAG = b'\x7e'


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """AMS hub YAML setup."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMS as config entry."""
    hub = AmsHub(hass, entry)
    hass.data[DOMAIN] = hub
    hass.async_add_job(
        hass.config_entries.async_forward_entry_setup(entry, 'sensor')
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].stop_serial_read()
    await hass.config_entries.async_forward_entry_unload(entry, 'sensor')
    return True


class AmsHub():
    """AmsHub wrapper for all sensors."""

    def __init__(self, hass, entry):
        """Initalize the AMS hub."""
        self._hass = hass
        port = entry.data[CONF_SERIAL_PORT]
        parity = entry.data[CONF_PARITY]
        self.sensor_data = {}
        self._hass.data[AMS_SENSORS] = self.data
        self._running = True
        self._ser = serial.Serial(
            port=port,
            baudrate=DEFAULT_BAUDRATE,
            parity=parity,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=DEFAULT_TIMEOUT)
        connection = threading.Thread(target=self.connect, daemon=True)
        connection.start()
        _LOGGER.debug('Finish init of AMS')

    def stop_serial_read(self):
        """Close resources."""
        self._running = False
        self._ser.close()

    def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while self._running:
            data = self._ser.read()
            if data:
                bytelist.extend(data)
                if data == FRAME_FLAG and byte_counter > 1:
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                continue

    def connect(self):
        """Read the data from the port."""
        while self._running:
            try:
                data = self.read_bytes()
                if han_decode.test_valid_data(data):
                    self.sensor_data = han_decode.parse_data(
                        self.sensor_data, data)
                    self._hass.data[AMS_SENSORS] = self.sensor_data
                    self._check_for_new_sensors_and_update(self.sensor_data)
            except serial.serialutil.SerialException:
                pass

    @property
    def data(self):
        """Return sensor data."""
        _LOGGER.debug('sending sensor data')
        return self.sensor_data

    def _check_for_new_sensors_and_update(self, sensor_data):
        """Compare sensor list and update."""
        sensor_list = []
        new_devices = []
        for sensor_name in sensor_data.keys():
            sensor_list.append(sensor_name)
        _LOGGER.debug('sensor_list= %s', sensor_list)
        _LOGGER.debug('AMS_DEVICES= %s', AMS_DEVICES)
        if len(AMS_DEVICES) < len(sensor_list):
            new_devices = list(set(sensor_list) ^ set(AMS_DEVICES))
            for device in new_devices:
                AMS_DEVICES.append(device)
            async_dispatcher_send(self._hass, SIGNAL_NEW_AMS_SENSOR)
            _LOGGER.debug('new_devices= %s', new_devices)
        else:
            _LOGGER.debug('sensors are the same, updating states')
            _LOGGER.debug('hass.data[AMS_SENSORS] = %s',
                          self._hass.data[AMS_SENSORS])
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)
