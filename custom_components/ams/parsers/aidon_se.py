"""
Decode for Swedish HAN Aidon.

This module will decode the incoming message from Mbus serial.
"""
import logging
from pprint import pprint
from datetime import datetime
from crccheck.crc import CrcX25
from custom_components.ams import const
from . import byte_decode, field_type


_LOGGER = logging.getLogger(__name__)


def new_parse_data(stored, data):
    """Parse the incoming data"""
    sensor_data = {}
    han_data = {}
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    list_type = pkt[19]
    han_data["list_type"] = list_type
    _LOGGER.debug("list_type is %s", list_type)

    for key in const.name_obis_map:
        if len(const.name_obis_map[key]) == 2:
            for item in const.name_obis_map[key]:
                for i in range(len(pkt)):
                    if pkt[i:i + len(item)] == item:
                        # Double-long-unsigned construct
                        if pkt[i + len(item)] == 6:
                            v_start = i + len(item) + 1
                            v_stop = v_start + 4
                            print(key, item, (i, i + len(
                                item)), (pkt[(i + len(item))]), "Double")
                            print("Value_double 6: ", byte_decode(
                                fields=pkt[v_start:v_stop]) /
                                  const.SENSOR_SCALER.get(key), v_start,
                                  v_stop)
                        # Date time construct
                        elif pkt[i + len(item)] == 9:
                            v_start = i + len(item) + 2
                            v_length = pkt[v_start - 1]
                            v_stop = v_start + v_length
                            meter_date_time_year = byte_decode(fields=pkt[
                                (v_start):(v_start + 2)], count=2)
                            meter_date_time_month = pkt[v_start + 2]
                            meter_date_time_date = pkt[v_start + 3]
                            meter_date_time_day_of_week = (
                                const.WEEKDAY_MAPPING.get(pkt[v_start + 4]))
                            meter_date_time_hour = str(pkt[v_start +
                                                           5]).zfill(2)
                            meter_date_time_minute = str(pkt[v_start +
                                                           6]).zfill(2)
                            meter_date_time_seconds = str(pkt[v_start +
                                                           7]).zfill(2)
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
                            print(key, item, (i, i + len(
                                item)), (pkt[(i + len(item))]), "Double")
                            print(key, item, meter_date_time_year,
                                  meter_date_time_month,
                                  meter_date_time_date,
                                  meter_date_time_day_of_week,
                                  meter_date_time_hour,
                                  meter_date_time_minute,
                                  meter_date_time_seconds,
                                  meter_date_time_str)
                        # Long-signed & Long-unsigned construct
                        elif (pkt[i + len(item)] == 16 or
                                pkt[i + len(item)] == 18):
                            v_start = i + len(item) + 1
                            v_stop = v_start + 2
                            print(key, item, (i, i + len(
                                item)), (pkt[(i + len(item))]), "Double")
                            print("Value_double 16/18: ", (byte_decode(
                                fields=pkt[v_start:v_stop], count=2) / 10),
                                  v_start, v_stop)
                        # Visible string construct
                        elif pkt[i + len(item)] == 10:
                            v_start = i + len(item) + 2
                            v_length = pkt[v_start - 1]
                            v_stop = v_start + v_length
                            print(key, item, (i, i + len(
                                item)), (pkt[(i + len(item))]), "Double")
                            print("Value_double 10: ", (field_type(
                                fields=pkt[v_start:v_stop], enc=chr)),
                                  v_start, v_stop)

        for i in range(len(pkt)):
            if (pkt[i:i + len(const.name_obis_map[key])] ==
                    const.name_obis_map[key]):
                print(key, const.name_obis_map[key], (i, i + len(
                    const.name_obis_map[key])),
                       (pkt[(i + len(const.name_obis_map[key]))]), "Single")
                # Double-long-unsigned construct
                if pkt[i + len(const.name_obis_map[key])] == 6:
                    v_start = i + len(const.name_obis_map[key]) + 1
                    v_stop = v_start + 4
                    print("Value_single 6: ", byte_decode(
                            fields=pkt[v_start:v_stop]) /
                          const.SENSOR_SCALER.get(key), v_start, v_stop)


    #_LOGGER.debug("Found sequence at %s", values_of_key)
