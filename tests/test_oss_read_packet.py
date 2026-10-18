"""Regression tests for issue #112: complete OSS/TCP HDLC frame reception.

Uses the actual frame fixtures stored in tests/test_oss_tcp_definition.py.
Run: python -m pytest tests/test_issue_112_read_packet.py -v --tb=short
"""


import pytest

from custom_components.ams import AmsHub
from custom_components.ams.parsers import aidon
from tests.test_oss_tcp_definition import LONG_OSS, SHORT


class FakeSerial:
    """Deliver TCP payload one byte at a time, like serial.read(size=1)."""

    def __init__(self, payload):
        self.data = iter(bytes(payload))
        self.exhausted = False
        self.hub = None

    def read(self, size=1):
        assert size == 1
        try:
            return bytes((next(self.data),))
        except StopIteration:
            self.exhausted = True
            # Prevent infinite waits if the receiver has discarded the frame.
            self.hub._running = False
            return b""


def receive_once(payload, oss):
    """Call the production receiver using a deterministic byte stream."""
    hub = AmsHub.__new__(AmsHub)
    fake = FakeSerial(payload)
    fake.hub = hub
    hub._ser = fake
    hub._running = True
    hub.oss = oss
    return hub.read_packet()


@pytest.mark.parametrize("oss", [False, True])
def test_short_hdlc_frame_survives_tcp_receiver(oss):
    """Normal 44-byte packets must not change, in either OSS mode."""
    packet = receive_once(SHORT, oss)
    assert packet == list(SHORT)
    assert aidon.test_valid_data(packet, False)


def test_issue_112_plain_tcp_reconstructs_valid_hdlc_frame():
    """The long OSS frame should be normalized before its CRC is checked.

    Expected to FAIL against the current receiver, proving the missing step.
    """
    packet = receive_once(LONG_OSS, oss=False)
    assert packet is not None, "read_packet discarded the 272-byte frame"
    assert packet[0] == 0x7E and packet[-1] == 0x7E
    assert len(packet) == 269
    assert aidon.test_valid_data(packet, False)


def test_issue_112_oss_tcp_reconstructs_valid_hdlc_frame():
    """Enabling OSS must not return a premature, unchecked 269-byte prefix.

    Expected to FAIL against current code (it returns before the end flag).
    """
    packet = receive_once(LONG_OSS, oss=True)
    assert packet is not None
    assert packet[0] == 0x7E and packet[-1] == 0x7E
    assert len(packet) == 269
    assert aidon.test_valid_data(packet, False)


def test_unchanged_short_frame_corruption_is_rejected_by_crc():
    """Reception is separate from CRC validation; bad bytes remain invalid."""
    data = bytearray(SHORT)
    data[20] ^= 0x01
    packet = receive_once(data, oss=False)
    assert packet == list(data)
    assert not aidon.test_valid_data(packet, False)
