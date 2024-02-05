#import packages
import utime, machine
from machine import Pin, SPI, I2C
from pico_i2c_lcd import I2cLcd

#Assign GPIO pins. The first Potentiometer is the dial that sets 'brew time'. The second two ADC inputs aren't currently used.
#thermo = machine.ADC(28)
#potentiometer2 = machine.ADC(27)
potentiometer = machine.ADC(26) #Set the GP26 pin as analog input
#Conversion factor translates the bits from the resistance of the 'brew time' dial into a useful value (default 0-10 seconds) 
conversion_factor = 10 / (65535)
#led is currently a light that turns on and off to emulate when the pump should be run. This will be replaced by a solid state relay.
led_external = machine.Pin(15, machine.Pin.OUT) #Set GP15 as output mode
#button is currently a N/C button, which is causing some issues. This needs to be changed when we replace the button.
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
i2c = I2C(id=0,scl=Pin(9),sda=Pin(8),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

#function called when we pull an espresso shot. Displays a countdown and activates the led/relay for the time set.
def pull():
    print("Lighting for " + str(shot))
    seconds = shot
    lcd.clear()
    led_external.on()
    while True:
        if seconds > 0:
            stringseconds=str(seconds)
            lcd.move_to(0,0)
            lcd.putstr("Brewing Now!")
            lcd.move_to(8,1)
            lcd.putstr(stringseconds)
            utime.sleep(1)
            seconds = seconds - 1
        else:
            print("pullcleanup")
            cleanup()

#function called when we press the button once. Wakes the display from 'sleep mode', displays current set shot time, and if pressed again will pull a shot.
def wakeup():
    print("Waking up ")
    utime.sleep(.2)
    seconds = 10
    lcd.clear()
    lcd.backlight_on()
    while True:
        if button.value() == 0:
            print("second press")
            pull()
        if seconds > 0:
            lcd.move_to(0,0)
            lcd.putstr('Ready to Brew ')
            lcd.putchar(chr(0))
            lcd.putchar(chr(1))
            lcd.move_to(0,1)
            volt = (potentiometer.read_u16() * conversion_factor)#Convert the sampled data to voltage value
            shot=int(volt)
            msg=(str("Shot = ") + str(shot) + str(" sec"))
            lcd.putstr(msg)
            utime.sleep(1)
            seconds = seconds - 1
        else:
            print("wakeupcleanup")
            cleanup()
          
#the other functions resolve to this, in order to ensure the displays and relays are set to a clean/safe state, before returning to Ready state.
def cleanup():
    print("cleaning up")
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Cleaning Up')
    led_external.off()
    utime.sleep(2)
    lcd.clear()
    lcd.backlight_off()
    print("all done")
    ready()

#this is the 'default' function/state that should always be running, waiting for a button press.
def ready():
    while True:
        global volt
        global shot
        volt = (potentiometer.read_u16() * conversion_factor)#Convert the sampled data to voltage value
        shot=int(volt)
        msg=(str("Shot = ") + str(shot) + str(" sec"))
        lcd.clear()
        lcd.backlight_off()
        if button.value() == 0:
            print("First press")
            utime.sleep(.2)
            wakeup()

#Code starts here, initialises custom logo (only needs to be done once) then calls the Ready function.
lcd.custom_char(1, bytearray([0x08,
  0x10,
  0x08,
  0x00,
  0x1C,
  0x1A,
  0x1C,
  0x10]))
lcd.custom_char(0, bytearray([0x04,
  0x08,
  0x04,
  0x00,
  0x1F,
  0x0F,
  0x0F,
  0x07]))        
ready()
