"""
Decode for HAN Kaifa.

This module will decode the incoming message from Mbus serial.
Kaifa does not use OBIS in their data, so real parsing is not possible.
"""
import logging
from datetime import datetime
from crccheck.crc import CrcX25
from custom_components.ams.parsers import byte_decode, field_type
from custom_components.ams.const import (
    ATTR_DEVICE_CLASS,
    ATTR_STATE_CLASS,
    DATA_FLAG,
    DEVICE_CLASS_ENERGY,
    FRAME_FLAG,
    HAN_LIST_VER_ID,
    HAN_METER_DATETIME,
    HAN_METER_DAYOFWEEK,
    HAN_METER_LIST_TYPE,
    HAN_METER_MANUFACTURER,
    HAN_METER_SERIAL,
    HAN_METER_TYPE,
    HAN_PACKET_SIZE,
    LIST_TYPE_LONG_1PH,
    LIST_TYPE_LONG_3PH,
    LIST_TYPE_SHORT_1PH,
    LIST_TYPE_SHORT_3PH,
    LIST_TYPE_MINI,
    METER_TYPE,
    SENSOR_ATTR,
    SENSOR_ICON,
    SENSOR_STATE,
    SENSOR_UOM,
    STATE_CLASS_TOTAL_INCREASING,
    UNKNOWN_METER,
    WEEKDAY_MAPPING,
)
_LOGGER = logging.getLogger(__name__)


