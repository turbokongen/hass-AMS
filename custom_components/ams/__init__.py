"""AMS hub platform."""
import asyncio
import logging
import threading
from copy import deepcopy

import homeassistant.helpers.config_validation as cv
import serial
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.core_config import Config
from homeassistant.helpers.dispatcher import async_dispatcher_send
from custom_components.ams.parsers import aidon as Aidon
from custom_components.ams.parsers import field_type
from custom_components.ams.parsers import kaifa as Kaifa
from custom_components.ams.parsers import kaifa_se as Kaifa_se
from custom_components.ams.parsers import kamstrup as Kamstrup
from custom_components.ams.parsers import aidon_se as Aidon_se
from custom_components.ams.const import (
    AMS_DEVICES,
    AIDON_METER_SEQ,
    AIDON_SE_METER_SEQ_1PH,
    AIDON_SE_METER_SEQ_3PH,
    CONF_BAUDRATE,
    CONF_METER_MANUFACTURER,
    CONF_OSS_BRIKKEN,
    CONF_KAMSTRUP_6841138_SCALE,
    CONF_PARITY,
    CONF_PROTOCOL,
    CONF_SERIAL_PORT,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_METER_MANUFACTURER,
    DEFAULT_OSS_BRIKKEN,
    DEFAULT_PARITY,
    DEFAULT_SERIAL_PORT,
    DEFAULT_TIMEOUT,
    DOMAIN,
    HAN_METER_MANUFACTURER,
    HAN_METER_SERIAL,
    HAN_METER_TYPE,
    KAIFA_SE_METER_SEQ,
    KAMSTRUP_METER_SEQ,
    NETWORK,
    SENSOR_ATTR,
    SERIAL,
    SIGNAL_NEW_AMS_SENSOR,
    SIGNAL_UPDATE_AMS,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

SERIAL_SCHEMA = {vol.Required(CONF_SERIAL_PORT, default=DEFAULT_SERIAL_PORT)}
NETWORK_SCHEMA = {vol.Required(CONF_TCP_HOST), vol.Required(CONF_TCP_PORT)}
PROTOCOL_SCHEMA = {
    vol.Required(SERIAL): SERIAL_SCHEMA,
    vol.Required(NETWORK): NETWORK_SCHEMA,
}
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_PROTOCOL, default=SERIAL): vol.In(
                    [NETWORK, SERIAL]),
                vol.Optional(CONF_TCP_HOST): str,
                vol.Optional(CONF_TCP_PORT): vol.All(
                    vol.Coerce(int), vol.Range(0, 65535)
                ),
                vol.Optional(CONF_SERIAL_PORT): str,
                vol.Optional(CONF_PARITY, default=DEFAULT_PARITY): cv.string,
                vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.All(
                    vol.Coerce(int), vol.Range(0, 256000)
                ),
                vol.Optional(
                    CONF_METER_MANUFACTURER, default=DEFAULT_METER_MANUFACTURER
                ): cv.string,
                vol.Optional(
                    CONF_OSS_BRIKKEN, default=DEFAULT_OSS_BRIKKEN
                ): vol.All(vol.Any(int, bool), vol.Coerce(bool))
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def _setup(hass, config):
    """Setup helper for the component."""
    if DOMAIN not in hass.data:
        hub = AmsHub(hass, config)
        hass.data[DOMAIN] = hub


