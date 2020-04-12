"""AMS hub platform."""
import asyncio
import logging
from copy import deepcopy

import serial_asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (AMS_DEVICES, CONF_METER_MANUFACTURER, CONF_SERIAL_PORT,
                    DEFAULT_BAUDRATE, DOMAIN, FRAME_FLAG,
                    SIGNAL_NEW_AMS_SENSOR, SIGNAL_UPDATE_AMS)
from .parsers import auto_detect_parser

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """AMS hub YAML setup."""
    hass.data[DOMAIN] = {}

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMS as config entry."""
    hub = AmsHub(hass, entry)
    hass.data[DOMAIN] = hub
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, hub.stop_serial_read())
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry."""
    return True


class AmsHub:
    """AmsHub wrapper for all sensors."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the AMS hub."""
        self._hass = hass
        self.meter_manufacturer = entry.data.get(CONF_METER_MANUFACTURER)
        self.port = (entry.data[CONF_SERIAL_PORT].split(":"))[0]
        self.sensor_data = {}
        self._attrs = {}
        self._running = True
        self._ser = None
        self._runner = hass.loop.create_task(self.aio_run())
        _LOGGER.debug("Connecting to HAN using port %s", self.port)
        _LOGGER.debug("DUMP entry %s", entry.data)
        _LOGGER.debug("Finish init of AMS")

    async def create_aio_serial(self):
        """Create the streamreader."""
        _LOGGER.debug("Setting up serial.")
        if self._ser is None:
            self._ser, _ = await serial_asyncio.open_serial_connection(
                url=self.port,
                baudrate=DEFAULT_BAUDRATE,
            )
            return self._ser

    async def aio_run(self):
        """Start the serial connection to the han port and start reading data."""
        while self._ser is None:
            await self.create_aio_serial()
            await asyncio.sleep(1)

        # Setup the parser
        if self.meter_manufacturer == "auto":
            _LOGGER.debug("Detecting parser")
            while self.meter_manufacturer == "auto":
                pkg = await self.read_bytes()
                parser = auto_detect_parser(pkg)
                if parser is not None:
                    self.meter_manufacturer = parser.meter_manufacturer
        else:
            parser = auto_detect_parser(self.meter_manufacturer)

        _LOGGER.debug("Using parser %s", self.meter_manufacturer)

        try:
            while self._running:
                data = await self.read_bytes()
                if parser.test_valid_data(data):
                    _LOGGER.debug("data read from port=%s", data)
                    self.sensor_data, _ = parser.parse_data(self.sensor_data, data)
                    self._check_for_new_sensors_and_update(self.sensor_data)
                else:
                    _LOGGER.debug("failed package: %s", data)
        except Exception as e:
            _LOGGER.exception("Some crap happend %s", e)

    @property
    def meter_serial(self):
        return self._attrs["meter_serial"]

    @property
    def meter_type(self):
        return self._attrs["meter_type"]

    async def stop_serial_read(self):
        """Stop the task that reads the serial."""
        self._running = False
        self._runner.cancel()
        self._ser.close()
        self._ser = None
        self._runner = None

    async def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while self._running:
            # is one the correct alternativ here?
            # the parser excepts one char at the time
            # but it might be less cpu usage to read more at the same time.
            buf = await self._ser.read(1)
            # Force yield to the event loop.
            await asyncio.sleep(0)
            if buf:
                bytelist.extend(buf)
                if buf == FRAME_FLAG and byte_counter > 1:
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                continue

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
