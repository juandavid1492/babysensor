#------------------------------ [IMPORT]------------------------------------
from machine import sleep, SoftI2C, Pin, I2C, ADC
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import network, time, urequests
from machine import Pin, ADC, PWM
import dht
import utime
import ujson
import ufirebase as firebase
from pulsometro import Pulso
#--------------------------- [OBJETOS]---------------------------------------

i2c = SoftI2C(sda=Pin(19), scl=Pin(23), freq=400000)
oledC = Pulso()



#----------------------[ CONECTAR WIFI ]---------------------------------------------------------#

def conectaWifi (red, password):
            global miRed
            miRed = network.WLAN(network.STA_IF)     
            if not miRed.isconnected():              #Si no está conectado…
                miRed.active(True)                   #activa la interface
                miRed.connect(red, password)         #Intenta conectar con la red
                print('Conectando a la red', red +"…")
                timeout = time.time ()
            while not miRed.isconnected():           #Mientras no se conecte..
                if (time.ticks_diff (time.time (), timeout) > 10):
                    return False
            return True

            

        #------------------------------------[BOT]---------------------------------------------------------------------#

if conectaWifi ("Camilo", "salvador123"):
    
            print ("Conexión exitosa!")
            print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())         


            #sensor.Pulso(BPM, Sp02, temp)
            BPM = Pulso().datos
            Sp02= Pulso().datos2
            temp = Pulso().datos3
                              
            message = ujson.dumps({
            "BPM": BPM,
            "Sp02": Sp02,
            "temp": temp},)
                            
            firebase.setURL("https://babysecurity-e1c85-default-rtdb.firebaseio.com/")

                                      
            firebase.put("Estacion/{}".format(message, bg=0))
            print("Enviado...", message, " ",)

                                    
            firebase.get("Estacion/{}".format( "dato_recuperado", bg=0))
            print("Recuperado.... "+str(firebase.dato_recuperado))
            



            