async def async_setup(hass: HomeAssistant, config: Config):
    """AMS hub YAML setup."""
    if config.get(DOMAIN) is None:
        _LOGGER.info("No YAML config available, using config_entries")
        return True
    _setup(hass, config[DOMAIN])
    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=config[DOMAIN]
            )
        )
    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry):
    """Apply the compatibility setting without restarting the serial reader."""
    hub = hass.data.get(DOMAIN)
    if hub is not None:
        hub.kamstrup_6841138_scale = entry.options.get(
            CONF_KAMSTRUP_6841138_SCALE, False
        )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up AMS as config entry."""
    config = dict(entry.data)
    config.update(entry.options)
    await hass.async_add_executor_job(_setup, hass, config)
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True


async def async_remove_entry(hass, entry):  # pylint: disable=unused-argument
    """Handle removal of an entry."""
    await hass.async_add_executor_job(hass.data[DOMAIN].stop_serial_read)
    return True


class AmsHub:
    """AmsHub wrapper for all sensors."""

    def __init__(self, hass, entry):
        """Initialize the AMS hub."""
        _LOGGER.debug("config entry = %s", entry)
        self._hass = hass
        self.meter_manufacturer = entry.get(CONF_METER_MANUFACTURER)
        self.kamstrup_6841138_scale = entry.get(
            CONF_KAMSTRUP_6841138_SCALE, False
        )
        self.sensor_data = {}
        self._attrs = {}
        self._running = True
        self.oss = entry.get(CONF_OSS_BRIKKEN, False)
        if entry.get(CONF_PROTOCOL) == SERIAL:
            port = entry.get(CONF_SERIAL_PORT)

            _LOGGER.debug("Connecting to HAN using serialport %s", port)
            try:
                self._ser = serial.serial_for_url(
                    port,
                    baudrate=entry.get(CONF_BAUDRATE),
                    parity=entry.get(CONF_PARITY),
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=DEFAULT_TIMEOUT,
                )
            except serial.serialutil.SerialException as ex:
                _LOGGER.warning("Serial error: %", ex)
        if entry.get(CONF_PROTOCOL) == NETWORK:
            port = f"socket://{entry.get(CONF_TCP_HOST)}" \
                   f":{entry.get(CONF_TCP_PORT)}"
            _LOGGER.debug("Connecting to HAN using TCP/IP %s", port)
            try:
                self._ser = serial.serial_for_url(
                    port,
                    baudrate=entry.get(CONF_BAUDRATE, DEFAULT_BAUDRATE),
                    parity=entry.get(CONF_PARITY, DEFAULT_PARITY),
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=DEFAULT_TIMEOUT,
                )
            except serial.serialutil.SerialException as ex:
                _LOGGER.warning("Serial error: %s", ex)
        self.connection = threading.Thread(target=self.connect, daemon=True)
        self.connection.start()
        _LOGGER.debug("Finish init of AMS")

    def stop_serial_read(self):
        """Close resources."""
        _LOGGER.debug("stop_serial_read")
        self._running = False
        self.connection.join()
        self._ser.close()

    @staticmethod
    def _normalize_oss_frame(frame, expected_size):
        """Recover OSS-inserted CR bytes only if Aidon CRC stays valid."""
        if len(frame) <= expected_size or frame[-1] != 0x7E:
            return None
        # Only apply this workaround to the documented Aidon DLMS strings.
        if frame.count(b"\x0d\x0a") != len(frame) - expected_size:
            return None
        normalized = frame.replace(b"\x0d\x0a", b"\x0a")
        if len(normalized) != expected_size:
            return None
        if not Aidon.test_valid_data(list(normalized), False):
            return None
        return list(normalized)

    def read_packet(self):
        """Read one HDLC frame, including OSS-inserted CR bytes."""
        frame = bytearray()
        expected_size = None
        # The documented OSS corruption adds 3 bytes. Limit recovery to 8.
        max_extra = 8
        while self._running:
            buf = self._ser.read()
            if not buf:
                if frame:
                    _LOGGER.debug("Timeout waiting for HDLC frame")
                frame.clear()
                expected_size = None
                continue
            for value in buf:
                if not frame:
                    if value == 0x7E:
                        frame.append(value)
                    continue
                frame.append(value)
                if len(frame) == 3:
                    expected_size = (((frame[1] & 0x0F) << 8)
                                     | frame[2]) + 2
                    if expected_size < 4 or expected_size > 583:
                        frame.clear()
                        expected_size = None
                        continue
                if expected_size is None:
                    continue
                if len(frame) == expected_size and value == 0x7E:
                    return list(frame)
                if len(frame) > expected_size and value == 0x7E:
                    if getattr(self, "meter_manufacturer", "aidon") in (
                        "aidon", "auto"
                    ):
                        recovered = self._normalize_oss_frame(
                            bytes(frame), expected_size
                        )
                        if recovered is not None:
                            return recovered
                    _LOGGER.debug("Rejecting invalid extended HDLC frame")
                    frame.clear()
                    expected_size = None
                    continue
                if len(frame) >= expected_size + max_extra:
                    _LOGGER.debug("HDLC frame exceeded recovery limit")
                    frame.clear()
                    expected_size = None

    @property
    def meter_serial(self):
        """The electrical meter's serial number"""
        return self._attrs[HAN_METER_SERIAL]

    @property
    def meter_type(self):
        """The electrical meter's type"""

        return self._attrs[HAN_METER_TYPE]

    def connect(self):  # pylint: disable=too-many-branches
        """Read the data from the port."""
        parser = None
        detect_pkg = None  # This is needed to push the package used for
        # detecting the meter straight to the parser. If not, users will get
        # unknown state class None for energy sensors at startup.
        if self.meter_manufacturer == "auto":
            while parser is None and self._running is True:
                _LOGGER.info("Autodetecting meter manufacturer")
                detect_pkg = self.read_packet()
                self.meter_manufacturer = self._find_parser(detect_pkg)
                parser = self.meter_manufacturer

        swedish = None
        if self.meter_manufacturer == "aidon":
            parser = Aidon
        elif self.meter_manufacturer == "aidon_se":
            parser = Aidon_se
        elif self.meter_manufacturer == "kaifa":
            if detect_pkg and field_type(
                    fields=detect_pkg[62:70], enc=chr) == "MA304H4D":
                swedish = True
                parser = Kaifa
            else:
                parser = Kaifa
        elif self.meter_manufacturer == "kaifa_se":
            parser = Kaifa_se
        elif self.meter_manufacturer == "kamstrup":
            parser = Kamstrup

        while self._running:
            try:
                if detect_pkg:
                    data = detect_pkg
                else:
                    data = self.read_packet()

                if parser.test_valid_data(
                    data, False if parser is Aidon else self.oss
                ):
                    _LOGGER.debug("data read from port=%s", data)
                    if swedish:
                        self.sensor_data, _ = parser.parse_data(
                            self.sensor_data, data, swedish
                        )
                    elif parser is Kamstrup:
                        self.sensor_data, _ = parser.parse_data(
                            self.sensor_data, data,
                            kamstrup_6841138_scale=(
                                self.kamstrup_6841138_scale
                            ),
                        )
                    else:
                        self.sensor_data, _ = parser.parse_data(
                            self.sensor_data, data
                        )

                    self._check_for_new_sensors_and_update(self.sensor_data)
                else:
                    _LOGGER.debug("failed package: %s", data)
                if detect_pkg:
                    detect_pkg = None
            except serial.serialutil.SerialException:
                pass

    @classmethod
    def _find_parser(cls, pkg):
        """Helper to detect meter manufacturer."""

        def _test_meter(test_pkg, meter):
            """Meter tester."""
            match = []
            _LOGGER.debug("Testing for %s", meter)
            if test_pkg is None:
                return None
            for i, _ in enumerate(test_pkg):
                if test_pkg[i] == meter[0] and (
                    test_pkg[i:(i + len(meter))] == meter
                ):
                    match.append(meter)
            return meter in match

        if _test_meter(pkg, AIDON_METER_SEQ):
            _LOGGER.info("Detected Aidon meter")
            return "aidon"
        if _test_meter(pkg, AIDON_SE_METER_SEQ_3PH):
            _LOGGER.info("Detected Swedish Aidon meter")
            return "aidon_se"
        if _test_meter(pkg, AIDON_SE_METER_SEQ_1PH):
            _LOGGER.info("Detected Swedish Aidon meter")
            return "aidon_se"
        if _test_meter(pkg, KAIFA_SE_METER_SEQ):
            if field_type(fields=pkg[62:70], enc=chr) == "MA304H4D":
                _LOGGER.info("Detected Swedish Kaifa meter MA304H4D")
                return "kaifa"
            elif _test_meter(pkg, [1, 0, 1, 7, 0, 255]):
                _LOGGER.info("Detected Swedish kaifa meter")
                return "kaifa_se"
            else:
                _LOGGER.info("Detected Kaifa meter")
                return "kaifa"
        if _test_meter(pkg, KAMSTRUP_METER_SEQ):
            _LOGGER.info("Detected Kamstrup meter")
            return "kamstrup"

        _LOGGER.warning("No parser detected")
        _LOGGER.debug("Meter detection package dump: %s", pkg)

    @property
    def data(self):
        """Return sensor data."""
        return self.sensor_data

    def missing_attrs(self, data=None):
        """Check if we have any missing attrs that we need and set them."""
        if data is None:
            data = self.data

        attrs_to_check = [HAN_METER_SERIAL,
                          HAN_METER_MANUFACTURER, HAN_METER_TYPE]
        imp_attrs = [i for i in attrs_to_check if i not in self._attrs]
        if imp_attrs:
            cp_sensors_data = deepcopy(data)
            for check in imp_attrs:
                for value in cp_sensors_data.values():
                    val = value.get(SENSOR_ATTR, {}).get(check)
                    if val:
                        self._attrs[check] = val
                        break
            del cp_sensors_data
            miss_attrs = [i for i in attrs_to_check if i not in self._attrs]
            _LOGGER.debug(
                "miss_attrs=%s", (
                    [i for i in attrs_to_check if i not in self._attrs])
            )
            if miss_attrs:
                _LOGGER.debug("We miss some attributes: %s", miss_attrs)
                return True
        return False

    def _check_for_new_sensors_and_update(self, sensor_data):
        """Compare sensor list and update."""
        new_devices = []
        sensors_in_data = set(sensor_data.keys())
        new_devices = sensors_in_data.difference(AMS_DEVICES)

        if new_devices:
            # Check that we have all the info we need before the sensors are
            # created, the most important one is the meter_serial as this is
            # use to create the unique_id
            if self.missing_attrs(sensor_data) is True:
                _LOGGER.debug(
                    "Missing some attributes waiting for new read from the"
                    " serial"
                )
            else:
                _LOGGER.debug("Got %s new devices from the serial",
                              len(new_devices))
                _LOGGER.debug("DUMP %s", sensor_data)
                asyncio.run_coroutine_threadsafe(self._signal_new_sensor(),
                                                 self._hass.loop).result()
        else:
            # _LOGGER.debug("sensors are the same, updating states")
            asyncio.run_coroutine_threadsafe(self._signal_update_sensors(),
                                             self._hass.loop).result()

    async def _signal_new_sensor(self) -> None:
        async_dispatcher_send(self._hass, SIGNAL_NEW_AMS_SENSOR)

    async def _signal_update_sensors(self) -> None:
        async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)
