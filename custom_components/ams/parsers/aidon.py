"""
Decode for HAN Aidon.

This module will decode the incoming message from Mbus serial.
"""
import logging
from datetime import datetime

from crccheck.crc import CrcX25

from ..const import (
    DATA_FLAG,
    FRAME_FLAG,
    LIST_TYPE_LONG_1PH,
    LIST_TYPE_LONG_3PH,
    LIST_TYPE_MINI,
    LIST_TYPE_SHORT_1PH,
    LIST_TYPE_SHORT_3PH,
    WEEKDAY_MAPPING,
)
from . import byte_decode, field_type

_LOGGER = logging.getLogger(__name__)

LIST_TYPE_SHORT_3PH_3W = 12
LIST_TYPE_LONG_3PH_3W = 17

METER_TYPE = {
    6515: (
        "6515 1-phase Meter with CB on both lines and Earth "
        "Fault Current Measurement"
    ),
    6475: "6475 RF2-system module Master 500mW 2G/3G/4G",
    6478: "6478 RF2-system module Master 500mW 2G/3G/4G Ethernet",
    6479: "6479 RF2-system module Master 500mW 2G73G/4G Ethernet Integrated HAN",
    6483: "6483 RF2-system module Slave 500mW",
    6484: "6484 RF2-system module Slave 500mW Integrated HAN",
    6515: "6515 1-phase Meter with CB and Earth fault Measurement",
    6525: "6525 3-phase Meter with CB and Earth Fault Measurement",
    6534: "6534 3-phase Meter with CB and Neutral Current Measurement",
    6540: "6540 3-phase CT Meter",
    6550: "6550 3-phase CT Meter",
}


