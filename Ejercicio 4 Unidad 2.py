from machine import Pin, time_pulse_us
import network
import urequests
import time
from hcsr04 import HCSR04

sensor_HCSR04 = HCSR04(trigger_pin = 12, echo_pin = 26, echo_timeout_us = 24000);
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1369521165382455349/hW1V7eGze1ZHC5_i6-BBLQvydges_Q7u29dIsOlwKLO0WOQaSfE0wGuex2bbFpIbgvDO"

# Conexión Wi-Fi
def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        time.sleep(1)
    print("Conectado:", wlan.ifconfig())

SSID = "Manuelifter.19"
PASSWORD = "deadlift"
conectar_wifi(SSID, PASSWORD)

def enviar_mensaje_discord(mensaje):
    try:
        response = urequests.post(DISCORD_WEBHOOK_URL, json={"content": mensaje})
        response.close()
    except Exception as e:
        print("Error al enviar mensaje:", e)

while True:
    distancia = sensor_HCSR04.distance_cm();
    print("Distancia:", distancia, "cm")
    if distancia < 20:
        enviar_mensaje_discord(f"Objeto cercano a {distancia:.2f} cm")
        time.sleep(5)
    time.sleep(1)