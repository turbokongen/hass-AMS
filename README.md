# hass-AMS
Custom component reading AMS through MBus adapter into HomeAssistant sensors.


## *Installation*
copy *ams* folder into your *custom_components* folder
add the following to your configuration.yaml:
```yaml
ams:
  serial_port: [SERIAL_PORT TO YOUR MBus ADAPTER] *required*
  parity: [PARITY FOR SERIAL READING, defaults to N.] *optional*
```
For parity options see https://github.com/pyserial/pyserial/blob/master/serial/serialutil.py#L79

This will create sensors for each of the available usage data in the meter.
The accumulative sensors will only be available after first read, and is transmitted from the meter 5 seconds past the hour.

This is only tested on Kamstrup 3phase meter.

Kamstrup 1phase meters are untested, but available in code. In theory it should work.
I do not have decoders for Kaifa and Aidon meters. Feel free to open PR og supply data so it can be added.
Imporvements and suggestions are also welcome.
Keep in mind, I am not a experienced programmer :)
Enjoy
