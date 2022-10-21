"""AMS hub platform."""
import logging
import threading
from copy import deepcopy

import homeassistant.helpers.config_validation as cv
import serial
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, SOURCE_IMPORT
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send
from custom_components.ams.parsers import aidon as Aidon
from custom_components.ams.parsers import byte_decode, field_type
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
    CONF_PARITY,
    CONF_PROTOCOL,
    CONF_PROTOCOL_TYPE,
    CONF_SERIAL_PORT,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    DEFAULT_BAUDRATE,
    DEFAULT_METER_MANUFACTURER,
    DEFAULT_PARITY,
    DEFAULT_SERIAL_PORT,
    DEFAULT_TIMEOUT,
    DOMAIN,
    FRAME_FLAG,
    HAN_METER_MANUFACTURER,
    HAN_METER_SERIAL,
    HAN_METER_TYPE,
    KAIFA_METER_SEQ,
    KAIFA_SE_METER_SEQ,
    KAMSTRUP_METER_SEQ,
    METER_TYPE,
    NETWORK,
    SENSOR_ATTR,
    SERIAL,
    SIGNAL_NEW_AMS_SENSOR,
    SIGNAL_UPDATE_AMS,
    UNKNOWN_METER,
)

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
                vol.Required(CONF_PROTOCOL, default=SERIAL): vol.In([NETWORK, SERIAL]),
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


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up AMS as config entry."""
    _setup(hass, entry.data)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
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
        self.sensor_data = {}
        self._attrs = {}
        self._running = True
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
            port = f"socket://{entry.get(CONF_TCP_HOST)}:{entry.get(CONF_TCP_PORT)}"
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

    def read_packet(self):
        """Read raw data for one packet from serial port."""
        byte_counter = 0
        bytelist = []
        frame_started = False
        packet_size = -1
        while self._running:
            buf = self._ser.read()

            if buf:
                if buf == FRAME_FLAG and not frame_started:
                    # Purge data until FRAME_FLAG is received
                    frame_started = True
                    byte_counter = 0
                    bytelist = []
                if frame_started:
                    # Build packet
                    bytelist.extend(buf)
                    byte_counter = byte_counter + 1
                    if byte_counter == 3:
                        # Calculate size after FRAME_FLAG + 2 bytes are
                        # received
                        packet_size = ((bytelist[1] & 0x0F) << 8 | bytelist[2]) + 2
                    if byte_counter == packet_size:
                        # If we have built a packet equal to packet size
                        if buf == FRAME_FLAG:
                            # Valid packet as last byte is FRAME_FLAG
                            return bytelist
                        else:
                            # Not valid packet. Flush what we have built so
                            # far.
                            _LOGGER.debug(
                                "Not a valid packet. Start over "
                                "again. byte_counter=%s, "
                                "frame_started=%s, "
                                "packet_size=%s, DUMP: %s",
                                byte_counter,
                                frame_started,
                                packet_size,
                                bytelist,
                            )
                            bytelist = []
                            byte_counter = 0
                            frame_started = False
                            packet_size = -1
            else:
                if frame_started:
                    _LOGGER.debug(
                        "Timeout waiting for end of packet. Flush "
                        " current packet. byte_counter=%s, "
                        "frame_started=%s, package_size=%s, "
                        "DUMP: %s",
                        byte_counter,
                        frame_started,
                        packet_size,
                        bytelist,
                    )
                    frame_started = False
                    byte_counter = 0
                    bytelist = []

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
            while parser is None:
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
            if detect_pkg and field_type(fields=detect_pkg[62:70], enc=chr) == "MA304H4D":
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
                if parser.test_valid_data(data):
                    _LOGGER.debug("data read from port=%s", data)
                    if swedish:
                        self.sensor_data, _ = parser.parse_data(
                            self.sensor_data, data, swedish
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
        if _test_meter(pkg, KAIFA_METER_SEQ):
            _LOGGER.info("Detected Kaifa meter")
            return "kaifa"
        if _test_meter(pkg, KAIFA_SE_METER_SEQ):
            if field_type(fields=pkg[62:70], enc=chr) == "MA304H4D":
                _LOGGER.info("Detected Swedish Kaifa meter MA304H4D")
                return "kaifa"
            else:
                _LOGGER.info("Detected Swedish Kaifa meter")
                return "kaifa_se"
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

        attrs_to_check = [HAN_METER_SERIAL, HAN_METER_MANUFACTURER, HAN_METER_TYPE]
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
                "miss_attrs=%s", ([i for i in attrs_to_check if i not in self._attrs])
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
                    "Missing some attributes waiting for new read from the" " serial"
                )
            else:
                _LOGGER.debug("Got %s new devices from the serial", len(new_devices))
                _LOGGER.debug("DUMP %s", sensor_data)
                async_dispatcher_send(self._hass, SIGNAL_NEW_AMS_SENSOR)
        else:
            # _LOGGER.debug("sensors are the same, updating states")
            async_dispatcher_send(self._hass, SIGNAL_UPDATE_AMS)
