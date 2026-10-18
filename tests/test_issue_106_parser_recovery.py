"""Regression tests for #106: malformed Aidon packet must not kill reader."""

from unittest.mock import patch

from custom_components.ams import AmsHub
from custom_components.ams.const import HAN_CURRENT_L1, SENSOR_OBIS_MAP
from custom_components.ams.parsers import aidon
from .common_test_data import TestData


def _incomplete_current_packet():
    """Place a current OBIS signature at the end, without its value."""
    pkt = list(TestData.AIDON_HOURLY)
    item = list(SENSOR_OBIS_MAP[HAN_CURRENT_L1][0])
    # Preserve the earlier metadata, but append a truncated signed-16 field.
    # The last three bytes are checksum and HDLC end flag, not value bytes.
    return pkt[:-3] + item + [16] + pkt[-3:]


def test_truncated_signed_current_does_not_raise_indexerror():
    """A truncated signed current field is skipped, not decoded."""
    pkt = _incomplete_current_packet()
    # We deliberately invoke the parser directly: this is a bounds test,
    # not a valid-CRC transport test.
    result, _ = aidon.parse_data({}, pkt)
    assert isinstance(result, dict)


def test_connect_continues_after_parser_indexerror():
    """A malformed validated packet must not terminate the read loop."""
    hub = object.__new__(AmsHub)
    hub._running = True
    hub.meter_manufacturer = "aidon"
    hub.oss = False
    hub.sensor_data = {}
    packets = [[126, 1], [126, 2]]
    calls = []

    def fake_read():
        if not packets:
            hub._running = False
            return None
        return packets.pop(0)

    def fake_parse(stored, data):
        calls.append(data)
        if len(calls) == 1:
            raise IndexError("deliberate malformed OBIS field")
        hub._running = False
        return stored, {}

    hub.read_packet = fake_read
    hub._check_for_new_sensors_and_update = lambda data: None

    with patch.object(aidon, "test_valid_data", return_value=True), \
            patch.object(aidon, "parse_data", side_effect=fake_parse):
        hub.connect()

    assert calls == [[126, 1], [126, 2]]
