from time import sleep
import paho.mqtt.client as mqtt
import adafruit_dht
import board
import psutil

MY_ID = "25"

dht_device = adafruit_dht.DHT22(board.D4)

def get_data():
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            return temperature, humidity
        except RuntimeError as error:
            sleep(2.0)
            continue

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = f"mobile/{MY_ID}/sensing"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

try:
    while True:
        sleep(1)
        humidity, temperature = get_data()
        value = f'{{"temperature": {temperature:.1f}, "humidity": {humidity}}}'
        client.publish(MQTT_TOPIC, value)
        print(value)
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    client.loop_stop()
    client.disconnect()
