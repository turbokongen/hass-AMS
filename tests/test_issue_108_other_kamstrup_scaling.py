"""Regression tests: other Kamstrup models retain /100 energy scaling.

The existing Kamstrup hourly telegram is intentionally different from
model 6841138 (issue #108). Assert raw OBIS values *and* parsed values,
so an accidental global /1000 change is detected.
"""

import pytest

from custom_components.ams.parsers import byte_decode, kamstrup
from tests.common_test_data import TestData


FRAME = TestData.KAMSTRUP_HOURLY

ENERGY_REGISTERS = [
    ("ams_active_energy_import", (1, 1, 1, 8, 0, 255), 15523251, 155232.51),
    ("ams_active_energy_export", (1, 1, 2, 8, 0, 255), 0, 0.0),
    ("ams_reactive_energy_import", (1, 1, 3, 8, 0, 255), 324289, 3242.89),
    ("ams_reactive_energy_export", (1, 1, 4, 8, 0, 255), 724362, 7243.62),
]


def _raw_uint32(obis):
    """Extract exact unsigned 32-bit value after a DLMS OBIS tag."""
    payload = bytes(FRAME)
    signature = bytes((9, 6, *obis, 6))
    assert payload.count(signature) == 1
    index = payload.index(signature) + len(signature)
    return byte_decode(list(payload[index:index + 4]))


def test_reference_telegram_is_not_issue_108_model():
    """Guard against accidentally testing the special-case model itself."""
    payload = bytes(FRAME)
    model_obis = bytes((9, 6, 1, 1, 96, 1, 1, 255, 10))
    assert payload.count(model_obis) == 1
    start = payload.index(model_obis) + len(model_obis) + 1
    model = payload[start:start + 7].decode("ascii")
    assert model.isdigit()
    assert model != "6841138"
    assert kamstrup.test_valid_data(FRAME, oss=False)


@pytest.mark.parametrize("key,obis,raw,expected", ENERGY_REGISTERS)
def test_other_kamstrup_retains_hundredths_scaling(
    key, obis, raw, expected
):
    """Verify /100 (not /1000) for all four energy registers."""
    assert _raw_uint32(obis) == raw
    parsed, _ = kamstrup.parse_data({}, FRAME)
    assert parsed[key]["state"] == pytest.approx(expected)
