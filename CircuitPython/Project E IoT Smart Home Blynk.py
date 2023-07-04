"""
Smart Home with DHT11, LDR, LEDs and Blynk

Additional libraries, saved into the lib folder.
  https://circuitpython.org/libraries
  - adafruit_dht.mpy
  - adafruit_requests.mpy
  
"""

import os
import time
import board
import analogio
import digitalio
import adafruit_dht
import microcontroller
import wifi
import ipaddress
import socketpool
import adafruit_requests
import ssl

# DHT11 sensor object
dht11 = adafruit_dht.DHT11(board.GP16)

# LDR sensor object
ldr = analogio.AnalogIn(board.GP26)           
resistance = 10000   # resistance value in ohm

# LED1 object and mode
led1 = digitalio.DigitalInOut(board.GP13)
led1.direction = digitalio.Direction.OUTPUT

# LED3 object and mode
led2 = digitalio.DigitalInOut(board.GP14)
led2.direction = digitalio.Direction.OUTPUT

# LED3 object and mode
led3 = digitalio.DigitalInOut(board.GP15)
led3.direction = digitalio.Direction.OUTPUT

# blynkTimer object
blynkTimer = time.monotonic()

# sensorTimer object
sensorTimer = time.monotonic()

# Get Wi-Fi and Thingspeak Write API details from the settings.toml file
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
blynkAuthToken = os.getenv("BLYNK_AUTH_TOKEN")

# ThingSpeak HTTP API URL.
thingSpeakAPI = os.getenv("THINGSPEAK_HTTP_API")

print("""
   ___  __          __  
  / _ )/ /_ _____  / /__
 / _  / / // / _ \/  '_/
/____/_/\_, /_//_/_/\_\ 
       /___/            """ + "(Microcontroller: " + os.uname()[0] + ")\n")

# Connect to Wi-Fi AP
print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
wifi.radio.connect(ssid, password)
print("connected!")
pool = socketpool.SocketPool(wifi.radio)
print("R.Pi Pico W IP Address: {}\n".format(wifi.radio.ipv4_address))
requests = adafruit_requests.Session(pool, ssl.create_default_context())

# Function of conversion of voltage to lux
def resistance_to_lux (adc):
    ldr_voltage = (adc * 3.3) / 65536
    ldr_resistance = (ldr_voltage * resistance) / (3.3 - ldr_voltage)
    lux = 500 / (ldr_resistance / 1000) # Conversion of resistance to lumen
    
    return lux

# Write API
def blynk_write(token, pin, value):
    api_url = "https://blynk.cloud/external/api/update?token=" + token + "&" + pin + "="+ str(value)
    response = requests.get(api_url)
    
    if "200" in str(response):
        print(f"Value {pin} successfully updated to Blynk")
    else:
        print("Could not find the device token or wrong pin format!")

# Read API
def blynk_read(token, pin):
    api_url = "https://blynk.cloud/external/api/get?token=" + token + "&" + pin
    response = requests.get(api_url)
    return response.content.decode()

# Start a loop that reads data from the sensor and sends it to ThingSpeak
while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
            wifi.radio.connect(ssid, password)
            print("connected!")
        
        # Update Interval Every 2 seconds to read sensor's data
        if (sensorTimer + 2) < time.monotonic():
            
            sensorTimer = time.monotonic()
            
            temperature = dht11.temperature
            humidity = dht11.humidity
            
            ldr_adc = ldr.value
            light = resistance_to_lux(ldr_adc)
            
            print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH, Light:  {:.2f} lux".format(temperature, humidity, light))
        
        # Read Blynk Virtual Pin V0 for LED1
        led1Status = blynk_read(blynkAuthToken, "V0")
        # Read Blynk Virtual Pin V1 for LED2
        led2Status = blynk_read(blynkAuthToken, "V1")
        # Read Blynk Virtual Pin V2 for LED3
        led3Status = blynk_read(blynkAuthToken, "V2")
        
        # Control the LED1 based on status
        if (led1Status == "1"):
            led1.value = True
        else:
            led1.value = False
        
        # Control the LED2 based on status
        if (led2Status == "1"):
            led2.value = True
        else:
            led2.value = False
        
        # Control the LED3 based on status
        if (led3Status == "1"):
            led3.value = True
        else:
            led3.value = False
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    
    except Exception as error:
        dht11.exit()
        raise error
    
    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()
    
    # Update Interval Every 5 seconds to Blynk
    if (blynkTimer + 5) < time.monotonic():
        
        blynkTimer = time.monotonic()
        
        # Updating Data to Blynk
        print("Updating data to Blynk")
        
        # Write Blynk Virtual Pin V3
        blynk_write(blynkAuthToken, "V3", temperature)
        
        # Write Blynk Virtual Pin V4
        blynk_write(blynkAuthToken, "V4", humidity)
        
        # Write Blynk Virtual Pin V5
        blynk_write(blynkAuthToken, "V5", light)