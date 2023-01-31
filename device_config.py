from dependencies.PiicoDev_SSD1306 import *
from dependencies.PiicoDev_BME280 import *
from dependencies.PiicoDev_VEML6030 import *
from dependencies.PiicoDev_VEML6040 import *
from dependencies.PiicoDev_TMP117 import *

pest_id = 'jack_test'
lab_id = 'jack'

### SENSOR INITIALIZING ###
class pico_sensors:
    def __init__(self):
        self.atmos = PiicoDev_BME280()
        self.light = PiicoDev_VEML6030()
        self.color = PiicoDev_VEML6030()
        self.color = PiicoDev_VEML6040()
        self.display = create_PiicoDev_SSD1306()
        self.temp = PiicoDev_TMP117()
        
        self.zeroAlt = self.atmos.altitude()
        
    def test_sensors(self):
        if not self.atmos.values():
            print("Atmospheric sensor not working")
        if not self.light.read():
            print("Light sensor not working")
        if not self.color.readRGB():
            print("Color sensor not working")
        if not self.temp.readTempC():
            print("Temperature sensor not working")
        try:
            self.display.text("|Pico Sensor|", 0, 0, 1)
            self.display.show()
        except:            
            print("Display not working")


class wifiSetup:
    def __init__(self):
        ## rPi400 hotspot ##
        self.rPi_ssid = 'pestHub'
        self.rPi_password = 'Zaq1Mjkl'

        ## Android hotspot ##
        self.android_ssid = 'Android'
        self.android_password = '12345678'

