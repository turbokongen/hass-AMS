"""
Decode for HAN Aidon.

This module will decode the incoming message from Mbus serial.
"""
import logging
from datetime import datetime
from crccheck.crc import CrcX25
from custom_components.ams.parsers import byte_decode, field_type
from custom_components.ams.const import (
    ATTR_DEVICE_CLASS,
    ATTR_LAST_RESET,
    ATTR_STATE_CLASS,
    DATA_FLAG,
    DEVICE_CLASS_ENERGY,
    FRAME_FLAG,
    HAN_ACTIVE_POWER_IMPORT,
    HAN_LIST_VER_ID,
    HAN_METER_DATETIME,
    HAN_METER_MANUFACTURER,
    HAN_METER_SERIAL,
    HAN_METER_TYPE,
    HAN_OBIS_CODE,
    HAN_OBIS_DATETIME,
    HOURLY_SENSORS,
    LAST_RESET_DATA,
    LIST_TYPE_MINI,
    METER_TYPE,
    SENSOR_ATTR,
    SENSOR_COMMON_OBIS_MAP,
    SENSOR_ICON,
    SENSOR_ICON_MAP,
    SENSOR_OBIS_MAP,
    SENSOR_STATE,
    SENSOR_UNIT,
    SENSOR_UOM,
    STATE_CLASS_MEASUREMENT,
    WEEKDAY_MAPPING,
)
_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-branches,too-many-locals,too-many-nested-blocks
# pylint: disable=too-many-statements
def parse_data(stored, data):
    """Parse the incoming data to dict"""
    sensor_data = {}
    han_data = {}
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    list_type = pkt[19]
    han_data["list_type"] = list_type
    _LOGGER.debug("list_type is %s", list_type)
    if list_type == LIST_TYPE_MINI:
        if HAN_ACTIVE_POWER_IMPORT not in stored:
            # Wait for long message (10sec) to get full attribute set before
            # publishing mini list data.
            return stored, han_data
        key = HAN_ACTIVE_POWER_IMPORT
        for item in SENSOR_OBIS_MAP[key]:
            for i in range(len(pkt)):
                if pkt[i:i + len(item)] == item:
                    # Double-long-unsigned dict construct
                    if pkt[i + len(item)] == 6:
                        v_start = i + len(item) + 1
                        v_stop = v_start + 4
                        han_data["obis_" + key] = (
                            '.'.join([str(elem) for elem in item])
                        )
                        han_data[key] = (
                            byte_decode(fields=pkt[v_start:v_stop])
                        )
                        sensor_data[key] = {
                            SENSOR_STATE: han_data[key],
                            SENSOR_ATTR: {
                                HAN_METER_MANUFACTURER: stored[key][
                                    SENSOR_ATTR][
                                        HAN_METER_MANUFACTURER],
                                HAN_METER_TYPE: stored[key][
                                    SENSOR_ATTR][
                                        HAN_METER_TYPE],
                                HAN_OBIS_CODE: han_data["obis_" + key],
                                HAN_METER_SERIAL: stored[key][
                                    SENSOR_ATTR][
                                        HAN_METER_SERIAL],
                                SENSOR_UOM:
                                    SENSOR_UNIT.get(key),
                                SENSOR_ICON: (
                                    "mdi:" + SENSOR_ICON_MAP.get(
                                        key)),
                            },

                        }
                        _LOGGER.debug(
                            "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                            key, item, (i, i + len(item)),
                            (pkt[(i + len(item))])
                        )
                        _LOGGER.debug(
                            "Value double OBIS type  6: %s, Index:%s",
                            han_data[key], (v_start, v_stop)
                        )
        return stored, han_data

    # Ensure basic data before parsing package
    for key in SENSOR_COMMON_OBIS_MAP:
        if len(SENSOR_COMMON_OBIS_MAP[key]) == 2:
            for item in SENSOR_COMMON_OBIS_MAP[key]:
                for i in range(len(pkt)):
                    if pkt[i:i + len(item)] == item:
                        # Date time construct
                        if pkt[i + len(item)] == 9:
                            han_data[HAN_OBIS_DATETIME] = (
                                '.'.join([str(elem) for elem in item])
                            )
                            v_start = i + len(item) + 2
                            meter_date_time_year = (
                                byte_decode(fields=pkt[v_start:(v_start + 2)],
                                            count=2))
                            meter_date_time_month = pkt[v_start + 2]
                            meter_date_time_date = pkt[v_start + 3]
                            meter_date_time_day_of_week = (
                                WEEKDAY_MAPPING.get(pkt[v_start + 4]))
                            meter_date_time_hour = (
                                str(pkt[v_start + 5]).zfill(2)
                            )
                            meter_date_time_minute = (
                                str(pkt[v_start + 6]).zfill(2)
                            )
                            meter_date_time_seconds = (
                                str(pkt[v_start + 7]).zfill(2)
                            )
                            meter_date_time_str = (
                                str(meter_date_time_year)
                                + "-"
                                + str(meter_date_time_month)
                                + "-"
                                + str(meter_date_time_date)
                                + "-"
                                + str(meter_date_time_hour)
                                + "-"
                                + str(meter_date_time_minute)
                                + "-"
                                + str(meter_date_time_minute)
                                + "-"
                                + str(meter_date_time_seconds)
                            )
                            han_data[
                                HAN_METER_DATETIME] = meter_date_time_str
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                HAN_METER_DATETIME, item,
                                (i, i + len(item)), (pkt[(i + len(item))]))
                            _LOGGER.debug("%s, %s, %s, %s, %s, %s, %s, %s, "
                                          "%s, %s",
                                          HAN_METER_DATETIME,
                                          item, meter_date_time_year,
                                          meter_date_time_month,
                                          meter_date_time_date,
                                          meter_date_time_day_of_week,
                                          meter_date_time_hour,
                                          meter_date_time_minute,
                                          meter_date_time_seconds,
                                          meter_date_time_str)
                        # Visible string construct
                        elif pkt[i + len(item)] == 10:
                            v_start = i + len(item) + 2
                            v_length = pkt[v_start - 1]
                            v_stop = v_start + v_length
                            han_data["obis_" + key] = (
                                '.'.join([str(elem) for elem in item])
                            )
                            if key == HAN_METER_TYPE:
                                han_data[key] = (
                                    METER_TYPE.get(field_type(fields=pkt[
                                        v_start:v_stop], enc=chr, dec=int))
                                )
                            else:
                                han_data[key] = (
                                    field_type(fields=pkt[v_start:v_stop],
                                               enc=chr)
                                )
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                key, item, (i, i + len(item)),
                                (pkt[(i + len(item))]))
                            _LOGGER.debug(
                                "Value double OBIS type 10: %s, Index:%s",
                                han_data[key], (v_start, v_stop))
        for i in range(len(pkt)):
            if (pkt[i:i + len(SENSOR_COMMON_OBIS_MAP[key])] ==
                    SENSOR_COMMON_OBIS_MAP[key]):
                # Visible string construct
                if pkt[i + len(SENSOR_COMMON_OBIS_MAP[key])] == 10:
                    print(SENSOR_COMMON_OBIS_MAP[key], key)
                    v_start = i + len(SENSOR_COMMON_OBIS_MAP[key]) + 2
                    v_length = pkt[v_start - 1]
                    v_stop = v_start + v_length
                    han_data["obis_" + key] = (
                        '.'.join([str(elem) for elem in
                                  SENSOR_COMMON_OBIS_MAP[key]])
                    )
                    han_data[key] = (
                        field_type(fields=pkt[v_start:v_stop], enc=chr)
                    )
                    _LOGGER.debug(
                        "%s, OBIS:%s, Index:%s, Type:%s Single OBIS",
                        key, SENSOR_COMMON_OBIS_MAP[key],
                        (i, i + len(SENSOR_COMMON_OBIS_MAP[key])),
                        (pkt[(i + len(SENSOR_COMMON_OBIS_MAP[key]))]))
                    _LOGGER.debug(
                        "Value Single OBIS type 10: %s, Index:%s",
                        han_data[key], (v_start, v_stop))
    for key in SENSOR_OBIS_MAP:
        if len(SENSOR_OBIS_MAP[key]) == 2:
            for item in SENSOR_OBIS_MAP[key]:
                for i in range(len(pkt)):
                    if pkt[i:i + len(item)] == item:
                        # Double-long-unsigned dict construct
                        if pkt[i + len(item)] == 6:
                            v_start = i + len(item) + 1
                            v_stop = v_start + 4
                            han_data["obis_" + key] = (
                                '.'.join([str(elem) for elem in item])
                            )
                            measure = (
                                byte_decode(fields=pkt[v_start:v_stop])
                            )
                            if key in HOURLY_SENSORS:
                                han_data[key] = measure / 100
                            else:
                                han_data[key] = measure
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                key, item, (i, i + len(item)),
                                (pkt[(i + len(item))])
                            )
                            sensor_data[key] = {
                                SENSOR_STATE: han_data[key],
                                SENSOR_ATTR: {
                                    HAN_METER_MANUFACTURER: han_data[
                                        HAN_LIST_VER_ID],
                                    HAN_METER_TYPE: han_data[
                                        HAN_METER_TYPE],
                                    HAN_OBIS_CODE: han_data[
                                        "obis_" + key],
                                    HAN_METER_SERIAL: han_data[
                                        HAN_METER_SERIAL],
                                    SENSOR_UOM:
                                        SENSOR_UNIT.get(key),
                                    SENSOR_ICON: (
                                        "mdi:" +
                                        SENSOR_ICON_MAP.get(key)),
                                },
                            }
                            if key in HOURLY_SENSORS:
                                sensor_data[key][SENSOR_ATTR][
                                    HAN_METER_DATETIME] = han_data[
                                        HAN_METER_DATETIME]
                                sensor_data[key][SENSOR_ATTR][
                                    ATTR_STATE_CLASS] = (
                                        STATE_CLASS_MEASUREMENT)
                                sensor_data[key][SENSOR_ATTR][
                                    ATTR_DEVICE_CLASS] = (
                                        DEVICE_CLASS_ENERGY)
                                sensor_data[key][SENSOR_ATTR][
                                    ATTR_LAST_RESET] = (
                                        LAST_RESET_DATA)
                            _LOGGER.debug(
                                "Value double OBIS type  6: %s, Index:%s",
                                han_data[key], (v_start, v_stop)
                            )
                        # Long-signed & Long-unsigned dict construct
                        elif (pkt[i + len(item)] == 16 or
                              pkt[i + len(item)] == 18):
                            v_start = i + len(item) + 1
                            v_stop = v_start + 2
                            han_data["obis_" + key] = (
                                '.'.join([str(elem) for elem in item])
                            )
                            han_data[key] = (
                                (byte_decode(fields=pkt[v_start:v_stop],
                                             count=2) / 10)
                            )
                            sensor_data[key] = {
                                SENSOR_STATE: han_data[key],
                                SENSOR_ATTR: {
                                    HAN_METER_MANUFACTURER: han_data[
                                        HAN_LIST_VER_ID],
                                    HAN_METER_TYPE: han_data[
                                        HAN_METER_TYPE],
                                    HAN_OBIS_CODE: han_data[
                                        "obis_" + key],
                                    HAN_METER_SERIAL: han_data[
                                        HAN_METER_SERIAL],
                                    SENSOR_UOM:
                                        SENSOR_UNIT.get(key),
                                    SENSOR_ICON: (
                                        "mdi:" +
                                        SENSOR_ICON_MAP.get(key)),
                                },

                            }
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                key, item, (i, i + len(item)),
                                (pkt[(i + len(item))]))
                            _LOGGER.debug(
                                "Value double OBIS type  16/18: %s, Index:%s",
                                han_data[key], (v_start, v_stop))
        for i in range(len(pkt)):
            if (pkt[i:i + len(SENSOR_OBIS_MAP[key])] ==
                    SENSOR_OBIS_MAP[key]):
                # Double-long-unsigned construct
                if pkt[i + len(SENSOR_OBIS_MAP[key])] == 6:
                    v_start = i + len(SENSOR_OBIS_MAP[key]) + 1
                    v_stop = v_start + 4
                    han_data["obis_" + key] = (
                        '.'.join([str(elem) for elem in
                                  SENSOR_OBIS_MAP[key]])
                    )
                    han_data[key] = (
                        byte_decode(fields=pkt[v_start:v_stop])
                    )
                    sensor_data[key] = {
                        SENSOR_STATE: han_data[key],
                        SENSOR_ATTR: {
                            HAN_METER_MANUFACTURER: han_data[
                                HAN_LIST_VER_ID],
                            HAN_METER_TYPE: han_data[
                                HAN_METER_TYPE],
                            HAN_OBIS_CODE: han_data["obis_" + key],
                            HAN_METER_SERIAL: han_data[
                                HAN_METER_SERIAL],
                            SENSOR_UOM: SENSOR_UNIT.get(key),
                            SENSOR_ICON: (
                                "mdi:" + SENSOR_ICON_MAP.get(key)),
                        },

                    }
                    _LOGGER.debug(
                        "%s, OBIS:%s, Index:%s, Type:%s Single OBIS", key,
                        SENSOR_OBIS_MAP[key], (i, i + len(
                            SENSOR_OBIS_MAP[key])),
                        (pkt[(i + len(SENSOR_OBIS_MAP[key]))]))
                    _LOGGER.debug(
                        "Value single OBIS type 6: %s Index:%s",
                        han_data[key], (v_start, v_stop))

    stored.update(sensor_data)
    return stored, han_data


def test_valid_data(data):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 581 or len(data) < 44:
        _LOGGER.debug("Invalid packet size %s", len(data))
        return False

    if not data[0] and data[-1] == FRAME_FLAG:
        _LOGGER.debug(
            "%s Received %s bytes of %s data",
            datetime.now().isoformat(),
            len(data),
            False,
        )
        return False

    header_checksum = CrcX25.calc(bytes(data[1:7]))
    read_header_checksum = data[8] << 8 | data[7]

    if header_checksum != read_header_checksum:
        _LOGGER.debug("Invalid header CRC check")
        return False

    frame_checksum = CrcX25.calc(bytes(data[1:-3]))
    read_frame_checksum = data[-2] << 8 | data[-3]

    if frame_checksum != read_frame_checksum:
        _LOGGER.debug("Invalid frame CRC check")
        return False

    if data[9:13] != DATA_FLAG:
        _LOGGER.debug("Data does not start with %s: %s", DATA_FLAG,
                      data[9:13])
        return False

    packet_size = len(data)
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2

    if packet_size != read_packet_size:
        _LOGGER.debug(
            "Packet size does not match read packet size: %s : %s",
            packet_size,
            read_packet_size,
        )
        return False

    return True
