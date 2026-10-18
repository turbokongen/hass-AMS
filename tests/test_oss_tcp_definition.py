"""Regression tests for GitHub issue #112: Aidon over ser2net / OSS.

The long-frame fixture is transcribed from the issue's hexdump.
No real meter, network socket, or serial port is required.
"""
from unittest.mock import MagicMock, patch

import pytest

from custom_components.ams import AmsHub
from custom_components.ams.const import (
    CONF_BAUDRATE,
    CONF_METER_MANUFACTURER,
    CONF_OSS_BRIKKEN,
    CONF_PARITY,
    CONF_PROTOCOL,
    CONF_TCP_HOST,
    CONF_TCP_PORT,
    NETWORK,
)
from custom_components.ams.parsers import aidon

# Short frame from the issue; declared HDLC length = 42, total = 44.
SHORT = bytes([
    126, 160, 42, 65, 8, 131, 19, 4, 19, 230, 231, 0,
    15, 64, 0, 0, 0, 0, 1, 1, 2, 3, 9, 6,
    1, 0, 1, 7, 0, 255, 6, 0, 0, 28, 116,
    2, 2, 15, 0, 22, 27, 142, 57, 126,
])

# Entire first long frame from TrondKjeldas's hexdump in issue #112.
# It contains three anomalous 0D 0A sequences at the string fields.

LONG_OSS = bytes.fromhex(
    "7e a1 0b 41 08 83 13 fa 7c e6 e7 00 0f "
    "40 00 00 00 00 01 0c 02 02 09 06 01 01 00 02 81 "
    "ff 0d 0a 0b 41 49 44 4f 4e 5f 56 30 30 30 31 02 "
    "02 09 06 00 00 60 01 00 ff 0d 0a 10 37 33 35 39 "
    "39 39 32 39 32 30 38 30 38 38 33 30 02 02 09 06 "
    "00 00 60 01 07 ff 0d 0a 04 36 35 32 35 02 03 09 "
    "06 01 00 01 07 00 ff 06 00 00 1e ea 02 02 0f 00 "
    "16 1b 02 03 09 06 01 00 02 07 00 ff 06 00 00 00 "
    "00 02 02 0f 00 16 1b 02 03 09 06 01 00 03 07 00 "
    "ff 06 00 00 00 00 02 02 0f 00 16 1d 02 03 09 06 "
    "01 00 04 07 00 ff 06 00 00 03 bf 02 02 0f 00 16 "
    "1d 02 03 09 06 01 00 1f 07 00 ff 10 00 fd 02 02 "
    "0f ff 16 21 02 03 09 06 01 00 47 07 00 ff 10 00 "
    "ca 02 02 0f ff 16 21 02 03 09 06 01 00 20 07 00 "
    "ff 12 09 3a 02 02 0f ff 16 23 02 03 09 06 01 00 "
    "34 07 00 ff 12 09 22 02 02 0f ff 16 23 02 03 09 "
    "06 01 00 48 07 00 ff 12 09 50 02 02 0f ff 16 23 "
    "98 c4 7e"
)


def _length(frame):
    return (((frame[1] & 15) << 8) | frame[2]) + 2


class ByteStream:
    """Minimal serial-like object that returns single-byte reads."""

    def __init__(self, data):
        self.data = iter(data)

    def read(self):
        return bytes([next(self.data)])


def _read_frame(frame, oss=False):
    hub = AmsHub.__new__(AmsHub)
    hub._running = True
    hub.oss = oss
    hub._ser = ByteStream(frame)
    return hub.read_packet()


def test_reported_short_frame_is_44_bytes_and_valid():
    assert len(SHORT) == 44
    assert _length(SHORT) == len(SHORT)
    assert aidon.test_valid_data(list(SHORT), False)
    assert _read_frame(SHORT) == list(SHORT)


def test_reported_long_frame_has_three_extra_bytes():
    assert LONG_OSS[0] == 126 and LONG_OSS[-1] == 126
    assert LONG_OSS.count(b"\x0d\x0a") == 3
    assert _length(LONG_OSS) == 269
    assert len(LONG_OSS) == 272


def test_aidon_rejects_unmodified_oversized_frame():
    """Document current CRC/size protection: no silent invalid packets."""
    assert not aidon.test_valid_data(list(LONG_OSS), False)


def test_valid_short_packet_rejected_after_corruption():
    corrupted = bytearray(SHORT)
    corrupted[30] ^= 0x01
    assert not aidon.test_valid_data(list(corrupted), False)


@pytest.mark.parametrize("oss", [True, False])
def test_network_configuration_preserves_oss_flag(oss):
    """Current implementation fails for oss=True; should pass after fix."""
    config = {
        CONF_PROTOCOL: NETWORK,
        CONF_TCP_HOST: "127.0.0.1",
        CONF_TCP_PORT: 3001,
        CONF_BAUDRATE: 115200,
        CONF_PARITY: "N",
        CONF_METER_MANUFACTURER: "aidon",
        CONF_OSS_BRIKKEN: oss,
    }
    fake_serial = MagicMock()
    with (
        patch("custom_components.ams.serial.serial_for_url",
              return_value=fake_serial),
        patch("custom_components.ams.threading.Thread") as thread,
    ):
        hub = AmsHub(MagicMock(), config)
        thread.return_value.start.assert_called_once()
    assert hub.oss is oss


def test_normalized_issue_frame_has_valid_crc():
    """Remove only the three demonstrated spurious CR bytes.

    This verifies the issue's source hexdump against the existing validator;
    it does not turn off or bypass frame CRC.
    """
    clean = LONG_OSS.replace(b"\x0d\x0a", b"\x0a")
    assert len(clean) == _length(clean)
    assert aidon.test_valid_data(list(clean), False)


def test_normalized_issue_frame_parses_aidon_6525():
    clean = LONG_OSS.replace(b"\x0d\x0a", b"\x0a")
    stored, meta = aidon.parse_data({}, list(clean))
    assert meta["meter_serial"] == "7359992920808830"
    assert stored["ams_active_power_import"]["state"] == 7914


def test_unmodified_long_frame_is_not_accepted_by_receiver():
    """A byte-count-only receiver must not return a truncated frame."""
    # The current receiver may drop the invalid frame, then block waiting
    # for another. This assertion instead documents that it must never
    # report the first 269 bytes as a complete, CRC-valid frame.
    assert not aidon.test_valid_data(list(LONG_OSS[:269]), False)
