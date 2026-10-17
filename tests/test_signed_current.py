"""Regression tests for issue #113: Swedish Aidon signed current values.

The signed 16-bit input is big-endian and the Aidon SE current parser
scales it by 1/10 to amperes. These tests do not modify application code.
"""

import pytest

from custom_components.ams.parsers import signed_decode


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("0000", 0),
        ("0001", 1),
        ("000f", 15),
        ("0010", 16),
        ("0100", 256),
        ("0ff0", 4080),
        ("7fff", 32767),
        ("8000", -32768),
        ("fe0c", -500),
        ("fed4", -300),
        ("fef2", -270),
        ("ff00", -256),
        ("ff01", -255),
        ("ff06", -250),
        ("ff0f", -241),
        ("ff10", -240),
        ("ff80", -128),
        ("ffff", -1),
    ],
)
def test_signed_decode_boundaries(raw, expected):
    """Sign and low-byte zero padding must be preserved."""
    assert signed_decode(list(bytes.fromhex(raw))) == expected


@pytest.mark.parametrize("amperes", [-50.0, -30.0, -27.0, -25.6, -25.5,
                                     -25.0, -24.0, -21.0, 0.0, 25.6])
def test_swedish_aidon_current_scaling(amperes):
    """Aidon SE reports two-byte signed currents in tenths of an ampere."""
    raw_integer = round(amperes * 10)
    packet_bytes = raw_integer.to_bytes(2, byteorder="big", signed=True)
    actual = signed_decode(list(packet_bytes)) / 10
    assert actual == pytest.approx(amperes)


def test_all_signed_16bit_values():
    """Check the full two-byte domain to catch subtle decoding errors."""
    for raw_unsigned in range(65536):
        raw = raw_unsigned.to_bytes(2, byteorder="big", signed=False)
        expected = int.from_bytes(raw, byteorder="big", signed=True)
        actual = signed_decode(list(raw))
        assert actual == expected, (
            f"Raw bytes {raw.hex()}: expected {expected}, got {actual}"
        )
