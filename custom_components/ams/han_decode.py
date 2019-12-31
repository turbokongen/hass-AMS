"""
Decode for han_kamstrup.

This module will decode the incoming message from Mbus serial.
"""

import logging
from datetime import datetime
from crccheck.crc import CrcX25

DATA_FLAG = [230, 231, 0, 15]
FRAME_FLAG = b'\x7e'
LIST_TYPE_SHORT_1PH = 17
LIST_TYPE_LONG_1PH = 27
LIST_TYPE_SHORT_3PH = 25
LIST_TYPE_LONG_3PH = 35

WEEKDAY_MAPPING = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}

METER_TYPE = {
    6861111: 'Omnipower 1 Phase Direct meter',
    6841121: 'Omnipower 3 Phase 3-Wire Direct meter',
    6841131: 'Omnipower 3 Phase 4-Wire Direct meter',
    6851121: 'Omnipower 3 Phase CT 3-Wire Direct meter',
    6851131: 'Omnipower 3 Phase CT 4-Wire Direct meter'
}

_LOGGER = logging.getLogger(__name__)
# pylint: disable=too-many-locals, too-many-statements


def parse_data(stored, data):
    """Parse the incoming data to dict."""
    sensor_data = {}
    han_data = stored
    pkt = data
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2
    han_data["packet_size"] = read_packet_size
    date_time_year = byte_decode(fields=pkt[17:19], count=2)
    date_time_month = pkt[19]
    date_time_date = pkt[20]
    date_time_hour = str(pkt[22]).zfill(2)
    date_time_minute = str(pkt[23]).zfill(2)
    date_time_seconds = str(pkt[24]).zfill(2)
    date_time_str = (str(date_time_year) +
                     '-' + str(date_time_month) +
                     '-' + str(date_time_date) +
                     ' ' + date_time_hour +
                     ':' + date_time_minute +
                     ':' + date_time_seconds)
    han_data["date_time"] = date_time_str
    han_data["day_of_week"] = WEEKDAY_MAPPING.get(pkt[21])
    list_type = pkt[30]
    han_data["list_type"] = list_type
    han_data["obis_list_version"] = field_type(fields=pkt[33:47], enc=chr)
    han_data["obis_m_s"] = field_type(".", fields=pkt[49:54])
    han_data["meter_serial"] = field_type(fields=pkt[57:73], enc=chr)
    han_data["obis_m_t"] = field_type(".", fields=pkt[75:80])
    han_data["meter_type"] = field_type(fields=pkt[83:101], enc=chr)
    han_data["meter_type_str"] = METER_TYPE.get(
        field_type(fields=pkt[83:90], enc=chr, dec=int))
    han_data["obis_a_p_p"] = field_type(".", fields=pkt[103:109])
    han_data["active_power_p"] = byte_decode(fields=pkt[110:114])
    sensor_data["ams_active_power_import"] = {
        'state': han_data["active_power_p"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_a_p_p"],
            'unit_of_measurement': 'W',
            'icon': 'mdi:gauge'
            }
        }

    han_data["obis_a_p_n"] = field_type(".", fields=pkt[116:122])
    han_data["active_power_n"] = byte_decode(fields=pkt[123:127])
    sensor_data["ams_active_power_export"] = {
        'state': han_data["active_power_n"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_a_p_n"],
            'unit_of_measurement': 'W',
            'icon': 'mdi:gauge'
            }
        }
    han_data["obis_r_p_p"] = field_type(".", fields=pkt[129:135])
    han_data["reactive_power_p"] = byte_decode(fields=pkt[136:140])
    sensor_data["ams_reactive_power_import"] = {
        'state': han_data["reactive_power_p"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_r_p_p"],
            'unit_of_measurement': 'VAr',
            'icon': 'mdi:gauge'
            }
        }
    han_data["obis_r_p_n"] = field_type(".", fields=pkt[142:148])
    han_data["reactive_power_n"] = byte_decode(fields=pkt[149:153])
    sensor_data["ams_reactive_power_export"] = {
        'state': han_data["reactive_power_n"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_r_p_n"],
            'unit_of_measurement': 'VAr',
            'icon': 'mdi:gauge'
            }
        }
    han_data["obis_c_l1"] = field_type(".", fields=pkt[155:161])
    han_data["current_l1"] = byte_decode(fields=pkt[162:166]) / 100
    sensor_data["ams_current_l1"] = {
        'state': han_data["current_l1"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_c_l1"],
            'unit_of_measurement': 'A',
            'icon': 'mdi:current-ac'
            }
        }

    if (list_type is LIST_TYPE_SHORT_3PH or
            list_type is LIST_TYPE_LONG_3PH):
        han_data["obis_c_l2"] = field_type(".", fields=pkt[168:174])
        han_data["current_l2"] = byte_decode(fields=pkt[175:179]) / 100
        sensor_data["ams_current_l2"] = {
            'state': han_data["current_l2"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_c_l2"],
                'unit_of_measurement': 'A',
                'icon': 'mdi:current-ac'
                }
            }
        han_data["obis_c_l3"] = field_type(".", fields=pkt[181:187])
        han_data["current_l3"] = byte_decode(fields=pkt[188:192]) / 100
        sensor_data["ams_current_l3"] = {
            'state': han_data["current_l3"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_c_l3"],
                'unit_of_measurement': 'A',
                'icon': 'mdi:current-ac'
                }
            }
        han_data["obis_v_l1"] = field_type(".", fields=pkt[194:200])
        han_data["voltage_l1"] = byte_decode(fields=pkt[201:203], count=2)
        sensor_data["ams_voltage_l1"] = {
            'state': han_data["voltage_l1"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_v_l1"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }
        han_data["obis_v_l2"] = field_type(".", fields=pkt[205:211])
        han_data["voltage_l2"] = byte_decode(fields=pkt[212:214], count=2)
        sensor_data["ams_voltage_l2"] = {
            'state': han_data["voltage_l2"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_v_l2"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }
        han_data["obis_v_l3"] = field_type(".", fields=pkt[216:222])
        han_data["voltage_l3"] = byte_decode(fields=pkt[223:225], count=2)
        sensor_data["ams_voltage_l3"] = {
            'state': han_data["voltage_l3"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_v_l3"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }

    if (list_type is LIST_TYPE_SHORT_1PH or
            list_type is LIST_TYPE_LONG_1PH):

        han_data["obis_v_l1"] = field_type(".", fields=pkt[168:174])
        han_data["voltage_l1"] = byte_decode(fields=pkt[175:177], count=2)
        sensor_data["ams_voltage_l1"] = {
            'state': han_data["voltage_l1"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_v_l1"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }

    if list_type == LIST_TYPE_LONG_1PH:
        han_data["obis_meter_date_time"] = field_type(".", fields=pkt[179:185])
        meter_date_time_year = byte_decode(fields=pkt[187:189], count=2)
        meter_date_time_month = pkt[189]
        meter_date_time_date = pkt[190]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[191])
        meter_date_time_hour = str(pkt[192]).zfill(2)
        meter_date_time_minute = str(pkt[193]).zfill(2)
        meter_date_time_seconds = str(pkt[194]).zfill(2)
        han_data["meter_date_time"] = (str(meter_date_time_year) +
                                       '-' + str(meter_date_time_month) +
                                       '-' + str(meter_date_time_date) +
                                       ' ' + meter_date_time_hour +
                                       ':' + meter_date_time_minute +
                                       ':' + meter_date_time_seconds)
        han_data["obis_a_e_p"] = field_type(".", fields=pkt[201:207])
        han_data["active_energy_p"] = byte_decode(fields=pkt[208:212]) / 100
        sensor_data["ams_active_energy_import"] = {
            'state': han_data["active_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_a_e_p"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_a_e_n"] = field_type(".", fields=pkt[214:220])
        han_data["active_energy_n"] = byte_decode(fields=pkt[221:225]) / 100
        sensor_data["ams_active_energy_export"] = {
            'state': han_data["active_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_a_e_n"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_r_e_p"] = field_type(".", fields=pkt[227:233])
        han_data["reactive_energy_p"] = byte_decode(fields=pkt[234:238]) / 100
        sensor_data["ams_reactive_energy_import"] = {
            'state': han_data["reactive_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_r_e_p"],
                'unit_of_measurement': 'kVAh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_r_e_n"] = field_type(".", fields=pkt[240:246])
        han_data["reactive_energy_n"] = byte_decode(fields=pkt[247:251]) / 100
        sensor_data["ams_reactive_energy_export"] = {
            'state': han_data["reactive_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_r_e_n"],
                'unit_of_measurement': 'kVAh',
                'icon': 'mdi:gauge'
                }
            }

    if list_type == LIST_TYPE_LONG_3PH:
        han_data["obis_meter_date_time"] = field_type(".", fields=pkt[227:233])
        meter_date_time_year = byte_decode(fields=pkt[235:237], count=2)
        meter_date_time_month = pkt[237]
        meter_date_time_date = pkt[238]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[239])
        meter_date_time_hour = str(pkt[240]).zfill(2)
        meter_date_time_minute = str(pkt[241]).zfill(2)
        meter_date_time_seconds = str(pkt[242]).zfill(2)
        han_data["meter_date_time"] = (str(meter_date_time_year) +
                                       '-' + str(meter_date_time_month) +
                                       '-' + str(meter_date_time_date) +
                                       ' ' + meter_date_time_hour +
                                       ':' + meter_date_time_minute +
                                       ':' + meter_date_time_seconds)
        han_data["obis_a_e_p"] = field_type(".", fields=pkt[249:255])
        han_data["active_energy_p"] = byte_decode(fields=pkt[256:260]) / 100
        sensor_data["ams_active_energy_import"] = {
            'state': han_data["active_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_a_e_p"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_a_e_n"] = field_type(".", fields=pkt[262:268])
        han_data["active_energy_n"] = byte_decode(fields=pkt[269:273]) / 100
        sensor_data["ams_active_energy_export"] = {
            'state': han_data["active_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_a_e_n"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_r_e_p"] = field_type(".", fields=pkt[275:281])
        han_data["reactive_energy_p"] = byte_decode(fields=pkt[282:286]) / 100
        sensor_data["ams_reactive_energy_import"] = {
            'state': han_data["reactive_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_r_e_p"],
                'unit_of_measurement': 'kVAh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["obis_r_e_n"] = field_type(".", fields=pkt[288:294])
        han_data["reactive_energy_n"] = byte_decode(fields=pkt[295:299]) / 100
        sensor_data["ams_reactive_energy_export"] = {
            'state': han_data["reactive_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'obis_code': han_data["obis_r_e_n"],
                'unit_of_measurement': 'kVAh',
                'icon': 'mdi:gauge'
                }
            }
    return sensor_data


def field_type(default="", fields=None, enc=str, dec=None):
    """Obis/data field decoder/encoder."""
    data = default.join(enc(i) for i in fields)
    if dec:
        return dec(data)
    return data


def byte_decode(fields=None, count=4):
    """Data content decoder."""
    _LOGGER.debug('fields= %s', fields)
    if count == 2:
        data = (fields[0] << 8 | fields[1])
        return data

    data = (fields[0] << 24 |
            fields[1] << 16 |
            fields[2] << 8 |
            fields[3])

    return data


def test_valid_data(data):
    """Test the incoming data for validity."""
    # pylint: disable=too-many-return-statements
    if data is None:
        return False

    if len(data) > 302 or len(data) < 180:
        _LOGGER.debug('Invalid packet size %s', len(data))
        return False

    if not data[0] and data[-1] == FRAME_FLAG:
        _LOGGER.debug("%s Recieved %s bytes of %s data",
                        datetime.now().isoformat(),
                        len(data), False)
        return False

    header_checksum = CrcX25.calc(bytes(data[1:6]))
    read_header_checksum = (data[7] << 8 | data[6])

    if header_checksum != read_header_checksum:
        _LOGGER.debug('Invalid header CRC check')
        return False

    frame_checksum = CrcX25.calc(bytes(data[1:-3]))
    read_frame_checksum = (data[-2] << 8 | data[-3])

    if frame_checksum != read_frame_checksum:
        _LOGGER.debug('Invalid frame CRC check')
        return False

    if data[8:12] != DATA_FLAG:
        _LOGGER.debug('Data does not start with %s: %s',
                        DATA_FLAG, data[8:12])
        return False

    packet_size = len(data)
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2

    if packet_size != read_packet_size:
        _LOGGER.debug(
            'Packet size does not match read packet size: %s : %s',
            packet_size, read_packet_size)
        return False

    return True
