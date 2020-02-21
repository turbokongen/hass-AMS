"""
Decode for han_kaifa.

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
    "MA105H2E": 'Domestic 1 Phase 230V/400V meter',
    "MA304H3E": 'Domestic/Industrial 3 Phase 230V 3-Wire meter',
    "MA304H4": 'Domestic/Industrial 3 Phase 400V 4-Wire meter',
    "MA304T4": 'Industrial 3 Phase 230V 3-Wire meter',
    "MA304T3": 'Industrial 3 Phase 400V 4-Wire meter'
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
    date_time_year = byte_decode(fields=pkt[19:21], count=2)
    date_time_month = pkt[21]
    date_time_date = pkt[22]
    han_data["day_of_week"] = WEEKDAY_MAPPING.get(pkt[23])
    date_time_hour = str(pkt[24]).zfill(2)
    date_time_minute = str(pkt[25]).zfill(2)
    date_time_seconds = str(pkt[26]).zfill(2)
    date_time_str = (str(date_time_year) +
                     '-' + str(date_time_month) +
                     '-' + str(date_time_date) +
                     ' ' + date_time_hour +
                     ':' + date_time_minute +
                     ':' + date_time_seconds)
    han_data["date_time"] = date_time_str
    list_type = pkt[32]
    han_data["list_type"] = list_type
    if list_type is LIST_TYPE_MINI:
        han_data["active_power_p"] = byte_decode(fields=pkt[34:38])
        sensor_data["ams_active_power_import"] = {
            'state': han_data["active_power_p"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'unit_of_measurement': 'W',
                'icon': 'mdi:gauge'
            }
        }
        return sensor_data

    han_data["obis_list_version"] = field_type(fields=pkt[35:42], enc=chr)
    han_data["meter_serial"] = field_type(fields=pkt[44:60], enc=chr)
    han_data["meter_type"] = field_type(fields=pkt[62:70], enc=chr)
    han_data["meter_type_str"] = METER_TYPE.get(
        field_type(fields=pkt[62:70], enc=chr))
    han_data["active_power_n"] = byte_decode(fields=pkt[76:80]) / 100
    sensor_data["ams_active_power_export"] = {
        'state': han_data["active_power_n"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'unit_of_measurement': 'W',
            'icon': 'mdi:gauge'
            }
        }
    han_data["reactive_power_p"] = byte_decode(fields=pkt[81:85])
    sensor_data["ams_reactive_power_import"] = {
        'state': han_data["reactive_power_p"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'unit_of_measurement': 'VAr',
            'icon': 'mdi:gauge'
            }
        }
    han_data["reactive_power_n"] = byte_decode(fields=pkt[86:90])
    sensor_data["ams_reactive_power_export"] = {
        'state': han_data["reactive_power_n"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'unit_of_measurement': 'VAr',
            'icon': 'mdi:gauge'
            }
        }
    han_data["current_l1"] = byte_decode(fields=pkt[91:95]) / 1000
    sensor_data["ams_current_l1"] = {
        'state': han_data["current_l1"],
        'attributes': {
            'timestamp': han_data["date_time"],
            'meter_manufacturer': han_data["obis_list_version"].title(),
            'meter_type': han_data["meter_type_str"],
            'meter_serial': han_data["meter_serial"],
            'unit_of_measurement': 'A',
            'icon': 'mdi:current-ac'
            }
        }

    if (list_type is LIST_TYPE_SHORT_3PH or
            list_type is LIST_TYPE_LONG_3PH):
        han_data["current_l2"] = byte_decode(fields=pkt[96:100]) / 1000
        sensor_data["ams_current_l2"] = {
            'state': han_data["current_l2"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'A',
                'icon': 'mdi:current-ac'
                }
            }
        han_data["current_l3"] = byte_decode(fields=pkt[101:105]) / 1000
        sensor_data["ams_current_l3"] = {
            'state': han_data["current_l3"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'A',
                'icon': 'mdi:current-ac'
                }
            }
        han_data["voltage_l1"] = byte_decode(fields=pkt[106:110]) / 10
        sensor_data["ams_voltage_l1"] = {
            'state': han_data["voltage_l1"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }
        han_data["voltage_l2"] = byte_decode(fields=pkt[111:115]) / 10
        sensor_data["ams_voltage_l2"] = {
            'state': han_data["voltage_l2"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }
        han_data["voltage_l3"] = byte_decode(fields=pkt[116:120]) / 10
        sensor_data["ams_voltage_l3"] = {
            'state': han_data["voltage_l3"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
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
            han_data["active_energy_p"] = byte_decode(fields=pkt[135:139]) / 1000
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
            han_data["active_energy_n"] = byte_decode(fields=pkt[140:144]) / 1000
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
            han_data["reactive_energy_p"] = byte_decode(fields=pkt[145:149]) / 1000
            sensor_data["ams_reactive_energy_import"] = {
                'state': han_data["reactive_energy_p"],
                'attributes': {
                    'timestamp': han_data["date_time"],
                    'meter_timestamp': han_data["meter_date_time"],
                    'meter_manufacturer': han_data["obis_list_version"].title(),
                    'meter_type': han_data["meter_type_str"],
                    'meter_serial': han_data["meter_serial"],
                    'unit_of_measurement': 'kVArh',
                    'icon': 'mdi:gauge'
                }
            }
            han_data["reactive_energy_n"] = byte_decode(fields=pkt[150:154]) / 1000
            sensor_data["ams_reactive_energy_export"] = {
                'state': han_data["reactive_energy_n"],
                'attributes': {
                    'timestamp': han_data["date_time"],
                    'meter_timestamp': han_data["meter_date_time"],
                    'meter_manufacturer': han_data["obis_list_version"].title(),
                    'meter_type': han_data["meter_type_str"],
                    'meter_serial': han_data["meter_serial"],
                    'unit_of_measurement': 'kVArh',
                    'icon': 'mdi:gauge'
                }
            }

    if (list_type is LIST_TYPE_SHORT_1PH or
            list_type is LIST_TYPE_LONG_1PH):

        han_data["voltage_l1"] = byte_decode(fields=pkt[96:100]) / 10
        sensor_data["ams_voltage_l1"] = {
            'state': han_data["voltage_l1"],
            'attributes': {
                'timestamp': han_data["date_time"],
                'meter_manufacturer': han_data["obis_list_version"].title(),
                'meter_type': han_data["meter_type_str"],
                'meter_serial': han_data["meter_serial"],
                'unit_of_measurement': 'V',
                'icon': 'mdi:flash'
                }
            }

        if list_type == LIST_TYPE_LONG_1PH:
            meter_date_time_year = byte_decode(fields=pkt[102:104], count=2)
            meter_date_time_month = pkt[104]
            meter_date_time_date = pkt[105]
            han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(pkt[106])
            meter_date_time_hour = str(pkt[107]).zfill(2)
            meter_date_time_minute = str(pkt[108]).zfill(2)
            meter_date_time_seconds = str(pkt[109]).zfill(2)
            han_data["meter_date_time"] = (str(meter_date_time_year) +
                                           '-' + str(meter_date_time_month) +
                                           '-' + str(meter_date_time_date) +
                                           ' ' + meter_date_time_hour +
                                           ':' + meter_date_time_minute +
                                           ':' + meter_date_time_seconds)
            han_data["active_energy_p"] = byte_decode(fields=pkt[115:120]) / 1000
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
            han_data["active_energy_n"] = byte_decode(fields=pkt[121:125]) / 1000
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
            han_data["reactive_energy_p"] = byte_decode(fields=pkt[126:130]) / 1000
            sensor_data["ams_reactive_energy_import"] = {
                'state': han_data["reactive_energy_p"],
                'attributes': {
                    'timestamp': han_data["date_time"],
                    'meter_timestamp': han_data["meter_date_time"],
                    'meter_manufacturer': han_data["obis_list_version"].title(),
                    'meter_type': han_data["meter_type_str"],
                    'meter_serial': han_data["meter_serial"],
                    'unit_of_measurement': 'kVArh',
                    'icon': 'mdi:gauge'
                    }
                }
            han_data["reactive_energy_n"] = byte_decode(fields=pkt[131:135]) / 1000
            sensor_data["ams_reactive_energy_export"] = {
                'state': han_data["reactive_energy_n"],
                'attributes': {
                    'timestamp': han_data["date_time"],
                    'meter_timestamp': han_data["meter_date_time"],
                    'meter_manufacturer': han_data["obis_list_version"].title(),
                    'meter_type': han_data["meter_type_str"],
                    'meter_serial': han_data["meter_serial"],
                    'unit_of_measurement': 'kVArh',
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

    if len(data) > 157 or len(data) < 41:
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

    if data[9:13] != DATA_FLAG:
        _LOGGER.debug('Data does not start with %s: %s',
                      DATA_FLAG, data[9:13])
        return False

    packet_size = len(data)
    read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2

    if packet_size != read_packet_size:
        _LOGGER.debug(
            'Packet size does not match read packet size: %s : %s',
            packet_size, read_packet_size)
        return False

    return True
