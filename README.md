# hass-AMS
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
Custom component reading AMS through MBus adapter into HomeAssistant
Works with the following meters:
Kamstrup:
  - 6861111
  - 6841121
  - 6841131
  - 6851121
  - 6851131
 
 Kaifa:
  - MA304H3E Thanks to @thomasja27 for testing :+1:
 
 Not tested with, but should work:
  - MA105H2E
  - MA304H4
  - MA304T4
  - MA304T3

Aidon:
Aidon meters are not tested yet. (Please report errors or if it's working)
 - 6515
 - 6525
 - 6534
 - 6540
 - 6550
 
## *Installation*
Stop Home-Assistant, 
Find your MBus adapter port, 
copy *ams* folder into your *custom_components* folder, 
Start Home-Assistant, 
Set up the integration in the *Integrations* config, 

For parity options see https://github.com/pyserial/pyserial/blob/master/serial/serialutil.py#L79

Meter manufacturer field options are:

*aidon*
*kamstrup*
*kaifa*

This will create sensors for each of the available usage data in the meter.
The accumulative sensors will only be available after first read, and is transmitted from the meter 5 seconds past the hour.

## *Known working modules*
https://www.aliexpress.com/item/32719562958.html?spm=a2g0s.9042311.0.0.c8314c4dpbv1pv
https://www.aliexpress.com/item/32751482255.html?spm=2114.10010108.1000014.1.2a3189f8fCOsSM

## * Known NOT working modules*
https://www.aliexpress.com/item/32814808312.html?shortkey=iM7rQb67&addresstype=600

Imporvements and suggestions are also welcome.
Keep in mind, I am not a experienced programmer :)
Enjoy
