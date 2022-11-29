# Passive Environmental Sleep Tracker (PEST)

This is a repo for a Raspberry Pi & Pi Pico based sensor station.
This is very much a prototype device, but intends to allow for network-attached bedroom environmental sensors. It also intends to fill a similar role to the [Withings Data Hub](https://support.withings.com/hc/en-us/categories/360001272798-Data-Hub).

Features / integrations:

* Sensors
  * Microphone
  * Temperature
  * Humidity
  * Air Pressure
  * Altitude
  * Light (Lux & Hue/Sat/Kelvin)
* Processing
  * Integration with [SNAPI](http://www.snapi.space/) website & database
  * On-board processing of SPL and other audio data
* Future
  * Android emulation to handle device connections
  * Additional IO to handle unconnected devices (e.g., WatchPAT, Actiwatch, etc...)
  * 4G/Mobile Data to allow for independent connectivity
