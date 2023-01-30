from machine import sleep, SoftI2C, Pin, I2C, ADC 
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import utime
import time 
from ssd1306 import SSD1306_I2C  
import framebuf
import machine

class Pulso():
    def __init__ (self):
        self.datos=0
        self.datos2=0
        self.datos3=0
        
         
        
        
        
        
    def pantalla(self):
        ancho = 128  # Definimos el ancho de la OLED
        alto = 64    # Definimos el alto de la OLED

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Definimos los pines de la OLED SCL y SDA para ssd1306 y sh1106(otra)
        oled = SSD1306_I2C(ancho, alto, i2c)
        #sensor = machine.ADC(19)
        #adc = machine.ADC(machine.Pin(26))
        #sensor = adc.read_u16()


        print(i2c.scan())

        def buscar_icono(ruta):
            dibujo = open(ruta, "rb")  # Abrir en modo lectura de bits https://python-intermedio.readthedocs.io/es/latest/open_function.html
            dibujo.readline() # metodo para ubicarse en la primera linea de los bist
            xy = dibujo.readline() # ubicarnos en la segunda linea
            x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
            y = int(xy.split()[1])
            icono = bytearray(dibujo.read())  # guardar en matriz de bites
            dibujo.close()
            return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)  # Utilizamos el metodo MONO_HLSB

        oled.blit(buscar_icono("areandina/babysensor.pbm"), 0, 0)  # ruta y sitio de ubicación del directorio
        oled.show()  # mostrar en la oled
        time.sleep(3)  # Espera de 3 segundos
        oled.fill(0)
        oled.show()

        oled.text('Welcome to the', 0, 10)
        oled.text('Baby sensor', 0, 30)
        oled.text('Juan y Camilo', 0, 50)
        oled.show()
        time.sleep(4)

        oled.fill(1)
        oled.show()
        time.sleep(2)
        oled.fill(0)
        oled.show()

        """while True:
            oled.fill(0)
            conversion_factor = 3.3 / (65535)
            val= (sensor)
            voltaje = (sensor*conversion_factor)
            oled.text("************",0,0)    
            oled.text("Lectura",10,10)
            oled.text(str(val),10,20)
            oled.text("Voltaje",10,30)                
            oled.text(str(voltaje),0,40)
            oled.text("************",0,50)
            oled.show()
                
            print("Voltaje =", voltaje)
            time.sleep(0.25)"""
            
    def muestra (self):
        i2c = SoftI2C(sda=Pin(19), scl=Pin(23), freq=400000)  
        sensor = MAX30102(i2c=i2c)

        if sensor.i2c_address not in i2c.scan():
            print("Sensor no encontrado.")
            return

        elif not (sensor.check_part_id()):
            print("ID de dispositivo I2C no correspondiente a MAX30102 o MAX30105.")
            return

        else:
            print("Sensor conectado y reconocido.")

        sensor.setup_sensor()
        sensor.set_sample_rate(400)
        sensor.set_fifo_average(2)
        sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        sleep(1)
        self.datos3 = sensor.read_temperature()
        

        compute_frequency = True
        t_start = ticks_us()
        samples_n = 0

        while True:
            sensor.check()
            if sensor.available():
                red_reading = sensor.pop_red_from_storage()
                ir_reading = sensor.pop_ir_from_storage() 
                f_conversion=60/17500
                self.datos=red_reading*f_conversion
                
                utime.sleep(2)    

                self.datos2=ir_reading*f_conversion
                
                utime.sleep(2)                

                if compute_frequency:
                    if ticks_diff(ticks_us(), t_start) >= 999999:
                        f_HZ = samples_n
                        samples_n = 0 
                        t_start = ticks_us()
                    else:
                        samples_n = samples_n + 1
                    

    
        

			