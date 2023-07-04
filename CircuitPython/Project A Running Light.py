"""
Running Light by 4 LEDs

"""

import time
import board
import digitalio

# LED1 object and mode
led1 = digitalio.DigitalInOut(board.GP12)
led1.direction = digitalio.Direction.OUTPUT

# LED2 object and mode
led2 = digitalio.DigitalInOut(board.GP13)
led2.direction = digitalio.Direction.OUTPUT

# LED3 object and mode
led3 = digitalio.DigitalInOut(board.GP14)
led3.direction = digitalio.Direction.OUTPUT

# LED4 object and mode
led4 = digitalio.DigitalInOut(board.GP15)
led4.direction = digitalio.Direction.OUTPUT

while True:
    # Control the LED 1
    led1.value = True
    time.sleep(0.1)
    
    led1.value = False
    time.sleep(0.1)
    
    # Control the LED 2
    led2.value = True
    time.sleep(0.1)
    
    led2.value = False
    time.sleep(0.1)
    
    # Control the LED 3
    led3.value = True
    time.sleep(0.1)
    
    led3.value = False
    time.sleep(0.1)
    
    # Control the LED 4
    led4.value = True
    time.sleep(0.1)
    
    led4.value = False
    time.sleep(0.1)