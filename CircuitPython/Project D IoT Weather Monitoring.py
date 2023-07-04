"""
Weather Monitoring System with DHT11, LDR and Thingspeak

Additional libraries, saved into the lib folder.
    https://circuitpython.org/libraries
    - adafruit_dht.mpy
    - adafruit_requests.mpy

"""

import os
import time
import board
import analogio
import adafruit_dht
import microcontroller
import wifi
import socketpool
import adafruit_requests
import ssl

# DHT11 sensor object
dht11 = adafruit_dht.DHT11(board.GP16)

# LDR sensor object
ldr = analogio.AnalogIn(board.GP26)           
resistance = 10000   # resistance value in ohm

# now timer object
now = time.monotonic()

# Get Wi-Fi and Thingspeak Write API details from the settings.toml file
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")
thingSpeakWriteAPIKey = os.getenv("THINGSPEAK_WRITE_API_KEY")

# ThingSpeak HTTP API URL.
thingSpeakAPI = os.getenv("THINGSPEAK_HTTP_API")

print("""
 ________   _           ____              __  
/_  __/ /  (_)__  ___ _/ __/__  ___ ___ _/ /__
 / / / _ \/ / _ \/ _ `/\ \/ _ \/ -_) _ `/  '_/
/_/ /_//_/_/_//_/\_, /___/ .__/\__/\_,_/_/\_\ 
                /___/   /_/                  """ + "(Microcontroller: " + os.uname()[0] + ")\n")

# Connect to Wi-Fi AP
print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
wifi.radio.connect(ssid, password)
print("connected!")
pool = socketpool.SocketPool(wifi.radio)
print("R.Pi Pico W IP Address: {}\n".format(wifi.radio.ipv4_address))
requests = adafruit_requests.Session(pool, ssl.create_default_context())

def resistance_to_lux (adc):
    ldr_voltage = (adc * 3.3) / 65536
    ldr_resistance = (ldr_voltage * resistance) / (3.3 - ldr_voltage)
    lux = 500 / (ldr_resistance / 1000) # Conversion of resistance to lumen
    
    return lux

# Start a loop that reads data from the sensor and sends it to ThingSpeak
while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
            wifi.radio.connect(ssid, password)
            print("connected!")
        
        temperature = dht11.temperature
        humidity = dht11.humidity
        
        ldr_adc = ldr.value
        light = resistance_to_lux(ldr_adc)
        
        print("Temperature: {:.2f} °C, Humidity: {:.2f} %RH, Light:  {:.2f} lux".format(temperature, humidity, light))
    
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
        
    time.sleep(2)
    
    # Update Interval Every 16 seconds to ThingSpeak
    if (now + 16) < time.monotonic():
        
        now = time.monotonic()
        
        # Updating Data ThingSpeak
        print("Updating data to ThingSpeak ... ", end="")
        
        # Generate ThingSpeak HTTP API URL request
        thingSpeakRequestURL = thingSpeakAPI + "api_key=" + thingSpeakWriteAPIKey + "&field1=" + str(temperature) + "&field2=" + str(humidity) + "&field3=" + str(light)
        
        # Make HTTP request to ThingSpeak to update data in the channel
        response = requests.get(thingSpeakRequestURL)
        
        # Receive HTTP response from ThingSpeak
        print("done! Data Count: ", response.text, "\n")