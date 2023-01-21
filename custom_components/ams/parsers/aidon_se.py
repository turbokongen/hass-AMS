"""
Decode for Swedish HAN Aidon.

This module will decode the incoming message from Mbus serial.
"""
import logging

from datetime import datetime
from crccheck.crc import CrcX25
from custom_components.ams.parsers import byte_decode, signed_decode
from custom_components.ams.const import (
    ACTIVE_ENERGY_SENSORS,
    ATTR_DEVICE_CLASS,
    ATTR_STATE_CLASS,
    DATA_FLAG,
    DEC_FRAME_FLAG,
    HAN_LIST_VER_ID,
    HAN_METER_DATETIME,
    HAN_METER_LIST_TYPE,
    HAN_METER_MANUFACTURER,
    HAN_METER_SERIAL,
    HAN_METER_TYPE,
    HAN_OBIS_CODE,
    HAN_OBIS_DATETIME,
    HAN_PACKET_SIZE,
    HOURLY_SENSORS,
    METER_TYPE,
    SENSOR_ATTR,
    SENSOR_COMMON_OBIS_MAP,
    SENSOR_ICON,
    SENSOR_ICON_MAP,
    SENSOR_OBIS_MAP,
    SENSOR_STATE,
    SENSOR_UNIT,
    SENSOR_UOM,
    WEEKDAY_MAPPING,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass
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
    han_data[HAN_PACKET_SIZE] = read_packet_size
    list_type = pkt[19]
    han_data[HAN_METER_LIST_TYPE] = list_type
    _LOGGER.debug("list_type is %s", list_type)
    # Swedish Aidon package does not contain meter_type or meter_serial
    han_data[HAN_METER_SERIAL] = "00"
    han_data[HAN_METER_TYPE] = METER_TYPE.get(6484)
    # Swedish Aidon package does not contain obis_list_version. It is
    # defined in document: Aidon RJ45 HAN interface funktionsbeskrivning
    # v1.4A 2020.10.06 as AIDON_H0001.
    han_data[HAN_LIST_VER_ID] = "AIDON_H0001"

    # Get the date and time
    for item in SENSOR_COMMON_OBIS_MAP[HAN_METER_DATETIME]:
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
                    meter_date_time_hour = str(pkt[v_start + 5]).zfill(2)
                    meter_date_time_minute = str(pkt[v_start + 6]).zfill(2)
                    meter_date_time_seconds = str(pkt[v_start + 7]).zfill(2)
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
                    han_data[HAN_METER_DATETIME] = meter_date_time_str
                    _LOGGER.debug("%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
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
                            measure = byte_decode(fields=pkt[v_start:v_stop])
                            if key in HOURLY_SENSORS:
                                han_data[key] = measure / 1000
                            else:
                                han_data[key] = measure
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
                                    ATTR_DEVICE_CLASS] = (
                                        SensorDeviceClass.ENERGY)
                                if key in ACTIVE_ENERGY_SENSORS:
                                    sensor_data[key][SENSOR_ATTR][
                                        ATTR_STATE_CLASS] = (
                                            SensorStateClass.TOTAL_INCREASING)
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                key, item, (i, i + len(item)),
                                (pkt[(i + len(item))])
                            )
                            _LOGGER.debug(
                                "Value double OBIS type  6: %s, Index:%s",
                                han_data[key], (v_start, v_stop)
                            )
                        # Long-signed & Long-unsigned dict construct
                        elif (pkt[i + len(item)] == 16 or
                              pkt[i + len(item)] == 18):
                            signed = None
                            if pkt[i + len(item)] == 16:
                                signed = True
                            v_start = i + len(item) + 1
                            v_stop = v_start + 2
                            han_data["obis_" + key] = (
                                '.'.join([str(elem) for elem in item])
                            )
                            if signed:
                                han_data[key] = (
                                    signed_decode(
                                        fields=pkt[v_start:v_stop]) / 10
                                )
                            else:
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
                        # Visible string construct
                        elif pkt[i + len(item)] == 10:
                            v_start = i + len(item) + 2
                            v_length = pkt[v_start - 1]
                            v_stop = v_start + v_length
                            _LOGGER.debug(
                                "%s, OBIS:%s, Index:%s, Type:%s Double OBIS",
                                key, item, (i, i + len(item)),
                                (pkt[(i + len(item))]))
                            _LOGGER.debug(
                                "Value double OBIS type 10: %s, Index:%s",
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
                    han_data[key] = byte_decode(fields=pkt[v_start:v_stop])
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


def test_valid_data(data, oss):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        _LOGGER.debug("Packet is None!")
        return False

    if len(data) > 581 or len(data) < 44:
        _LOGGER.debug("Invalid packet size %s", len(data))
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

    if not data[0] == DEC_FRAME_FLAG and data[-1] == DEC_FRAME_FLAG:
        _LOGGER.debug(
            "%s Received %s bytes of %s data",
            datetime.now().isoformat(),
            len(data),
            False,
        )
        return False

    if data[9:13] != DATA_FLAG:
        _LOGGER.debug("Data does not start with %s: %s", DATA_FLAG,
                      data[9:13])
        return False

    header_checksum = CrcX25.calc(bytes(data[1:7]))
    read_header_checksum = data[8] << 8 | data[7]

    if header_checksum != read_header_checksum:
        _LOGGER.debug("Invalid header CRC check")
        return False

    if not oss:
        frame_checksum = CrcX25.calc(bytes(data[1:-3]))
        read_frame_checksum = data[-2] << 8 | data[-3]

        if frame_checksum != read_frame_checksum:
            _LOGGER.debug("Invalid frame CRC check")
            return False

    return True
