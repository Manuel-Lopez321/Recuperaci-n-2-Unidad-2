from machine import Pin, time_pulse_us
import network
import urequests
import time
from hcsr04 import HCSR04

LED_PIN = 14
led = Pin(LED_PIN, Pin.OUT)

TOKEN = "7514449296:AAETyW6FLkHquRrIxtGVmQaxJ0vhxQvpIWs"
BOT_URL = f"https://api.telegram.org/bot{TOKEN}"
ULTIMA_ACTUALIZACION = 0


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

def obtener_mensajes():
    global ULTIMA_ACTUALIZACION
    try:
        url = f"{BOT_URL}/getUpdates?offset={ULTIMA_ACTUALIZACION + 1}"
        r = urequests.get(url)
        mensajes = r.json()
        r.close()
        if mensajes["ok"]:
            return mensajes["result"]
        return []
    except Exception as e:
        print("Error al obtener mensajes:", e)
        return []
    
def enviar_mensaje(chat_id, texto):
    try:
        url = f"{BOT_URL}/sendMessage"
        urequests.post(url, json={"chat_id": chat_id, "text": texto}).close()
    except Exception as e:
        print("Error al enviar mensaje:", e)
        
while True:
    mensajes = obtener_mensajes()
    for mensaje in mensajes:
        ULTIMA_ACTUALIZACION = mensaje["update_id"]
        if "message" in mensaje:
            texto = mensaje["message"]["text"]
            chat_id = mensaje["message"]["chat"]["id"]
            print("Comando recibido:", texto)
            if texto == "/on":
                led.on()
                enviar_mensaje(chat_id, "LED encendido correctamente")
            elif texto == "/off":
                led.off()
                enviar_mensaje(chat_id, "LED apagado correctamente")
            else:
                enviar_mensaje(chat_id, "Comando no reconocido. Usa /on o /off.")
    time.sleep(2)