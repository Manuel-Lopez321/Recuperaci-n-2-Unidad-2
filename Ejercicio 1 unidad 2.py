import time
import dht
from machine import Pin

# Crear objeto del sensor DHT11
sensor = dht.DHT11(Pin(13))  # Usa el pin GPIO 4

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()

        print("Temperatura: {} °C, Humedad: {} %".format(temp, hum))
        
    except OSError as e:
        print("Error al leer del sensor:", e)
    
    time.sleep(2)  # Espera 2 segundos
