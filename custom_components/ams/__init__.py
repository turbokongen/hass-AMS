"""AMS hub platform."""
import logging
import threading
from copy import deepcopy

import serial
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (AIDON_METER_SEQ, AMS_DEVICES, CONF_METER_MANUFACTURER,
                    CONF_PARITY, CONF_SERIAL_PORT, DEFAULT_BAUDRATE,
                    DEFAULT_TIMEOUT, DOMAIN, FRAME_FLAG, HOURLY_SENSORS,
                    KAIFA_METER_SEQ, KAMSTRUP_METER_SEQ, SIGNAL_NEW_AMS_SENSOR,
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
        _LOGGER.debug("Connecting to HAN using port %s", port)
        self.meter_manufacturer = entry.data.get(CONF_METER_MANUFACTURER)
        parity = entry.data[CONF_PARITY]
        self.sensor_data = {}
        self._attrs = {}
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
            buf = self._ser.read()
            if buf:
                bytelist.extend(buf)
                if buf == FRAME_FLAG and byte_counter > 1:
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                continue

    @property
    def meter_serial(self):
        return self._attrs["meter_serial"]

    @property
    def meter_type(self):
        return self._attrs["meter_type"]

    def connect(self):
        """Read the data from the port."""
        parser = None

        if self.meter_manufacturer == "auto":
            while parser is None:
                _LOGGER.info("Autodetecting meter manufacturer")
                pkg = self.read_bytes()
                self.meter_manufacturer = self._find_parser(pkg)
                parser = self.meter_manufacturer

        if self.meter_manufacturer == "aidon":
            parser = Aidon
        elif self.meter_manufacturer == "kaifa":
            parser = Kaifa
        elif self.meter_manufacturer == "kamstrup":
            parser = Kamstrup

        while self._running:
            try:
                data = self.read_bytes()
                if parser.test_valid_data(data):
                    _LOGGER.debug("data read from port=%s", data)
                    self.sensor_data, _ = parser.parse_data(self.sensor_data, data)
                    self._check_for_new_sensors_and_update(self.sensor_data)
                else:
                    _LOGGER.debug("failed package: %s", data)
            except serial.serialutil.SerialException:
                pass

    def _find_parser(self, pkg):
        """Helper to detect meter manufacturer."""

        def _test_meter(pkg, meter):
            """Meter tester."""
            match = []
            _LOGGER.debug("Testing for %s", meter)
            for i in range(len(pkg)):
                if pkg[i] == meter[0] and pkg[i:i+len(meter)] == meter:
                    match.append(meter)
            return meter in match
        if _test_meter(pkg, AIDON_METER_SEQ):
            _LOGGER.info("Detected Adion meter")
            return "aidon"
        elif _test_meter(pkg, KAIFA_METER_SEQ):
            _LOGGER.info("Detected Kaifa meter")
            return "kaifa"
        elif _test_meter(pkg, KAMSTRUP_METER_SEQ):
            _LOGGER.info("Detected Kamstrup meter")
            return "kamstrup"
        _LOGGER.warning("No parser detected")

    @property
    def data(self):
        """Return sensor data."""
        return self.sensor_data

    def missing_attrs(self, data=None):
        """Check if we have any missing attrs that we need and set them."""
        if data is None:
            data = self.data

        attrs_to_check = ["meter_serial", "meter_manufacturer", "meter_type"]
        miss_attrs = [i for i in attrs_to_check if i not in self._attrs]
        if miss_attrs:
            cp_sensors_data = deepcopy(data)
            for check in miss_attrs:
                for value in cp_sensors_data.values():
                    v = value.get("attributes", {}).get(check)
                    if v:
                        self._attrs[check] = v
                        break
            del cp_sensors_data
            if len([i for i in attrs_to_check if i not in self._attrs]):
                return True
            else:
                return False
        else:
            return False

    def _check_for_new_sensors_and_update(self, sensor_data):
        """Compare sensor list and update."""
        new_devices = []
        sensors_in_data = set(sensor_data.keys())
        new_devices = sensors_in_data.difference(AMS_DEVICES)

        if len(new_devices):
            # Check that we have all the info we need before the sensors are
            # created, the most importent one is the meter_serial as this is
            # use to create the unique_id
            if self.missing_attrs(sensor_data) is True:
                _LOGGER.debug("Missing some attributes waiting for new read from the serial")
            else:
                _LOGGER.debug(
                    "Got %s new devices from the serial",
                    len(new_devices)
                )
                _LOGGER.debug("DUMP %s", sensor_data)
                async_dispatcher_send(self._hass, SIGNAL_NEW_AMS_SENSOR)
        else:
            # _LOGGER.debug("sensors are the same, updating states")
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)
