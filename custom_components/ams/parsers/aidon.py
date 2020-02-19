"""
Decode for han aidon.

This module will decode the incoming message from Mbus serial.
"""

import logging
from datetime import datetime
from crccheck.crc import CrcX25

DATA_FLAG = [230, 231, 0, 15]
FRAME_FLAG = b'\x7e'
LIST_TYPE_MINI = 1
LIST_TYPE_SHORT_1PH = 9
LIST_TYPE_LONG_1PH = 14
LIST_TYPE_SHORT_3PH = 13
LIST_TYPE_LONG_3PH = 18

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
    6515: '6515 1-phase Meter with CB on both lines and Earth Fault Current Measuremen',
    6525: '6525 3-phase Meter with CB and Earth Fault Measurement',
    6534: '6534 3-phase Meter with CB and Neutral Current Measurement',
    6540: '6540 3-phase CT Meter',
    6550: '6550 3-phase CT Meter'
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
    list_type = pkt[19]
    han_data["list_type"] = list_type
    if list_type == LIST_TYPE_MINI:
        han_data["obis_a_p_p"] = field_type(".", fields=pkt[24:30])
        han_data["active_power_p"] = byte_decode(fields=pkt[31:35])
        sensor_data["ams_active_power_import"] = {
            'state': han_data["active_power_p"],
            'attributes': {
                'obis_code': han_data["obis_a_p_p"],
                'unit_of_measurement': 'W',
                'icon': 'mdi:gauge'
            }
        }
        return sensor_data
    han_data["obis_list_version"] = field_type(fields=pkt[31:42], enc=chr)
    han_data["meter_serial"] = field_type(fields=pkt[55:71], enc=chr)
    han_data["meter_type"] = field_type(fields=pkt[83:87], enc=chr)
    han_data["meter_type_str"] = METER_TYPE.get(
        field_type(fields=pkt[83:87], enc=chr, dec=int))
    han_data["obis_a_p_p"] = field_type(".", fields=pkt[91:97])
    han_data["active_power_p"] = byte_decode(fields=pkt[98:102])
    sensor_data["ams_active_power_import"] = {
        'state': han_data["active_power_p"],
        'attributes': {
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'obis_code': han_data["obis_a_p_p"],
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'obis_code': han_data["obis_a_p_p"],
            'unit_of_measurement': 'W',
            'icon': 'mdi:gauge'
            }
        }
    han_data["obis_a_p_n"] = field_type(".", fields=pkt[112:118])
    han_data["active_power_n"] = byte_decode(fields=pkt[119:123])
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
    han_data["obis_r_p_n"] = field_type(".", fields=pkt[133:139])
    han_data["reactive_power_p"] = byte_decode(fields=pkt[140:144])
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
    han_data["obis_r_p_n"] = field_type(".", fields=pkt[154:160])
    han_data["reactive_power_n"] = byte_decode(fields=pkt[161:165])
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
    han_data["obis_c_l1"] = field_type(".", fields=pkt[175:181])
    han_data["current_l1"] = byte_decode(fields=pkt[182:184]) / 100
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
        han_data["obis_c_l2"] = field_type(".", fields=pkt[195:201])
        han_data["current_l2"] = byte_decode(fields=pkt[202:204]) / 100
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
        han_data["obis_c_l3"] = field_type(".", fields=pkt[215:221])
        han_data["current_l3"] = byte_decode(fields=pkt[222:224]) / 100
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
        han_data["obis_v_l1"] = field_type(".", fields=pkt[225:231])
        han_data["voltage_l1"] = byte_decode(fields=pkt[232:234]) / 10
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
        han_data["obis_v_l2"] = field_type(".", fields=pkt[245:251])
        han_data["voltage_l2"] = byte_decode(fields=pkt[252:254]) / 10
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
        han_data["obis_v_l3"] = field_type(".", fields=pkt[265:271])
        han_data["voltage_l3"] = byte_decode(fields=pkt[272:274]) / 10
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
        han_data["obis_v_l1"] = field_type(".", fields=pkt[195:201])
        han_data["voltage_l1"] = byte_decode(fields=pkt[202:204]) / 10
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
        meter_date_time_year = byte_decode(fields=pkt[222:224], count=2)
        meter_date_time_month = pkt[224]
        meter_date_time_date = pkt[225]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[226])
        meter_date_time_hour = str(pkt[227]).zfill(2)
        meter_date_time_minute = str(pkt[228]).zfill(2)
        meter_date_time_seconds = str(pkt[229]).zfill(2)
        han_data["meter_date_time"] = (str(meter_date_time_year) +
                                       '-' + str(meter_date_time_month) +
                                       '-' + str(meter_date_time_date) +
                                       ' ' + meter_date_time_hour +
                                       ':' + meter_date_time_minute +
                                       ':' + meter_date_time_seconds)
        han_data["obis_a_e_p"] = field_type(".", fields=pkt[238:244])
        han_data["active_energy_p"] = byte_decode(fields=pkt[245:249]) / 100
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
        han_data["obis_a_e_n"] = field_type(".", fields=pkt[259:265])
        han_data["active_energy_n"] = byte_decode(fields=pkt[266:270]) / 100
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
        han_data["obis_r_e_p"] = field_type(".", fields=pkt[281:287])
        han_data["reactive_energy_p"] = byte_decode(fields=pkt[288:292]) / 100
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
        han_data["obis_r_e_n"] = field_type(".", fields=pkt[303:309])
        han_data["reactive_energy_n"] = byte_decode(fields=pkt[310:314]) / 100
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
        meter_date_time_year = byte_decode(fields=pkt[122:124], count=2)
        meter_date_time_month = pkt[124]
        meter_date_time_date = pkt[125]
        han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[126])
        meter_date_time_hour = str(pkt[127]).zfill(2)
        meter_date_time_minute = str(pkt[128]).zfill(2)
        meter_date_time_seconds = str(pkt[129]).zfill(2)
        han_data["meter_date_time"] = (str(meter_date_time_year) +
                                       '-' + str(meter_date_time_month) +
                                       '-' + str(meter_date_time_date) +
                                       ' ' + meter_date_time_hour +
                                       ':' + meter_date_time_minute +
                                       ':' + meter_date_time_seconds)
        han_data["active_energy_p"] = byte_decode(fields=pkt[134:139]) / 100
        sensor_data["ams_active_energy_import"] = {
            'state': han_data["active_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["active_energy_n"] = byte_decode(fields=pkt[140:144]) / 100
        sensor_data["ams_active_energy_export"] = {
            'state': han_data["active_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'kWh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["reactive_energy_p"] = byte_decode(fields=pkt[145:149]) / 100
        sensor_data["ams_reactive_energy_import"] = {
            'state': han_data["reactive_energy_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'kVAh',
                'icon': 'mdi:gauge'
                }
            }
        han_data["reactive_energy_n"] = byte_decode(fields=pkt[150:154]) / 100
        sensor_data["ams_reactive_energy_export"] = {
            'state': han_data["reactive_energy_n"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_timestamp': han_data["meter_date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
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

    if len(data) > 377 or len(data) < 44:
        _LOGGER.debug('Invalid packet size %s', len(data))
        return False

    if not data[0] and data[-1] == FRAME_FLAG:
        _LOGGER.debug("%s Recieved %s bytes of %s data",
                      datetime.now().isoformat(),
                      len(data), False)
        return False

    header_checksum = CrcX25.calc(bytes(data[1:7]))
    read_header_checksum = (data[8] << 8 | data[7])

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
