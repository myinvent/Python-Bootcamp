"""
Ambient Light Sensing (Lux Measurement)

"""

import time
import board
import analogio

# LDR sensor object
ldr = analogio.AnalogIn(board.GP26)           
resistance = 10000   # resistance value in ohm

# sensorTimer object
sensorTimer = time.monotonic()

# Function of conversion of voltage to lux
def resistance_to_lux (adc):
    ldr_voltage = (adc * 3.3) / 65536
    ldr_resistance = (ldr_voltage * resistance) / (3.3 - ldr_voltage)
    lux = 500 / (ldr_resistance / 1000) # Conversion of resistance to lumen
    
    return lux

while True:
    
    # Update Interval Every 2 seconds to read sensor's data
    if (sensorTimer + 2) < time.monotonic():
        
        sensorTimer = time.monotonic()
        
        ldr_adc = ldr.value
        light = resistance_to_lux(ldr_adc)
        
        print("Ambient Light: {:.2f} lux".format(light))
