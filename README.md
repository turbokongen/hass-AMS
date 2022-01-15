# hass-AMS - AMS Reader for Norwegian and swedish AMS meters
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=AS5PQHAERQ85J&currency_code=NOK&source=url)
<a href="https://www.buymeacoffee.com/turbokongen" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Custom component reading AMS through MBus adapter into HomeAssistant
Supports the new energy dashboard in Home-Assistant.

If it does not decode your data, please submit a ticket, and I will try to 
make a parser for your meter.
If your meter type shown "unknown", please submit a ticket, and I will add 
your meter to the module.

Works with the following swedish and norwegian meters:

Kamstrup:
  - 6861111 tested by janna at homeassistant community forum
  - 6841121 tested by me
  - 6841131
  - 6841138A tested by NilsFA at homeassistant community forum
  - 6851121
  - 6851131
 
Kaifa:
Norway: 
  - MA304H3E Thanks to @thomasja27 for testing :+1:

Sweden:
  - MA304H4 Thanks to @runlar for testing (swedish version) :+1:

Not tested with, but should work:
  - MA105H2E
  - MA304T4
  - MA304T3

Aidon:
Norway:
 - 6525 Thanks to @razzymoose for testing and providing patch :+1:
 - 6515 Thanks to @maxgyver87 for fault finding and testing :+1:
 - 6534 Thanks to @mariwing for testing and debugging :+1:
 - 6483 Thanks @PerBob81 for confirming :+1:

Sweden:
 - 6484 Thanks to @bo1jo for testing and debugging :+1:


Not tested with, but should work:
 
 Norway:
 - 6540
 - 6550
 
 Sweden:
 - 6479
 
## *Installation
Easiest method is to install via HACS. Then setup via *Integrations* config.
*Or*
1. Copy *ams* folder into your *custom_components* folder.
2. Config by YAML setup or config by integrations in Home-assistant

*YAML options*
```yaml
ams:
  serial_port: '/dev/ttyUSB0' # Required. The serial port used to communicate through
  baudrate: 2400 # Optional, defaults to '2400'
  parity: 'N'  # Optional, defaults to 'N'
  meter_manufacturer: 'auto' # Optional, defaults to 'auto'
```

  
Start Home-Assistant, 
Set up the integration in the *Integrations* config if you haven't set up by YAML config.

For parity options see https://github.com/pyserial/pyserial/blob/master/serial/serialutil.py#L79

Meter manufacturer field options are:
```
'auto'
'aidon'
'aidon_se' # Swedish aidon meter RF2 modules
'kamstrup'
'kaifa'
'kaifa_se' # Swedish kaifa meters
```
This will create sensors for each of the available usage data in the meter.
The accumulative sensors will only be fully available after first read, and is transmitted from the meter 5 seconds past the hour.
There seems to be a bug in the current Kamstrup firmware that the hour package is transmitted at xx:xx:55.

## *Known working modules*
https://www.aliexpress.com/item/32719562958.html?spm=a2g0s.9042311.0.0.c8314c4dpbv1pv
https://www.aliexpress.com/item/32751482255.html?spm=2114.10010108.1000014.1.2a3189f8fCOsSM
https://www.aliexpress.com/item/32834331647.html?spm=a2g0o.detail.1000060.1.74cfdcd4qts4jp

## *Known NOT working modules*
https://www.aliexpress.com/item/32814808312.html?shortkey=iM7rQb67&addresstype=600

Improvements and suggestions are also welcome.
Keep in mind, I am not a experienced programmer :)
Enjoy

Latest information about OBIS for all the norwegian meters: https://www.nek.no/info-ams-han-utviklere/

Latest information about swedish standard for AMS: https://www.energiforetagen.se/globalassets/energiforetagen/det-erbjuder-vi/kurser-och-konferenser/elnat/branschrekommendation-lokalt-granssnitt-v2_0-201912.pdf
