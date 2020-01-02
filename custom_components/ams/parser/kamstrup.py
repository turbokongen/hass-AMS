"""
Decode for han_kamstrup.

This module will decode the incoming message from Mbus serial.
"""

import logging
from datetime import datetime
from crccheck.crc import CrcX25


from .const import (
    DATA_FLAG_LIST,
    FRAME_FLAG,
    LIST_TYPE_SHORT_1PH,
    LIST_TYPE_LONG_1PH,
    LIST_TYPE_SHORT_3PH,
    LIST_TYPE_LONG_3PH,
    WEEKDAY_MAPPING
)

# Lets just leave this for now, its just used here.
METER_TYPE = {
    6861111: "Omnipower 1 Phase Direct meter",
    6841121: "Omnipower 3 Phase 3-Wire Direct meter",
    6841131: "Omnipower 3 Phase 4-Wire Direct meter",
    6851121: "Omnipower 3 Phase CT 3-Wire Direct meter",
    6851131: "Omnipower 3 Phase CT 4-Wire Direct meter"
}

_LOGGER = logging.getLogger(__name__)


def p_type(default="", it=None, type_=str, r_type=None):
    """Helper to parse stuff to a result."""
    res = default.join(type_(i) for i in it)
    if r_type:
        return r_type(res)
    return res


