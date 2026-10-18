"""Regression and diagnostic tests for hass-AMS issue #108.

Source: Kamstrup 6841138A hourly HDLC packet posted on 2025-04-15.
These tests characterize current behavior. They DO NOT establish whether the
meter's true display reading should be 250369.33 or 25036.933 kWh.
"""

import pytest

from custom_components.ams.parsers import byte_decode, kamstrup
from tests.common_test_data import TestData

# Exact decimal byte dump from GitHub issue #108 (15 April 2025).
ISSUE_108_FRAME = [
    126, 161, 44, 43, 33, 19, 252, 4, 230, 231, 0, 15, 0, 0, 0, 0,
    12, 7, 233, 4, 15, 2, 21, 0, 55, 255, 128, 0, 0, 2, 35, 10,
    14, 75, 97, 109, 115, 116, 114, 117, 112, 95, 86, 48, 48, 48, 49,
    9, 6, 1, 1, 0, 0, 5, 255, 10, 16, 53, 55, 48, 54, 53, 54, 55,
    51, 48, 55, 50, 49, 52, 49, 53, 53,
    9, 6, 1, 1, 96, 1, 1, 255, 10, 18,
    54, 56, 52, 49, 49, 51, 56, 65, 78, 50, 52, 53, 49, 48, 49,
    48, 57, 48,
    9, 6, 1, 1, 1, 7, 0, 255, 6, 0, 0, 2, 6,
    9, 6, 1, 1, 2, 7, 0, 255, 6, 0, 0, 0, 0,
    9, 6, 1, 1, 3, 7, 0, 255, 6, 0, 0, 0, 0,
    9, 6, 1, 1, 4, 7, 0, 255, 6, 0, 0, 1, 11,
    9, 6, 1, 1, 31, 7, 0, 255, 6, 0, 0, 0, 10,
    9, 6, 1, 1, 51, 7, 0, 255, 6, 0, 0, 0, 201,
    9, 6, 1, 1, 71, 7, 0, 255, 6, 0, 0, 0, 50,
    9, 6, 1, 1, 32, 7, 0, 255, 18, 0, 236,
    9, 6, 1, 1, 52, 7, 0, 255, 18, 0, 237,
    9, 6, 1, 1, 72, 7, 0, 255, 18, 0, 236,
    9, 6, 0, 1, 1, 0, 0, 255, 9, 12, 7, 233, 4, 15, 2, 21,
    0, 55, 255, 128, 0, 0,
    9, 6, 1, 1, 1, 8, 0, 255, 6, 1, 126, 8, 133,
    9, 6, 1, 1, 2, 8, 0, 255, 6, 0, 0, 0, 249,
    9, 6, 1, 1, 3, 8, 0, 255, 6, 0, 35, 166, 194,
    9, 6, 1, 1, 4, 8, 0, 255, 6, 0, 151, 72, 82,
    125, 191, 126,
]

ENERGY_CASES = [
    ("ams_active_energy_import", (1, 1, 1, 8, 0, 255),
     25_036_933, 250_369.33),
    ("ams_active_energy_export", (1, 1, 2, 8, 0, 255),
     249, 2.49),
    ("ams_reactive_energy_import", (1, 1, 3, 8, 0, 255),
     2_336_450, 23_364.50),
    ("ams_reactive_energy_export", (1, 1, 4, 8, 0, 255),
     9_914_450, 99_144.50),
]


def _raw_obis_value(frame, obis):
    """Locate a typed DLMS unsigned-32 value, avoiding offset assumptions."""
    signature = bytes((9, 6, *obis, 6))
    frame_bytes = bytes(frame)
    assert frame_bytes.count(signature) == 1, (
        f"Expected exactly one OBIS entry {obis}"
    )
    start = frame_bytes.index(signature) + len(signature)
    field = frame_bytes[start:start + 4]
    assert len(field) == 4
    return byte_decode(list(field))


def test_issue_108_hdlc_length_and_crc():
    assert len(ISSUE_108_FRAME) == 302
    assert ((ISSUE_108_FRAME[1] & 0x0F) << 8) + ISSUE_108_FRAME[2] + 2 == 302
    assert kamstrup.test_valid_data(ISSUE_108_FRAME, oss=False)


@pytest.mark.parametrize("key,obis,raw,scaled", ENERGY_CASES)
def test_issue_108_energy_registers(key, obis, raw, scaled):
    assert _raw_obis_value(ISSUE_108_FRAME, obis) == raw
    parsed, _ = kamstrup.parse_data({}, ISSUE_108_FRAME)
    assert parsed[key]["state"] == pytest.approx(scaled)


def test_issue_108_power_and_voltage_are_independently_plausible():
    parsed, _ = kamstrup.parse_data({}, ISSUE_108_FRAME)
    assert parsed["ams_active_power_import"]["state"] == 518
    assert parsed["ams_voltage_l1"]["state"] == 236
    assert parsed["ams_voltage_l2"]["state"] == 237
    assert parsed["ams_voltage_l3"]["state"] == 236


def test_issue_108_corrupt_frame_fails_crc():
    corrupted = ISSUE_108_FRAME.copy()
    corrupted[258] ^= 1
    assert not kamstrup.test_valid_data(corrupted, oss=False)


def test_existing_kamstrup_fixture_unchanged():
    assert kamstrup.test_valid_data(TestData.KAMSTRUP_HOURLY, oss=False)
    parsed, _ = kamstrup.parse_data({}, TestData.KAMSTRUP_HOURLY)
    assert parsed["ams_active_energy_import"]["state"] == 155_232.51
