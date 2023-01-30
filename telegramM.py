import network, time, urequests   # Cómo se trabaja con APIs hay que manejar esta libreria que ya la tiene machine para peticiones de recursos en APIs
from machine import Pin, ADC, I2C
from utelegram import Bot  # Utilizamos el módulo utelegram para que funcione
from ssd1306 import SSD1306_I2C
import framebuf
from time import sleep
import framebuf # Módulo para visualizar imagenes en pbm



#Modulo para conectar a Telegram
class Telebot():
    def __init__ (self):
        pass
    
    def pantalla (self):
        
        sensor = ADC(Pin(36)) # conectamos el ADC en el ADC 1 señal analoga para guardarlo en el objeto
        ancho = 128  # Definimos el ancho de la OLED
        alto = 64    # Definimos el alto de la OLED

        i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #Definimos los pines de la OLED SCL y SDA para ssd1306 y sh1106(otra)
        oled = SSD1306_I2C(ancho, alto, i2c)

        def buscar_icono(ruta):
            dibujo = open(ruta, "rb")  # Abrir en modo lectura de bits https://python-intermedio.readthedocs.io/es/latest/open_function.html
            dibujo.readline() # metodo para ubicarse en la primera linea de los bist
            xy = dibujo.readline() # ubicarnos en la segunda linea
            x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
            y = int(xy.split()[1])
            icono = bytearray(dibujo.read())  # guardar en matriz de bites
            dibujo.close()
            return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)  #Utilizamos el metodo MONO_HLSB
        print(i2c.scan())

        oled.blit(buscar_icono("areandina/cisco.pbm"), 0, 0) # ruta y sitio de ubicación del directorio
        oled.show()  #mostrar en la oled
        time.sleep(3) # Espera de 3 segundos
        oled.fill(0)
        oled.show()
         
        oled.text('Bienvenidos a', 10, 20)
        oled.text('Areandina', 20, 40)
        oled.text('Oxitegram', 20, 40)
        oled.show()
        time.sleep(4)
         
        oled.fill(1)
        oled.show()
        time.sleep(2)
        oled.fill(0)
        oled.show()
        
        
                  
    print("Soy el método oled")   
    
    
    def conectar (self):
        print("Conectando...")
        print("Soy el método Telegram")
        
        TOKEN = '5360526708:AAFRu0RX1JMLvrHoxMaoz3gmb-O_nRZPfPA'

        bot = Bot(TOKEN)
        led = Pin(2, Pin.OUT)

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

        if conectaWifi ("Fernanda 2.4", "1023167 "):

            print ("Conexión exitosa!")
            print('Datos de la red (IP/netmask/gw/Dns):', miRed.ifconfig())    
            
            @bot.add_message_handler('Hola')
            def help(update):
                update.reply('Escriba on para encender y off para apagar el led, Value para estado y Sensor para temperatura')

            @bot.add_message_handler('Value')
            def value(update):
                if led.value():
                    update.reply('LED is on')
                else:
                    update.reply('LED is off')
                    
            @bot.add_message_handler('On')
            def on(update):
                led.on()
                print("El led está encendido")
                update.reply('LED is on')
                

            @bot.add_message_handler('Off')
            def off(update):
                led.off()
                print("El led está apagado")
                update.reply('LED is off')
               
            bot.start_loop()
                
        else:
               print ("Imposible conectar")
               miRed.active (False)
               
    print("soy el método conectar")
    
   
      