def parse_data(stored, data):
    """Parse the incoming data to dict."""
    sensor_data = {}
    han_data = stored
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    date_time_year = pkt[17] << 8 | pkt[18]
    date_time_month = pkt[19]
    date_time_date = pkt[20]
    date_time_hour = str(pkt[22]).zfill(2)
    date_time_minute = str(pkt[23]).zfill(2)
    date_time_seconds = str(pkt[24]).zfill(2)
    date_time_str = (str(date_time_year) +
                     "-" + str(date_time_month) +
                     "-" + str(date_time_date) +
                     " " + date_time_hour +
                     ":" + date_time_minute +
                     ":" + date_time_seconds)
    han_data["date_time"] = date_time_str
    han_data["day_of_week"] = WEEKDAY_MAPPING.get(pkt[21])
    list_type = pkt[30]
    han_data["list_type"] = list_type
    han_data["obis_list_version"] = p_type(type_=chr, it=pkt[33:47])

    han_data["obis_m_s"] = p_type(".", it=pkt[49:54])
    han_data["meter_serial"] = p_type(type_=chr, it=pkt[57:73])
    han_data["obis_m_t"] = p_type(".", pkt[75:80])
    # This one seems to be emtpy also in the orginal impl.
    # Check this: TODO
    han_data["meter_type"] = p_type(type_=chr, it=pkt[83:100])
    han_data["meter_type_str"] = METER_TYPE.get(p_type(type_=chr, it=pkt[83:90], r_type=int))
    han_data["obis_a_p_p"] = p_type(".", pkt[103:109])
    han_data["active_power_p"] = (pkt[110] << 24 |
                                  pkt[111] << 16 |
                                  pkt[112] << 8 |
                                  pkt[113])
    sensor_data["ams_active_power_import"] = {
        "state": han_data["active_power_p"],
        "attributes": {
            "timestamp": han_data["date_time"],
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_a_p_p"],
            "unit_of_measurement": "W",
            "icon": "mdi:gauge"
            }
        }

    han_data["obis_a_p_n"] = p_type(".", pkt[116:122])
    han_data["active_power_n"] = (pkt[123] << 24 |
                                  pkt[124] << 16 |
                                  pkt[125] << 8 |
                                  pkt[126])
    sensor_data["ams_active_power_export"] = {
        "state": han_data["active_power_n"],
        "attributes": {
            "timestamp": han_data["date_time"],
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_a_p_n"],
            "unit_of_measurement": "W",
            "icon": "mdi:gauge"
            }
        }
    han_data["obis_r_p_p"] = p_type(".", pkt[129:135])
    han_data["reactive_power_p"] = (pkt[136] << 24 |
                                    pkt[137] << 16 |
                                    pkt[138] << 8 |
                                    pkt[139])
    sensor_data["ams_reactive_power_import"] = {
        "state": han_data["reactive_power_p"],
        "attributes": {
            "timestamp": han_data["date_time"],
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_r_p_p"],
            "unit_of_measurement": "VAr",
            "icon": "mdi:gauge"
            }
        }

    han_data["obis_r_p_n"] = p_type(".", pkt[142:148])
    han_data["reactive_power_n"] = (pkt[149] << 24 |
                                    pkt[150] << 16 |
                                    pkt[151] << 8 |
                                    pkt[152])
    sensor_data["ams_reactive_power_export"] = {
        "state": han_data["reactive_power_n"],
        "attributes": {
            "timestamp": han_data["date_time"],
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_r_p_n"],
            "unit_of_measurement": "VAr",
            "icon": "mdi:gauge"
            }
        }

    han_data["obis_c_l1"] = p_type(".", pkt[155:161])
    han_data["current_l1"] = (pkt[162] << 24 |
                              pkt[163] << 16 |
                              pkt[164] << 8 |
                              pkt[165]) / 100
    sensor_data["ams_current_l1"] = {
        "state": han_data["current_l1"],
        "attributes": {
            "timestamp": han_data["date_time"],
            "meter_manufacturer": han_data["obis_list_version"].title(),
            "meter_type": han_data["meter_type_str"],
            "meter_serial": han_data["meter_serial"],
            "obis_code": han_data["obis_c_l1"],
            "unit_of_measurement": "A",
            "icon": "mdi:current-ac"
            }
        }

    if (list_type is LIST_TYPE_SHORT_3PH or
            list_type is LIST_TYPE_LONG_3PH):

        han_data["obis_c_l2"] = p_type(".", pkt[168:174])
        han_data["current_l2"] = (pkt[175] << 24 |
                                  pkt[176] << 16 |
                                  pkt[177] << 8 |
                                  pkt[178]) / 100
        sensor_data["ams_current_l2"] = {
            "state": han_data["current_l2"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_c_l2"],
                "unit_of_measurement": "A",
                "icon": "mdi:current-ac"
                }
            }
        han_data["obis_c_l3"] = p_type(".", pkt[181:187])
        han_data["current_l3"] = (pkt[188] << 24 |
                                  pkt[189] << 16 |
                                  pkt[190] << 8 |
                                  pkt[191]) / 100
        sensor_data["ams_current_l3"] = {
            "state": han_data["current_l3"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_c_l3"],
                "unit_of_measurement": "A",
                "icon": "mdi:current-ac"
                }
            }
        han_data["obis_v_l1"] = p_type(".", pkt[194:200])
        han_data["voltage_l1"] = (pkt[201] << 8 |
                                  pkt[202])
        sensor_data["ams_voltage_l1"] = {
            "state": han_data["voltage_l1"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l1"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash"
                }
            }
        han_data["obis_v_l2"] = p_type(".", pkt[205:211])
        han_data["voltage_l2"] = (pkt[212] << 8 |
                                  pkt[213])
        sensor_data["ams_voltage_l2"] = {
            "state": han_data["voltage_l2"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l2"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash"
                }
            }
        han_data["obis_v_l3"] = p_type(".", pkt[216:222])
        han_data["voltage_l3"] = (pkt[223] << 8 |
                                  pkt[224])
        sensor_data["ams_voltage_l3"] = {
            "state": han_data["voltage_l3"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l3"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash"
                }
            }

    if (list_type == LIST_TYPE_SHORT_1PH or
            list_type == LIST_TYPE_LONG_1PH):
        han_data["obis_v_l1"] = p_type(".", pkt[168:174])
        han_data["voltage_l1"] = (pkt[175] << 8 |
                                  pkt[176])
        sensor_data["ams_voltage_l1"] = {
            "state": han_data["voltage_l1"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_v_l1"],
                "unit_of_measurement": "V",
                "icon": "mdi:flash"
                }
            }

    if list_type == LIST_TYPE_LONG_1PH:
        han_data["obis_meter_date_time"] = p_type(".", pkt[179:185])
        meter_date_time_year = pkt[187] << 8 | pkt[188]
        meter_date_time_month = pkt[189]
        meter_date_time_date = pkt[190]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[191])
        meter_date_time_hour = str(pkt[192]).zfill(2)
        meter_date_time_minute = str(pkt[193]).zfill(2)
        meter_date_time_seconds = str(pkt[194]).zfill(2)
        han_data["meter_date_time"] = f"{meter_date_time_year}-{meter_date_time_month}-{meter_date_time_date} {meter_date_time_hour}:{meter_date_time_minute}:{meter_date_time_seconds}"
        # han_data["meter_date_time"] = (str(meter_date_time_year) +
        #                                "-" + str(meter_date_time_month) +
        #                                "-" + str(meter_date_time_date) +
        #                                " " + meter_date_time_hour +
        #                                ":" + meter_date_time_minute +
        #                                ":" + meter_date_time_seconds)
        han_data["obis_a_e_p"] = p_type(".", pkt[201:207])
        han_data["active_energy_p"] = (pkt[208] << 24 |
                                       pkt[209] << 16 |
                                       pkt[210] << 8 |
                                       pkt[211]) / 100
        sensor_data["ams_active_energy_import"] = {
            "state": han_data["active_energy_p"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_a_e_p"],
                "unit_of_measurement": "kWh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_a_e_n"] = p_type(".", pkt[214:220])
        han_data["active_energy_n"] = (pkt[221] << 24 |
                                       pkt[222] << 16 |
                                       pkt[223] << 8 |
                                       pkt[224]) / 100
        sensor_data["ams_active_energy_export"] = {
            "state": han_data["active_energy_n"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_a_e_n"],
                "unit_of_measurement": "kWh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_r_e_p"] = p_type(".", pkt[227:233])
        han_data["reactive_energy_p"] = (pkt[234] << 24 |
                                         pkt[235] << 16 |
                                         pkt[236] << 8 |
                                         pkt[237]) / 100
        sensor_data["ams_reactive_energy_import"] = {
            "state": han_data["reactive_energy_p"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_r_e_p"],
                "unit_of_measurement": "kVAh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_r_e_n"] = p_type(".", pkt[240:246])
        han_data["reactive_energy_n"] = (pkt[247] << 24 |
                                         pkt[248] << 16 |
                                         pkt[249] << 8 |
                                         pkt[250]) / 100
        sensor_data["ams_reactive_energy_export"] = {
            "state": han_data["reactive_energy_n"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_r_e_n"],
                "unit_of_measurement": "kVAh",
                "icon": "mdi:gauge"
                }
            }

    if list_type == LIST_TYPE_LONG_3PH:
        han_data["obis_meter_date_time"] = p_type(".", pkt[227:233])
        meter_date_time_year = pkt[235] << 8 | pkt[236]
        meter_date_time_month = pkt[237]
        meter_date_time_date = pkt[238]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[239])
        meter_date_time_hour = str(pkt[240]).zfill(2)
        meter_date_time_minute = str(pkt[241]).zfill(2)
        meter_date_time_seconds = str(pkt[242]).zfill(2)
        # lets skip this for now.. didnt think the fstring was prettier
        # even if its faster..
        han_data["meter_date_time"] = (str(meter_date_time_year) +
                                       "-" + str(meter_date_time_month) +
                                       "-" + str(meter_date_time_date) +
                                       " " + meter_date_time_hour +
                                       ":" + meter_date_time_minute +
                                       ":" + meter_date_time_seconds)
        han_data["obis_a_e_p"] = p_type(".", pkt[249:255])
        han_data["active_energy_p"] = (pkt[256] << 24 |
                                       pkt[257] << 16 |
                                       pkt[258] << 8 |
                                       pkt[259]) / 100
        sensor_data["ams_active_energy_import"] = {
            "state": han_data["active_energy_p"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_a_e_p"],
                "unit_of_measurement": "kWh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_a_e_n"] = p_type(".", pkt[262:268])
        han_data["active_energy_n"] = (pkt[269] << 24 |
                                       pkt[270] << 16 |
                                       pkt[271] << 8 |
                                       pkt[272]) / 100
        sensor_data["ams_active_energy_export"] = {
            "state": han_data["active_energy_n"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_a_e_n"],
                "unit_of_measurement": "kWh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_r_e_p"] = p_type(".", pkt[275:281])
        han_data["reactive_energy_p"] = (pkt[282] << 24 |
                                         pkt[283] << 16 |
                                         pkt[284] << 8 |
                                         pkt[285]) / 100
        sensor_data["ams_reactive_energy_import"] = {
            "state": han_data["reactive_energy_p"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_r_e_p"],
                "unit_of_measurement": "kVAh",
                "icon": "mdi:gauge"
                }
            }
        han_data["obis_r_e_n"] = p_type(".", pkt[288:294])
        han_data["reactive_energy_n"] = (pkt[295] << 24 |
                                         pkt[296] << 16 |
                                         pkt[297] << 8 |
                                         pkt[298]) / 100
        sensor_data["ams_reactive_energy_export"] = {
            "state": han_data["reactive_energy_n"],
            "attributes": {
                "timestamp": han_data["date_time"],
                "meter_timestamp": han_data["meter_date_time"],
                "meter_manufacturer": han_data["obis_list_version"].title(),
                "meter_type": han_data["meter_type_str"],
                "meter_serial": han_data["meter_serial"],
                "obis_code": han_data["obis_r_e_n"],
                "unit_of_measurement": "kVAh",
                "icon": "mdi:gauge"
                }
            }
    return sensor_data


def test_valid_data(data):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 302 or len(data) < 180:
        _LOGGER.debug("Invalid packet size %s", len(data))
        return False

    if not data[0] and data[-1] == list(FRAME_FLAG):
        _LOGGER.debug("%s Recieved %s bytes of %s data",
                        datetime.now().isoformat(),
                        len(data), False)
        return False

    header_checksum = CrcX25.calc(bytes(data[1:6]))
    read_header_checksum = (data[7] << 8 | data[6])

    if header_checksum != read_header_checksum:
        _LOGGER.debug("Invalid header CRC check")
        return False

    frame_checksum = CrcX25.calc(bytes(data[1:-3]))
    read_frame_checksum = (data[-2] << 8 | data[-3])

    if frame_checksum != read_frame_checksum:
        _LOGGER.debug("Invalid frame CRC check")
        return False

    if data[8:12] != DATA_FLAG_LIST:
        _LOGGER.debug("Data does not start with %s: %s",
                        DATA_FLAG_LIST, data[8:12])
        return False

    packet_size = len(data)
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2

    if packet_size != read_packet_size:
        _LOGGER.debug(
            "Packet size does not match read packet size: %s : %s",
            packet_size, read_packet_size)
        return False

    return True
