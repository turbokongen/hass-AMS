# hass-AMS
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
Custom component reading AMS through MBus adapter into HomeAssistant


## *Installation*
Stop Home-Assistant, 
Find your MBus adapter port, 
copy *ams* folder into your *custom_components* folder, 
Start Home-Assistant, 
Set up the integration in the *Integrations* config, 

For parity options see https://github.com/pyserial/pyserial/blob/master/serial/serialutil.py#L79

This will create sensors for each of the available usage data in the meter.
The accumulative sensors will only be available after first read, and is transmitted from the meter 5 seconds past the hour.

## *Known working modules*
https://www.aliexpress.com/item/32719562958.html?spm=a2g0s.9042311.0.0.c8314c4dpbv1pv
https://www.aliexpress.com/item/32751482255.html?spm=2114.10010108.1000014.1.2a3189f8fCOsSM

## * Known NOT working modules*
https://www.aliexpress.com/item/32814808312.html?shortkey=iM7rQb67&addresstype=600

I do not have decoders for Kaifa and Aidon meters. Feel free to open PR og supply data so it can be added.
Imporvements and suggestions are also welcome.
Keep in mind, I am not a experienced programmer :)
Enjoy
