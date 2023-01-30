#import Firebasedht_variosdatos
import pulsometro
from machine import Timer
from pulsometro import Pulso
from telegramM import Telebot
from machine import sleep, SoftI2C, Pin, I2C, ADC
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import utime
import time
from ssd1306 import SSD1306_I2C
import ssd1306
import framebuf
import network, time, urequests

ancho = 128  # Definimos el ancho de la OLED
alto = 64    # Definimos el alto de la OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Definimos los pines de la OLED SCL y SDA para ssd1306 y sh1106(otra)
oled = SSD1306_I2C(ancho, alto, i2c)
        #sensor = machine.ADC(19)

temporiza = Timer(0)
oledC = Pulso()

oledC.pantalla()
#Base = Firebasedht_variosdatos


def desborde(Timer):
    print("*\n" * 40)
    if oledC.datos <= 30 and oledC.datos2 >= 31 or oledC.datos3 >= 10:
        print("BPM={:02} p SpO2={:02}%  Temp={:02} °C ".format(oledC.datos, oledC.datos2, oledC.datos3))
        #guardar_datos(oledC.datos, oledC.datos2, oledC.datos3)
        

        print("*" * 5)
        
       
    
           
        oled.text("BPM",10,0)
        oled.text(str(oledC.datos),10,10)
        oled.text("Sp02",10,20)                
        oled.text(str(oledC.datos2),10,30)
        oled.text("Temp",10,40)                
        oled.text(str(oledC.datos3),10,50)
        
        oled.show()
        
temporiza.init(period=1000,mode=Timer.PERIODIC,callback=desborde)        
        

        
            

            
    
    
    
        




oledC.muestra()


tele_obj = Telebot()
tele_obj.conectar()
tele_obj.pantalla()
#Base.conectaWifi()
#oledC.muestra()




#oledC.pantalla()
