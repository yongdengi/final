import time
import board
import adafruit_dht
import neopixel
from gpiozero import PWMOutputDevice

dht_device = adafruit_dht.DHT22(board.D4)

pixel_pin = board.D10
num_pixels = 4

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

pwm_device = PWMOutputDevice(pin=12, frequency=100, initial_value=0.5)

tones = [100,100,100,0,100,100,100,0]
music = [0,1,2,3,4,5,6,7]
term = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]

def get_humidity():
    try:
        humidity = dht_device.humidity
        return humidity
    except RuntimeError:
        return None

def set_led_color(humidity):
    if humidity < 65:
        pixels.fill((0, 0, 255))
        pixels.show()
        play_tone()
    elif 65 <= humidity <= 80:
        pixels.fill((0, 255, 0))
        pixels.show()
    else:
        pixels.fill((255, 0, 0))
        pixels.show()
        play_tone()

def play_tone():
    try:
        for i in range(len(music)):
            pwm_device.frequency = tones[music[i]]
            pwm_device.value = 0.5 
            time.sleep(term[i])
            pwm_device.value = 0
    except KeyboardInterrupt:
        pass

try:
    while True:
        humidity = get_humidity()
        set_led_color(humidity)
        print(f"Humidity: {humidity}%")
        time.sleep(2.0)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    dht_device.exit()
    pwm_device.close()
