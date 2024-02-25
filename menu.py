from rotary_irq_rp2 import RotaryIRQ
from machine import Pin
import time

rotary = RotaryIRQ(13, 14, pull_up=True, range_mode=RotaryIRQ.RANGE_WRAP, min_val=0)
btn = Pin(12, Pin.IN, Pin.PULL_UP)

current_val = 0  # Track the last known value of the encoder
brewtime = 30

def menusleeping():
    global current_val
    global new_val
    print("new val")
    print((rotary.value()))
    while True:
        new_val = rotary.value()  #encoder value right now
        if new_val != 0:  #if encoder value has changed
            current_val = new_val
            return()
            
def menuready():
    global current_val
    global new_val
    print("new val")
    print((rotary.value()))
    while True:
        new_val = rotary.value()  #encoder value right now
        if new_val != 1:  # The encoder value has changed!
            current_val = new_val
            return()

def menubrew():
    global current_val
    global new_val
    print("new val")
    print((rotary.value()))
    while True:
        new_val = rotary.value()  # What is the encoder value right now?
        if new_val != 2:  # The encoder value has changed!
            current_val = new_val
            return()
        
def menuset():
    global current_val
    global new_val
    global brewtime
    print("new val")
    print((rotary.value()))
    print(("brewtime ") + str(brewtime))
    print("press button to set time")
    while True:
        new_val = rotary.value()  # What is the encoder value right now?
        if btn.value() == 0:  # Has the button been pressed?
            time.sleep_ms(500) # A small delay to wait for the button to stop being pressed
            print("going to set time")
            rotary.reset()
            timeset() # Resets the rotary library's internal counter back to zero
        if new_val != 3:  # The encoder value has changed!
            current_val = new_val
            return()
        
def timeset():
    global current_val
    global new_val
    global brewtime
    while True:
        if btn.value() == 0:  # Has the button been pressed?
            time.sleep_ms(250) # A small delay to wait for the button to stop being pressed
            brewtime = current_val
            print("Setting brewtime to " + str(brewtime))
            return()
        new_val = rotary.value()  # What is the encoder value right now? 
        if current_val != new_val:  # The encoder value has changed!
            print('Encoder value:', new_val)
            current_val = new_val  # Track this change as the last know value

while True:
    current_val = rotary.value()
    if current_val == 0:
        print("sleeping")
        menusleeping()
    elif current_val == 1:
        print("ready")
        menuready()
    elif current_val == 2:
        print("brew")
        menubrew()
    elif current_val == 3:
        print("menuset")
        menuset()
    elif current_val >=4:
        rotary.reset()