# pylint: disable=too-many-locals, too-many-statements
def parse_data(stored, data, swedish):
    """Parse the incoming data to dict."""
    sensor_data = {}
    han_data = {}
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data[HAN_PACKET_SIZE] = read_packet_size
    date_time_year = byte_decode(fields=pkt[19:21], count=2)
    date_time_month = pkt[21]
    date_time_date = pkt[22]
    han_data[HAN_METER_DAYOFWEEK] = WEEKDAY_MAPPING.get(pkt[23])
    date_time_hour = str(pkt[24]).zfill(2)
    date_time_minute = str(pkt[25]).zfill(2)
    date_time_seconds = str(pkt[26]).zfill(2)
    date_time_str = (
        str(date_time_year)
        + "-"
        + str(date_time_month)
        + "-"
        + str(date_time_date)
        + " "
        + date_time_hour
        + ":"
        + date_time_minute
        + ":"
        + date_time_seconds
    )
    han_data["date_time"] = date_time_str
    list_type = pkt[32]
    han_data[HAN_METER_LIST_TYPE] = list_type
    if list_type is LIST_TYPE_MINI or swedish:
        if swedish:
            han_data["active_power_p"] = byte_decode(fields=pkt[71:75])
        else:
            han_data["active_power_p"] = byte_decode(fields=pkt[34:38])
        sensor_data["ams_active_power_import"] = {
            SENSOR_STATE: han_data["active_power_p"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                SENSOR_UOM: "W",
                SENSOR_ICON: "mdi:gauge",
            },
        }
        if not swedish:
            stored.update(sensor_data)
            return stored, han_data

    han_data[HAN_LIST_VER_ID] = field_type(fields=pkt[35:42], enc=chr)
    han_data[HAN_METER_SERIAL] = field_type(fields=pkt[44:60], enc=chr)
    han_data[HAN_METER_TYPE] = (
        METER_TYPE.get(field_type(fields=pkt[62:70], enc=chr), UNKNOWN_METER)
    )
    han_data["active_power_n"] = byte_decode(fields=pkt[76:80]) / 100
    sensor_data["ams_active_power_export"] = {
        SENSOR_STATE: han_data["active_power_n"],
        SENSOR_ATTR: {
            "timestamp": han_data["date_time"],
            HAN_METER_MANUFACTURER: han_data[
                HAN_LIST_VER_ID].title(),
            HAN_METER_TYPE: han_data[HAN_METER_TYPE],
            HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
            SENSOR_UOM: "W",
            SENSOR_ICON: "mdi:gauge",
        },
    }
    han_data["reactive_power_p"] = byte_decode(fields=pkt[81:85])
    sensor_data["ams_reactive_power_import"] = {
        SENSOR_STATE: han_data["reactive_power_p"],
        SENSOR_ATTR: {
            "timestamp": han_data["date_time"],
            HAN_METER_MANUFACTURER: han_data[
                HAN_LIST_VER_ID].title(),
            HAN_METER_TYPE: han_data[HAN_METER_TYPE],
            HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
            SENSOR_UOM: "VAr",
            SENSOR_ICON: "mdi:gauge",
        },
    }
    han_data["reactive_power_n"] = byte_decode(fields=pkt[86:90])
    sensor_data["ams_reactive_power_export"] = {
        SENSOR_STATE: han_data["reactive_power_n"],
        SENSOR_ATTR: {
            "timestamp": han_data["date_time"],
            HAN_METER_MANUFACTURER: han_data[
                HAN_LIST_VER_ID].title(),
            HAN_METER_TYPE: han_data[HAN_METER_TYPE],
            HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
            SENSOR_UOM: "VAr",
            SENSOR_ICON: "mdi:gauge",
        },
    }
    han_data["current_l1"] = byte_decode(fields=pkt[91:95]) / 1000
    sensor_data["ams_current_l1"] = {
        SENSOR_STATE: han_data["current_l1"],
        SENSOR_ATTR: {
            "timestamp": han_data["date_time"],
            HAN_METER_MANUFACTURER: han_data[
                HAN_LIST_VER_ID].title(),
            HAN_METER_TYPE: han_data[HAN_METER_TYPE],
            HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
            SENSOR_UOM: "A",
            SENSOR_ICON: "mdi:current-ac",
        },
    }

    if (list_type is LIST_TYPE_SHORT_3PH or
            list_type is LIST_TYPE_LONG_3PH):
        han_data["current_l2"] = byte_decode(fields=pkt[96:100]) / 1000
        sensor_data["ams_current_l2"] = {
            SENSOR_STATE: han_data["current_l2"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "A",
                SENSOR_ICON: "mdi:current-ac",
            },
        }
        han_data["current_l3"] = byte_decode(fields=pkt[101:105]) / 1000
        sensor_data["ams_current_l3"] = {
            SENSOR_STATE: han_data["current_l3"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "A",
                SENSOR_ICON: "mdi:current-ac",
            },
        }
        han_data["voltage_l1"] = byte_decode(fields=pkt[106:110]) / 10
        sensor_data["ams_voltage_l1"] = {
            SENSOR_STATE: han_data["voltage_l1"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "V",
                SENSOR_ICON: "mdi:flash",
            },
        }
        han_data["voltage_l2"] = byte_decode(fields=pkt[111:115]) / 10
        sensor_data["ams_voltage_l2"] = {
            SENSOR_STATE: han_data["voltage_l2"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "V",
                SENSOR_ICON: "mdi:flash",
            },
        }
        han_data["voltage_l3"] = byte_decode(fields=pkt[116:120]) / 10
        sensor_data["ams_voltage_l3"] = {
            SENSOR_STATE: han_data["voltage_l3"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "V",
                SENSOR_ICON: "mdi:flash",
            },
        }
        if list_type == LIST_TYPE_LONG_3PH:
            meter_date_time_year = byte_decode(fields=pkt[122:124], count=2)
            meter_date_time_month = pkt[124]
            meter_date_time_date = pkt[125]
            han_data[HAN_METER_DAYOFWEEK] = WEEKDAY_MAPPING.get(
                pkt[126])
            meter_date_time_hour = str(pkt[127]).zfill(2)
            meter_date_time_minute = str(pkt[128]).zfill(2)
            meter_date_time_seconds = str(pkt[129]).zfill(2)
            han_data[HAN_METER_DATETIME] = (
                str(meter_date_time_year)
                + "-"
                + str(meter_date_time_month)
                + "-"
                + str(meter_date_time_date)
                + " "
                + meter_date_time_hour
                + ":"
                + meter_date_time_minute
                + ":"
                + meter_date_time_seconds
            )
            han_data["active_energy_p"] = (
                byte_decode(fields=pkt[135:139]) / 1000
            )
            sensor_data["ams_active_energy_import"] = {
                SENSOR_STATE: han_data["active_energy_p"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kWh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["active_energy_n"] = (
                byte_decode(fields=pkt[140:144]) / 1000
            )
            sensor_data["ams_active_energy_export"] = {
                SENSOR_STATE: han_data["active_energy_n"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kWh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["reactive_energy_p"] = (
                byte_decode(fields=pkt[145:149]) / 1000
            )
            sensor_data["ams_reactive_energy_import"] = {
                SENSOR_STATE: han_data["reactive_energy_p"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kVArh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["reactive_energy_n"] = (
                byte_decode(fields=pkt[150:154]) / 1000
            )
            sensor_data["ams_reactive_energy_export"] = {
                SENSOR_STATE: han_data["reactive_energy_n"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kVArh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }

    if (list_type is LIST_TYPE_SHORT_1PH or
            list_type is LIST_TYPE_LONG_1PH):

        han_data["voltage_l1"] = byte_decode(fields=pkt[96:100]) / 10
        sensor_data["ams_voltage_l1"] = {
            SENSOR_STATE: han_data["voltage_l1"],
            SENSOR_ATTR: {
                "timestamp": han_data["date_time"],
                HAN_METER_MANUFACTURER: han_data[
                    HAN_LIST_VER_ID].title(),
                HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                SENSOR_UOM: "V",
                SENSOR_ICON: "mdi:flash",
            },
        }

        if list_type == LIST_TYPE_LONG_1PH:
            meter_date_time_year = byte_decode(fields=pkt[102:104], count=2)
            meter_date_time_month = pkt[104]
            meter_date_time_date = pkt[105]
            han_data[HAN_METER_DAYOFWEEK] = WEEKDAY_MAPPING.get(
                pkt[106])
            meter_date_time_hour = str(pkt[107]).zfill(2)
            meter_date_time_minute = str(pkt[108]).zfill(2)
            meter_date_time_seconds = str(pkt[109]).zfill(2)
            han_data[HAN_METER_DATETIME] = (
                str(meter_date_time_year)
                + "-"
                + str(meter_date_time_month)
                + "-"
                + str(meter_date_time_date)
                + " "
                + meter_date_time_hour
                + ":"
                + meter_date_time_minute
                + ":"
                + meter_date_time_seconds
            )
            han_data["active_energy_p"] = (
                byte_decode(fields=pkt[115:119]) / 1000
            )
            sensor_data["ams_active_energy_import"] = {
                SENSOR_STATE: han_data["active_energy_p"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kWh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["active_energy_n"] = (
                byte_decode(fields=pkt[120:124]) / 1000
            )
            sensor_data["ams_active_energy_export"] = {
                SENSOR_STATE: han_data["active_energy_n"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kWh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["reactive_energy_p"] = (
                byte_decode(fields=pkt[125:129]) / 1000
            )
            sensor_data["ams_reactive_energy_import"] = {
                SENSOR_STATE: han_data["reactive_energy_p"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kVArh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
            han_data["reactive_energy_n"] = (
                byte_decode(fields=pkt[130:134]) / 1000
            )
            sensor_data["ams_reactive_energy_export"] = {
                SENSOR_STATE: han_data["reactive_energy_n"],
                SENSOR_ATTR: {
                    "timestamp": han_data["date_time"],
                    HAN_METER_DATETIME: han_data[
                        HAN_METER_DATETIME],
                    HAN_METER_MANUFACTURER: (
                        han_data[HAN_LIST_VER_ID].title()
                    ),
                    HAN_METER_TYPE: han_data[HAN_METER_TYPE],
                    HAN_METER_SERIAL: han_data[HAN_METER_SERIAL],
                    SENSOR_UOM: "kVArh",
                    SENSOR_ICON: "mdi:gauge",
                    ATTR_STATE_CLASS: STATE_CLASS_TOTAL_INCREASING,
                    ATTR_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
                },
            }
    stored.update(sensor_data)
    return stored, han_data


def test_valid_data(data):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 157 or len(data) < 41:
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
