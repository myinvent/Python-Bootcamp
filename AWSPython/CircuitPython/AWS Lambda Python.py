import os
import time
import board
import analogio
import ssl
import wifi
import socketpool
import adafruit_requests
import adafruit_dht

# DHT11 sensor object
dht11 = adafruit_dht.DHT11(board.GP16)

# LDR sensor object
ldr = analogio.AnalogIn(board.GP26)           
resistance = 10000   # resistance value in ohm

# updateInterval timer object
updateInterval = time.monotonic()

# Get Wi-Fi and Thingspeak Write API details from the settings.toml file
ssid = os.getenv("WIFI_SSID")
password = os.getenv("WIFI_PASSWORD")

print("""
   ___ _      ______  ___       __  __            
  / _ | | /| / / __/ / _ \__ __/ /_/ /  ___  ___  
 / __ | |/ |/ /\ \  / ___/ // / __/ _ \/ _ \/ _ \ 
/_/ |_|__/|__/___/ /_/   \_, /\__/_//_/\___/_//_/ 
                        /___/""" + "(Microcontroller: " + os.uname()[0] + ")\n")

# Connect to Wi-Fi AP
print(f"Connecting to Wi-Fi AP: {ssid} ... ", end="")
wifi.radio.connect(ssid, password)
print("connected!")
print("R.Pi Pico W IP Address: {}\n".format(wifi.radio.ipv4_address))

# Create a socket pool using the wifi radio module
pool = socketpool.SocketPool(wifi.radio)

# Create a default SSL context
context = ssl.create_default_context()

# Create an HTTPS session using the socket pool and SSL context
https = adafruit_requests.Session(pool, context)

# Function conversion for light sensor from voltage to lux
def resistance_to_lux (adc):
    ldr_voltage = (adc * 3.3) / 65536
    ldr_resistance = (ldr_voltage * resistance) / (3.3 - ldr_voltage)
    lux = 500 / (ldr_resistance / 1000) # Conversion of resistance to lumen
    
    return lux

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
    
    # Update Interval Every 10 seconds to AWS API Endpoint
    if (updateInterval + 10) < time.monotonic():
        
        updateInterval = time.monotonic()
        
        httpBody = {
            "temperature": str(temperature),
            "humidity": str(humidity),
            "light": str(light)
        }

        response = https.request(
            os.getenv("AWS_HTTPS_METHOD"),
            os.getenv("AWS_HTTPS_API"),
            json = httpBody
        )
        
        print("AWS HTTPS Request: ", end="")
        
        if response.status_code == 200:
            print("Successful > ", end="")
            print(response.text)
        else:
            print("Failed!")
                
        response.close()
        
        print()