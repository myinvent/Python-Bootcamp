"""
IoT Home Security Alert

Additional libraries, saved into the lib folder.
  https://circuitpython.org/libraries
  - adafruit_requests.mpy
  
"""

import os
import time
import board
import digitalio
import microcontroller
import json
import wifi
import ipaddress
import socketpool
import adafruit_requests
import ssl

# Microwave Radar sensor object
buzzer = digitalio.DigitalInOut(board.GP16)
buzzer.direction = digitalio.Direction.OUTPUT

# Microwave Radar sensor object
radar = digitalio.DigitalInOut(board.GP15)
radar.direction = digitalio.Direction.INPUT

# Favoriot Update Interval
favoriotUpdateInterval = 30  # in seconds
lastUpdateTime = 0

# Get Wi-Fi and Thingspeak Write API details from the settings.toml file
ssid = os.getenv('WIFI_SSID')
password = os.getenv('WIFI_PASSWORD')

print("""
    ______                       _       __ 
   / ____/___ __   ______  _____(_)___  / /_
  / /_  / __ `/ | / / __ \/ ___/ / __ \/ __/
 / __/ / /_/ /| |/ / /_/ / /  / / /_/ / /_  
/_/    \__,_/ |___/\____/_/  /_/\____/\__/ API v3.2.0""" + " (Microcontroller: " + os.uname()[0] + ")\n")

# Connect to Wi-Fi AP
print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
wifi.radio.connect(ssid, password)
print("connected!")
pool = socketpool.SocketPool(wifi.radio)
print("R.Pi Pico W IP Address: {}\n".format(wifi.radio.ipv4_address))
http = adafruit_requests.Session(pool, ssl.create_default_context())

# Function to update status to Favoriot
def update_to_favoriot (data):
    
    httpHeader = {
        "content-type": "application/json",
        "apikey": os.getenv('FAVORIOT_DEVICE_ACCESS_TOKEN')
    }
    
    httpBody = {
        "device_developer_id": os.getenv('FAVORIOT_DEVICE_DEVELOPER_ID'),
        "data": {
            "motion": data
        }
    }

    request = http.post(
        os.getenv("FAVORIOT_HTTP_API"),
        headers = httpHeader,
        json = httpBody
    )
    
    print("Favoriot HTTP Request: ", end="")
    
    response = json.loads(request.text)

    if response["statusCode"] == 201:
        print("Success: " + response["message"])
    else:
        print("Error: " + response["message"])
            
    request.close()

# Function to activate the buzzer
def activate_buzzer():
    for _ in range(3):
        buzzer.value = True
        time.sleep(0.1)  # Buzzer on for 0.1 seconds
        buzzer.value = False
        time.sleep(0.1)  # Buzzer off for 0.1 seconds
    time.sleep(1.0)  # Pause for 1 second between heartbeats
    
while True:
    
    if radar.value == True:
        # Update to Favoriot if the interval has passed since the last update
        if time.monotonic() - lastUpdateTime >= favoriotUpdateInterval:
            update_to_favoriot(radar.value)
            lastUpdateTime = time.monotonic()
            # Activate the buzzer when motion is detected
            activate_buzzer()
    
    print("Motion: {} ".format(radar.value))
    
    time.sleep(2)