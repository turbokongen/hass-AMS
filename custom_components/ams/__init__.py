"""AMS hub platform."""

import threading
import serial
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from memory_profiler import profile
from .parsers import kaifa as Kaifa
from .parsers import kamstrup as Kamstrup
from .parsers import aidon as Aidon
from .const import (
    _LOGGER,
    AMS_DEVICES,
    AMS_SENSORS,
    CONF_SERIAL_PORT,
    CONF_PARITY,
    CONF_METER_MANUFACTURER,
    DEFAULT_BAUDRATE,
    DEFAULT_TIMEOUT,
    DOMAIN,
    FRAME_FLAG,
    SIGNAL_NEW_AMS_SENSOR,
    SIGNAL_UPDATE_AMS
)


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
    await hass.config_entries.async_forward_entry_unload(entry, 'sensor')
    return True


async def async_remove_entry(hass, entry) -> None:
    """Handle removal of an entry."""
    result = await hass.async_add_executor_job(hass.data[DOMAIN].stop_serial_read)
    return True


class AmsHub:
    """AmsHub wrapper for all sensors."""

    @profile(precision=6)
    def __init__(self, hass, entry):
        """Initialize the AMS hub."""
        self._hass = hass
        port = entry.data[CONF_SERIAL_PORT]
        parity = entry.data[CONF_PARITY]
        self.meter_manufacturer = entry.data[CONF_METER_MANUFACTURER]
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
        self.connection = threading.Thread(target=self.connect, daemon=True)
        self.connection.start()
        _LOGGER.debug('Finish init of AMS')

    @profile(precision=6)
    def stop_serial_read(self):
        """Close resources."""
        _LOGGER.debug("stop_serial_read")
        self._running = False
        self._ser.close()
        self.connection.join()

    @profile(precision=6)
    def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while self._running:
            data = self._ser.read()
            if data:
                bytelist.extend(data)
                if data == FRAME_FLAG and byte_counter > 1:
                    self._ser.flushInput()
                    _LOGGER.debug('buffer: %s', self._ser.inWaiting())
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                continue

    @profile(precision=6)
    def connect(self):
        """Read the data from the port."""
        if self.meter_manufacturer == "kaifa":
            parser = Kaifa
        elif self.meter_manufacturer == "aidon":
            parser = Aidon
        else:
            parser = Kamstrup
        while self._running:
            try:
                data = self.read_bytes()
                _LOGGER.debug('reading data = %s', data)
                if parser.test_valid_data(data):
                    _LOGGER.debug(data)
                    self.sensor_data = parser.parse_data(
                        self.sensor_data, data)
                    self._hass.data[AMS_SENSORS] = self.sensor_data
                    self._check_for_new_sensors_and_update(self.sensor_data)
                else:
                    self._ser.flushInput()
                    _LOGGER.debug("failed package: %s", data)

            except serial.serialutil.SerialException:
                pass

    @property
    def data(self):
        """Return sensor data."""
        _LOGGER.debug('sending sensor data')
        return self.sensor_data

    @profile(precision=6)
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