def parse_data(stored, data):
    """Parse the incoming data to dict."""
    sensor_data = {}
    han_data = {}
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    list_type = pkt[19]
    han_data["list_type"] = list_type
    if list_type == LIST_TYPE_MINI:
        if "ams_active_power_import" not in stored:
            # Wait for long message to get full attribute set before
            # publishing mini list data
            return stored, han_data
        han_data["obis_a_p_p"] = field_type(".", fields=pkt[24:30])
        han_data["active_power_p"] = byte_decode(fields=pkt[31:35])
        sensor_data["ams_active_power_import"] = {
            "state": han_data["active_power_p"],
            "attributes": {
                "meter_manufacturer": (
                    stored["ams_active_power_import"]["attributes"][
                        "meter_manufacturer"
                    ]
                ),
                "obis_code": han_data["obis_a_p_p"],
                "meter_type": (
                    stored["ams_active_power_import"]["attributes"]["meter_type"]
                ),
                "meter_serial": stored["ams_active_power_import"]["attributes"][
                    "meter_serial"
                ],
                "unit_of_measurement": "W",
                "icon": "mdi:gauge",
            },
        }
        stored.update(sensor_data)
        return stored, han_data

    han_data["obis_list_version"] = field_type(fields=pkt[32:43], enc=chr)
    han_data["meter_serial"] = field_type(fields=pkt[55:71], enc=chr)
    han_data["meter_type"] = field_type(fields=pkt[83:87], enc=chr, dec=int)
    han_data["meter_type_str"] = METER_TYPE.get(
        field_type(fields=pkt[83:87], enc=chr, dec=int)
    )
    han_data["obis_a_p_p"] = field_type(".", fields=pkt[91:97])
    han_data["active_power_p"] = byte_decode(fields=pkt[98:102])
    sensor_data["ams_active_power_import"] = {
        "state": han_data["active_power_p"],
        "attributes": {
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "obis_code": han_data["obis_a_p_p"],
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "unit_of_measurement": "W",
            "icon": "mdi:gauge",
        },
    }
    han_data["obis_a_p_n"] = field_type(".", fields=pkt[112:118])
    han_data["active_power_n"] = byte_decode(fields=pkt[119:123])
    sensor_data["ams_active_power_export"] = {
        "state": han_data["active_power_n"],
        "attributes": {
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_a_p_n"],
            "unit_of_measurement": "W",
            "icon": "mdi:gauge",
        },
    }
    han_data["obis_r_p_p"] = field_type(".", fields=pkt[133:139])
    han_data["reactive_power_p"] = byte_decode(fields=pkt[140:144])
    sensor_data["ams_reactive_power_import"] = {
        "state": han_data["reactive_power_p"],
        "attributes": {
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_r_p_p"],
            "unit_of_measurement": "VAr",
            "icon": "mdi:gauge",
        },
    }
    han_data["obis_r_p_n"] = field_type(".", fields=pkt[154:160])
    han_data["reactive_power_n"] = byte_decode(fields=pkt[161:165])
    sensor_data["ams_reactive_power_export"] = {
        "state": han_data["reactive_power_n"],
        "attributes": {
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_r_p_n"],
            "unit_of_measurement": "VAr",
            "icon": "mdi:gauge",
        },
    }
    han_data["obis_c_l1"] = field_type(".", fields=pkt[175:181])
    han_data["current_l1"] = byte_decode(fields=pkt[182:184], count=2) / 10
    sensor_data["ams_current_l1"] = {
        "state": han_data["current_l1"],
        "attributes": {
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_c_l1"],
            "unit_of_measurement": "A",
            "icon": "mdi:current-ac",
        },
    }

    if (list_type is LIST_TYPE_SHORT_3PH_3W or
            list_type is LIST_TYPE_LONG_3PH_3W):

        han_data["obis_c_l3"] = field_type(".", fields=pkt[194:200])
        han_data["current_l3"] = byte_decode(fields=pkt[201:203], count=2) / 10
        sensor_data["ams_current_l3"] = {
            "state": han_data["current_l3"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_c_l3"],
                "unit_of_measurement": "A",
                "icon": "mdi:current-ac",
            },
        }
        han_data["obis_v_l1"] = field_type(".", fields=pkt[213:219])
        han_data["voltage_l1"] = byte_decode(fields=pkt[220:222], count=2) / 10
        sensor_data["ams_voltage_l1"] = {
            "state": han_data["voltage_l1"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l1"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        han_data["obis_v_l2"] = field_type(".", fields=pkt[232:238])
        han_data["voltage_l2"] = byte_decode(fields=pkt[239:241], count=2) / 10
        sensor_data["ams_voltage_l2"] = {
            "state": han_data["voltage_l2"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l2"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        han_data["obis_v_l3"] = field_type(".", fields=pkt[251:257])
        han_data["voltage_l3"] = byte_decode(fields=pkt[258:260], count=2) / 10
        sensor_data["ams_voltage_l3"] = {
            "state": han_data["voltage_l3"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l3"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        if list_type is LIST_TYPE_LONG_3PH_3W:
            meter_date_time_year = byte_decode(fields=pkt[278:280], count=2)
            meter_date_time_month = pkt[280]
            meter_date_time_date = pkt[281]
            han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[282])
            meter_date_time_hour = str(pkt[283]).zfill(2)
            meter_date_time_minute = str(pkt[284]).zfill(2)
            meter_date_time_seconds = str(pkt[285]).zfill(2)
            han_data["meter_date_time"] = (
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
            han_data["obis_a_e_p"] = field_type(".", fields=pkt[294:300])
            han_data["active_energy_p"] = byte_decode(fields=pkt[301:305]) / 100
            sensor_data["ams_active_energy_import"] = {
                "state": han_data["active_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_p"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_n"] = field_type(".", fields=pkt[315:321])
            han_data["active_energy_n"] = byte_decode(fields=pkt[322:326]) / 100
            sensor_data["ams_active_energy_export"] = {
                "state": han_data["active_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_n"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_p"] = field_type(".", fields=pkt[336:342])
            han_data["reactive_energy_p"] = byte_decode(fields=pkt[343:347]) / 100
            sensor_data["ams_reactive_energy_import"] = {
                "state": han_data["reactive_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_n"] = field_type(".", fields=pkt[357:363])
            han_data["reactive_energy_n"] = byte_decode(fields=pkt[364:368]) / 100
            sensor_data["ams_reactive_energy_export"] = {
                "state": han_data["reactive_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_n"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }

    if list_type is LIST_TYPE_SHORT_3PH or list_type is LIST_TYPE_LONG_3PH:

        han_data["obis_c_l2"] = field_type(".", fields=pkt[194:200])
        han_data["current_l2"] = byte_decode(fields=pkt[201:203], count=2) / 10
        sensor_data["ams_current_l2"] = {
            "state": han_data["current_l2"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_c_l2"],
                "unit_of_measurement": "A",
                "icon": "mdi:current-ac",
            },
        }
        han_data["obis_c_l3"] = field_type(".", fields=pkt[213:219])
        han_data["current_l3"] = byte_decode(fields=pkt[220:222], count=2) / 10
        sensor_data["ams_current_l3"] = {
            "state": han_data["current_l3"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_c_l3"],
                "unit_of_measurement": "A",
                "icon": "mdi:current-ac",
            },
        }
        han_data["obis_v_l1"] = field_type(".", fields=pkt[232:238])
        han_data["voltage_l1"] = byte_decode(fields=pkt[239:241], count=2) / 10
        sensor_data["ams_voltage_l1"] = {
            "state": han_data["voltage_l1"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l1"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        han_data["obis_v_l2"] = field_type(".", fields=pkt[251:257])
        han_data["voltage_l2"] = byte_decode(fields=pkt[258:260], count=2) / 10
        sensor_data["ams_voltage_l2"] = {
            "state": han_data["voltage_l2"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l2"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        han_data["obis_v_l3"] = field_type(".", fields=pkt[270:276])
        han_data["voltage_l3"] = byte_decode(fields=pkt[277:279], count=2) / 10
        sensor_data["ams_voltage_l3"] = {
            "state": han_data["voltage_l3"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l3"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }
        if list_type is LIST_TYPE_LONG_3PH:
            meter_date_time_year = byte_decode(fields=pkt[297:299], count=2)
            meter_date_time_month = pkt[299]
            meter_date_time_date = pkt[300]
            han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[301])
            meter_date_time_hour = str(pkt[302]).zfill(2)
            meter_date_time_minute = str(pkt[303]).zfill(2)
            meter_date_time_seconds = str(pkt[304]).zfill(2)
            han_data["meter_date_time"] = (
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
            han_data["obis_a_e_p"] = field_type(".", fields=pkt[313:319])
            han_data["active_energy_p"] = byte_decode(fields=pkt[320:324]) / 100
            sensor_data["ams_active_energy_import"] = {
                "state": han_data["active_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_p"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_n"] = field_type(".", fields=pkt[334:340])
            han_data["active_energy_n"] = byte_decode(fields=pkt[341:345]) / 100
            sensor_data["ams_active_energy_export"] = {
                "state": han_data["active_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_n"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_p"] = field_type(".", fields=pkt[355:361])
            han_data["reactive_energy_p"] = byte_decode(fields=pkt[362:366]) / 100
            sensor_data["ams_reactive_energy_import"] = {
                "state": han_data["reactive_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_n"] = field_type(".", fields=pkt[376:382])
            han_data["reactive_energy_n"] = byte_decode(fields=pkt[383:387]) / 100
            sensor_data["ams_reactive_energy_export"] = {
                "state": han_data["reactive_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_n"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }

    if list_type is LIST_TYPE_SHORT_1PH or list_type is LIST_TYPE_LONG_1PH:
        han_data["obis_v_l1"] = field_type(".", fields=pkt[194:200])
        han_data["voltage_l1"] = byte_decode(fields=pkt[201:203], count=2) / 10
        sensor_data["ams_voltage_l1"] = {
            "state": han_data["voltage_l1"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l1"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash",
            },
        }

        if list_type is LIST_TYPE_LONG_1PH:
            meter_date_time_year = byte_decode(fields=pkt[221:223], count=2)
            meter_date_time_month = pkt[223]
            meter_date_time_date = pkt[224]
            han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[225])
            meter_date_time_hour = str(pkt[226]).zfill(2)
            meter_date_time_minute = str(pkt[227]).zfill(2)
            meter_date_time_seconds = str(pkt[228]).zfill(2)
            han_data["meter_date_time"] = (
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
            han_data["obis_a_e_p"] = field_type(".", fields=pkt[237:243])
            han_data["active_energy_p"] = byte_decode(fields=pkt[244:248]) / 100
            sensor_data["ams_active_energy_import"] = {
                "state": han_data["active_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_p"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_n"] = field_type(".", fields=pkt[258:264])
            han_data["active_energy_n"] = byte_decode(fields=pkt[265:269]) / 100
            sensor_data["ams_active_energy_export"] = {
                "state": han_data["active_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_n"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_p"] = field_type(".", fields=pkt[279:285])
            han_data["reactive_energy_p"] = byte_decode(fields=pkt[286:290]) / 100
            sensor_data["ams_reactive_energy_import"] = {
                "state": han_data["reactive_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_p"],
                    "unit_of_measurement": "kVAh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_n"] = field_type(".", fields=pkt[300:306])
            han_data["reactive_energy_n"] = byte_decode(fields=pkt[307:311]) / 100
            sensor_data["ams_reactive_energy_export"] = {
                "state": han_data["reactive_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": han_data["obis_list_version"].title(),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_n"],
                    "unit_of_measurement": "kVAh",
                    "icon": "mdi:gauge",
                },
            }

    stored.update(sensor_data)
    return stored, han_data


def test_valid_data(data):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 397 or len(data) < 44:
        _LOGGER.debug("Invalid packet size %s", len(data))
        return False

    if not data[0] and data[-1] == FRAME_FLAG:
        _LOGGER.debug(
            "%s Recieved %s bytes of %s data",
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
        _LOGGER.debug("Data does not start with %s: %s", DATA_FLAG, data[9:13])
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
