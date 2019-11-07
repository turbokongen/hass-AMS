"""AMS hub platform."""
import logging
import serial
import threading
from time import sleep
from pprint import pprint
from homeassistant.helpers.dispatcher import async_dispatcher_send

import voluptuous as vol
from . import han_decode

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_VALUE_TEMPLATE, EVENT_HOMEASSISTANT_STOP, EVENT_HOMEASSISTANT_START
from homeassistant.helpers.entity import Entity

DOMAIN = 'ams'
AMS_SENSORS = 'ams_sensors'
AMS_DEVICES = []
SIGNAL_UPDATE_AMS = 'update'

_LOGGER = logging.getLogger(__name__)

CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_PARITY = "parity"

DEFAULT_NAME = "AMS Sensor"
DEFAULT_BAUDRATE = 2400
DEFAULT_PARITY = serial.PARITY_NONE
DEFAULT_TIMEOUT = 0
FRAME_FLAG = b'\x7e'



CONFIG_SCHEMA = vol.Schema(
    { 
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_SERIAL_PORT): cv.string,
                vol.Optional(CONF_PARITY, default=DEFAULT_PARITY): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """AMS hub."""
    conf_ams = config[DOMAIN]
    port = conf_ams.get(CONF_SERIAL_PORT)
    parity = conf_ams.get(CONF_PARITY)
    ser = serial.Serial(
            port=port,
            baudrate=DEFAULT_BAUDRATE,
            parity=parity,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=DEFAULT_TIMEOUT)
    hub = AmsHub(hass, port, parity, ser)
    hass.data[DOMAIN] = hub
    connection = threading.Thread(target=hub.connect)
    
    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_serial_read(ser))
    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, connection.start())
    
    return True

def stop_serial_read(ser):
    """Close resources."""
    ser.close()

class AmsHub(Entity):
    """AmsHub wrapper for all sensors."""
    
    def __init__(self, hass, port, parity, ser):
        """Initalize the AMS hub."""

        self._hass = hass
        self._port = port
        self._parity = parity
        self._ser = ser
        self.sensor_data = {}
        self._hass.data[AMS_SENSORS] = self.data

    def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while True:
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
      self._ser.open()
      while True:
          try:
              data = self.read_bytes()
              if han_decode.test_valid_data(data):
                  self.sensor_data = han_decode.parse_data(self.sensor_data, data)
                  self._hass.data[AMS_SENSORS] = self.sensor_data
                  self._check_for_new_sensors_and_update(self.sensor_data)
#                  _LOGGER.debug('self.sensor_data is updated, %s', self.sensor_data)
          except serial.serialutil.SerialException:
              pass

    @property
    def data(self):
        """Contains the sensor data."""
        _LOGGER.debug('sending sensor data')
        return self.sensor_data

    def _check_for_new_sensors_and_update(self, sensor_data):
        """Compare existing sensor list to see if a new sensor needs to be added."""
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
            _LOGGER.debug('new_devices= %s', new_devices)
            self._hass.helpers.discovery.load_platform('sensor', DOMAIN, self._hass.data[AMS_SENSORS], self._ser)
        else:
            _LOGGER.debug('sensors are the same, updating states')
            _LOGGER.debug('hass.data[AMS_SENSORS] = %s', self._hass.data[AMS_SENSORS])
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)

