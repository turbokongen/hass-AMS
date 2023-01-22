"""Base functions to convert data from meter"""
import logging

_LOGGER = logging.getLogger(__name__)


def field_type(default="", fields=None, enc=str, dec=None):
    """Obis/data field decoder/encoder."""
    #_LOGGER.debug("field_type=%s", fields)
    data = default.join(enc(i) for i in fields)
    if dec:
        return dec(data)
    return data


def byte_decode(fields=None, count=4):
    """Data content decoder."""
    #_LOGGER.debug("byte_decode=%s", fields)
    if count == 2:
        data = fields[0] << 8 | fields[1]
        return data

    data = fields[0] << 24 | fields[1] << 16 | fields[2] << 8 | fields[3]

    return data


def signed_decode(fields=None):
    """Signed value decoder."""
    s_data = fields
    hex_val = ""
    for num in s_data:
        hex_val += hex(num)[2:]
    t = int(hex_val, 16)
    if t & (1 << (16 - 1)):
        t -= 1 << 16
    return t
