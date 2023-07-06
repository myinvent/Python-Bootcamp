"""
Indoor Air Sensing (Temperature & Humidity)

"""

import time
import board
import adafruit_dht

# DHT11 sensor object
dht11 = adafruit_dht.DHT11(board.GP16)

# sensorTimer object
sensorTimer = time.monotonic()

while True:
    # Update Interval Every 2 seconds to read sensor's data
    if (sensorTimer + 2) < time.monotonic():
        
        sensorTimer = time.monotonic()
        
        temperature = dht11.temperature
        humidity = dht11.humidity
        
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH".format(temperature, humidity))
