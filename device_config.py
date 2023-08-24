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
        try:
            self.atmos = PiicoDev_BME280()
            self.zeroAlt = self.atmos.altitude()
        except: self.atmos = None
        try: self.light = PiicoDev_VEML6030()
        except: self.light = None
        try: self.color = PiicoDev_VEML6040()
        except: self.color = None
        try: self.temp = PiicoDev_TMP117()
        except: self.temp = None
        
        try: self.display = create_PiicoDev_SSD1306()
        except: self.display = None
        
        
    def test_sensors(self):
        if not self.atmos:
            print("Atmospheric sensor not working")
        if not self.light:
            print("Light sensor not working")
        if not self.color:
            print("Color sensor not working")
        if not self.temp:
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
        self.android_ssid = 'JMobi'
        self.android_password = 'Zaq1Mjkl'