# pylint: disable=too-many-statements
def parse_data(stored, data):
    """Parse the incoming data to dict."""
    sensor_data = {}
    han_data = {}
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    list_type = pkt[19]
    han_data["list_type"] = list_type
    _LOGGER.debug("list_type is %s", list_type)


    if (list_type is const.LIST_TYPE_3PH_SE or list_type is
            const.LIST_TYPE_1PH_SE):
        han_data["meter_serial"] = "00"
        han_data["obis_list_version"] = "AIDON_H0001"
        han_data["meter_type_str"] = const.METER_TYPE.get(6484)
        han_data["obis_timedate"] = field_type(".", fields=pkt[24:30])
        meter_date_time_year = byte_decode(fields=pkt[32:34], count=2)
        meter_date_time_month = pkt[34]
        meter_date_time_date = pkt[35]
        han_data["meter_day_of_week"] = const.WEEKDAY_MAPPING.get(pkt[36])
        meter_date_time_hour = str(pkt[37]).zfill(2)
        meter_date_time_minute = str(pkt[38]).zfill(2)
        meter_date_time_seconds = str(pkt[39]).zfill(2)
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
        han_data["obis_a_p_p"] = field_type(".", fields=pkt[48:54])
        han_data["active_power_p"] = byte_decode(fields=pkt[55:59])
        sensor_data["ams_active_power_import"] = {
            "state": han_data["active_power_p"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "obis_code": han_data["obis_a_p_p"],
                "meter_serial": han_data["meter_serial"],
                "unit_of_measurement": "W",
                "icon": "mdi:gauge",
            },
        }
        han_data["obis_a_p_n"] = field_type(".", fields=pkt[69:75])
        han_data["active_power_n"] = byte_decode(fields=pkt[76:80])
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
        han_data["obis_r_p_p"] = field_type(".", fields=pkt[90:96])
        han_data["reactive_power_p"] = byte_decode(fields=pkt[97:102])
        sensor_data["ams_reactive_power_import"] = {
            "state": han_data["reactive_power_p"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_serial": han_data["meter_serial"],
                "meter_type": han_data["meter_type_str"],
                "obis_code": han_data["obis_r_p_p"],
                "unit_of_measurement": "VAr",
                "icon": "mdi:gauge",
            },
        }
        han_data["obis_r_p_n"] = field_type(".", fields=pkt[111:117])
        han_data["reactive_power_n"] = byte_decode(fields=pkt[118:123])
        sensor_data["ams_reactive_power_export"] = {
            "state": han_data["reactive_power_n"],
            "attributes": {
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_serial": han_data["meter_serial"],
                "meter_type": han_data["meter_type_str"],
                "obis_code": han_data["obis_r_p_n"],
                "unit_of_measurement": "VAr",
                "icon": "mdi:gauge",
            },
        }
        han_data["obis_c_l1"] = field_type(".", fields=pkt[132:138])
        han_data["current_l1"] = (
            byte_decode(fields=pkt[139:142], count=2) / 10
        )
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
        if list_type is const.LIST_TYPE_3PH_SE:

            han_data["obis_c_l2"] = field_type(".", fields=pkt[151:157])
            han_data["current_l2"] = (
                byte_decode(fields=pkt[158:161], count=2) / 10
            )
            sensor_data["ams_current_l2"] = {
                "state": han_data["current_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_c_l1"],
                    "unit_of_measurement": "A",
                    "icon": "mdi:current-ac",
                },
            }
            han_data["obis_c_l3"] = field_type(".", fields=pkt[170:176])
            han_data["current_l3"] = (
                byte_decode(fields=pkt[177:180], count=2) / 10
            )
            sensor_data["ams_current_l3"] = {
                "state": han_data["current_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_c_l3"],
                    "unit_of_measurement": "A",
                    "icon": "mdi:current-ac",
                },
            }
            han_data["obis_v_l1"] = field_type(".", fields=pkt[189:195])
            han_data["voltage_l1"] = (
                byte_decode(fields=pkt[196:198], count=2) / 10
            )
            sensor_data["ams_voltage_l1"] = {
                "state": han_data["voltage_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_v_l1"],
                    "unit_of_measurement": "V",
                    "icon": "mdi:flash",
                },
            }
            han_data["obis_v_l2"] = field_type(".", fields=pkt[208:214])
            han_data["voltage_l2"] = (
                byte_decode(fields=pkt[215:217], count=2) / 10
            )
            sensor_data["ams_voltage_l2"] = {
                "state": han_data["voltage_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_v_l2"],
                    "unit_of_measurement": "V",
                    "icon": "mdi:flash",
                },
            }
            han_data["obis_v_l3"] = field_type(".", fields=pkt[227:233])
            han_data["voltage_l3"] = (
                byte_decode(fields=pkt[234:236], count=2) / 10
            )
            sensor_data["ams_voltage_l3"] = {
                "state": han_data["voltage_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_v_l3"],
                    "unit_of_measurement": "V",
                    "icon": "mdi:flash",
                },
            }
            han_data["obis_a_p_p_l1"] = field_type(".", fields=pkt[246:252])
            han_data["active_power_p_l1"] = byte_decode(fields=pkt[253:257])
            sensor_data["ams_active_power_import_l1"] = {
                "state": han_data["active_power_p_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_p_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_n_l1"] = field_type(".", fields=pkt[267:273])
            han_data["active_power_n_l1"] = byte_decode(fields=pkt[274:278])
            sensor_data["ams_active_power_export_l1"] = {
                "state": han_data["active_power_n_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_n_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_p_l1"] = field_type(".", fields=pkt[288:294])
            han_data["reactive_power_p_l1"] = byte_decode(fields=pkt[295:299])
            sensor_data["ams_reactive_power_import_l1"] = {
                "state": han_data["reactive_power_p_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_p_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_n_l1"] = field_type(".", fields=pkt[309:315])
            han_data["reactive_power_n_l1"] = byte_decode(fields=pkt[316:320])
            sensor_data["ams_reactive_power_export_l1"] = {
                "state": han_data["reactive_power_n_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_n_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_p_l2"] = field_type(".", fields=pkt[330:336])
            han_data["active_power_p_l2"] = byte_decode(fields=pkt[337:341])
            sensor_data["ams_active_power_import_l2"] = {
                "state": han_data["active_power_p_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_p_l2"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_n_l2"] = field_type(".", fields=pkt[351:357])
            han_data["active_power_n_l2"] = byte_decode(fields=pkt[358:362])
            sensor_data["ams_active_power_export_l2"] = {
                "state": han_data["active_power_n_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_n_l2"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_p_l2"] = field_type(".", fields=pkt[372:378])
            han_data["reactive_power_p_l2"] = byte_decode(fields=pkt[379:383])
            sensor_data["ams_reactive_power_import_l2"] = {
                "state": han_data["reactive_power_p_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_p_l2"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_n_l2"] = field_type(".", fields=pkt[393:399])
            han_data["reactive_power_n_l2"] = byte_decode(fields=pkt[400:404])
            sensor_data["ams_reactive_power_export_l2"] = {
                "state": han_data["reactive_power_n_l2"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_n_l2"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_p_l3"] = field_type(".", fields=pkt[414:420])
            han_data["active_power_p_l3"] = byte_decode(fields=pkt[421:425])
            sensor_data["ams_active_power_import_l3"] = {
                "state": han_data["active_power_p_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_p_l3"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_n_l3"] = field_type(".", fields=pkt[435:441])
            han_data["active_power_n_l3"] = byte_decode(fields=pkt[442:446])
            sensor_data["ams_active_power_export_l3"] = {
                "state": han_data["active_power_n_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_n_l3"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_p_l3"] = field_type(".", fields=pkt[456:462])
            han_data["reactive_power_p_l3"] = byte_decode(fields=pkt[463:467])
            sensor_data["ams_reactive_power_import_l3"] = {
                "state": han_data["reactive_power_p_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_p_l3"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_n_l3"] = field_type(".", fields=pkt[477:483])
            han_data["reactive_power_n_l3"] = byte_decode(fields=pkt[484:488])
            sensor_data["ams_reactive_power_export_l3"] = {
                "state": han_data["reactive_power_n_l3"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_n_l3"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_p"] = field_type(".", fields=pkt[498:504])
            han_data["active_energy_p"] = (
                byte_decode(fields=pkt[504:508]) / 100
            )
            sensor_data["ams_active_energy_import"] = {
                "state": han_data["active_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_p"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_n"] = field_type(".", fields=pkt[519:525])
            han_data["active_energy_n"] = (
                byte_decode(fields=pkt[526:530]) / 100
            )
            sensor_data["ams_active_energy_export"] = {
                "state": han_data["active_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_n"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_p"] = field_type(".", fields=pkt[540:546])
            han_data["reactive_energy_p"] = (
                byte_decode(fields=pkt[547:551]) / 100
            )
            sensor_data["ams_reactive_energy_import"] = {
                "state": han_data["reactive_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_n"] = field_type(".", fields=pkt[561:567])
            han_data["reactive_energy_n"] = (
                byte_decode(fields=pkt[568:572]) / 100
            )
            sensor_data["ams_reactive_energy_export"] = {
                "state": han_data["reactive_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_n"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
        if list_type is const.LIST_TYPE_1PH_SE:
            han_data["obis_v_l1"] = field_type(".", fields=pkt[151:157])
            han_data["voltage_l1"] = (
                byte_decode(fields=pkt[158:161], count=2) / 10
            )
            sensor_data["ams_voltage_l1"] = {
                "state": han_data["voltage_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_v_l1"],
                    "unit_of_measurement": "V",
                    "icon": "mdi:flash",
                },
            }
            han_data["obis_a_p_p_l1"] = field_type(".", fields=pkt[170:176])
            han_data["active_power_p_l1"] = byte_decode(fields=pkt[177:181])
            sensor_data["ams_active_power_import_l1"] = {
                "state": han_data["active_power_p_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_p_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_p_n_l1"] = field_type(".", fields=pkt[191:197])
            han_data["active_power_n_l1"] = byte_decode(fields=pkt[198:202])
            sensor_data["ams_active_power_export_l1"] = {
                "state": han_data["active_power_n_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_a_p_n_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "W",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_p_l1"] = field_type(".", fields=pkt[212:218])
            han_data["reactive_power_p_l1"] = byte_decode(fields=pkt[219:223])
            sensor_data["ams_reactive_power_import_l1"] = {
                "state": han_data["reactive_power_p_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_p_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_p_n_l1"] = field_type(".", fields=pkt[233:239])
            han_data["reactive_power_n_l1"] = byte_decode(fields=pkt[240:244])
            sensor_data["ams_reactive_power_export_l1"] = {
                "state": han_data["reactive_power_n_l1"],
                "attributes": {
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "obis_code": han_data["obis_r_p_n_l1"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "VAr",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_p"] = field_type(".", fields=pkt[254:260])
            han_data["active_energy_p"] = (
                byte_decode(fields=pkt[261:265]) / 100
            )
            sensor_data["ams_active_energy_import"] = {
                "state": han_data["active_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_p"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_a_e_n"] = field_type(".", fields=pkt[275:281])
            han_data["active_energy_n"] = (
                byte_decode(fields=pkt[282:286]) / 100
            )
            sensor_data["ams_active_energy_export"] = {
                "state": han_data["active_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_a_e_n"],
                    "unit_of_measurement": "kWh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_p"] = field_type(".", fields=pkt[296:302])
            han_data["reactive_energy_p"] = (
                byte_decode(fields=pkt[303:307]) / 100
            )
            sensor_data["ams_reactive_energy_import"] = {
                "state": han_data["reactive_energy_p"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
            han_data["obis_r_e_n"] = field_type(".", fields=pkt[317:323])
            han_data["reactive_energy_n"] = (
                byte_decode(fields=pkt[324:328]) / 100
            )
            sensor_data["ams_reactive_energy_export"] = {
                "state": han_data["reactive_energy_n"],
                "attributes": {
                    "meter_timestamp": han_data["meter_date_time"],
                    "meter_manufacturer": (
                        han_data["obis_list_version"].title()
                    ),
                    "meter_type": han_data["meter_type_str"],
                    "meter_serial": han_data["meter_serial"],
                    "obis_code": han_data["obis_r_e_n"],
                    "unit_of_measurement": "kVArh",
                    "icon": "mdi:gauge",
                },
            }
    stored.update(sensor_data)
    return stored, han_data


def test_valid_data(data):
    """"Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 581 or len(data) < 44:
        _LOGGER.debug("Invalid packet size %s", len(data))
        return False

    if not data[0] and data[-1] == const.FRAME_FLAG:
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

    if data[9:13] != const.DATA_FLAG:
        _LOGGER.debug("Data does not start with %s: %s", const.DATA_FLAG,
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
