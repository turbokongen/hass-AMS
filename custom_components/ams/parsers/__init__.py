import logging

_LOGGER = logging.getLogger(__name__)


def field_type(default="", fields=None, enc=str, dec=None):
    """Obis/data field decoder/encoder."""
    data = default.join(enc(i) for i in fields)
    if dec:
        return dec(data)
    return data


def byte_decode(fields=None, count=4):
    """Data content decoder."""
    _LOGGER.debug("fields= %s", fields)
    if count == 2:
        data = fields[0] << 8 | fields[1]
        return data

    data = fields[0] << 24 | fields[1] << 16 | fields[2] << 8 | fields[3]

    return data
