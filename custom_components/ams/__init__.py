"""AMS hub platform."""
import logging
import threading

import serial
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (AMS_DEVICES, CONF_METER_MANUFACTURER, CONF_PARITY,
                    CONF_SERIAL_PORT, DEFAULT_BAUDRATE, DEFAULT_TIMEOUT,
                    DOMAIN, FRAME_FLAG, SIGNAL_NEW_AMS_SENSOR,
                    SIGNAL_UPDATE_AMS)
from .parsers import aidon as Aidon
from .parsers import kaifa as Kaifa
from .parsers import kamstrup as Kamstrup

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """AMS hub YAML setup."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMS as config entry."""
    hub = AmsHub(hass, entry)
    hass.data[DOMAIN] = hub
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True


async def async_remove_entry(hass, entry) -> None:
    """Handle removal of an entry."""
    await hass.async_add_executor_job(hass.data[DOMAIN].stop_serial_read)
    return True


class AmsHub:
    """AmsHub wrapper for all sensors."""

    def __init__(self, hass, entry):
        """Initialize the AMS hub."""
        self._hass = hass
        port = (entry.data[CONF_SERIAL_PORT].split(":"))[0]
        _LOGGER.debug("Using port %s", port)
        parity = entry.data[CONF_PARITY]
        self.meter_manufacturer = entry.data[CONF_METER_MANUFACTURER]
        self.sensor_data = {}
        self._running = True
        self._ser = serial.Serial(
            port=port,
            baudrate=DEFAULT_BAUDRATE,
            parity=parity,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=DEFAULT_TIMEOUT,
        )
        self.connection = threading.Thread(target=self.connect, daemon=True)
        self.connection.start()
        _LOGGER.debug("Finish init of AMS")

    def stop_serial_read(self):
        """Close resources."""
        _LOGGER.debug("stop_serial_read")
        self._running = False
        self.connection.join()
        self._ser.close()

    def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while self._running:
            buffer = self._ser.read()
            if buffer:
                bytelist.extend(buffer)
                if buffer == FRAME_FLAG and byte_counter > 1:
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                continue

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
                if parser.test_valid_data(data):
                    _LOGGER.debug("data read from port=%s", data)
                    self.sensor_data = parser.parse_data(self.sensor_data, data)
                    self._check_for_new_sensors_and_update(self.sensor_data)
                else:
                    _LOGGER.debug("failed package: %s", data)
            except serial.serialutil.SerialException:
                pass

    @property
    def data(self):
        """Return sensor data."""
        return self.sensor_data

    def _check_for_new_sensors_and_update(self, sensor_data):
        """Compare sensor list and update."""
        new_devices = []
        sensors_in_data = set(sensor_data.keys())
        new_devices = sensors_in_data.difference(AMS_DEVICES)
        if len(new_devices):
            _LOGGER.debug("Got %s new devices %r", len(new_devices), new_devices)
            async_dispatcher_send(self._hass, SIGNAL_NEW_AMS_SENSOR)
        else:
            _LOGGER.debug("sensors are the same, updating states")
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)
