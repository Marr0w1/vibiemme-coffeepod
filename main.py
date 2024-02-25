#import packages
import utime, machine
from machine import Pin, SPI, I2C
from pico_i2c_lcd import I2cLcd
import onewire, ds18x20
from vl53l0x import VL53L0X

ds_pin = Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

#Assign GPIO pins. The first Potentiometer is the dial that sets 'brew time'. The second two ADC inputs aren't currently used.
potentiometer = machine.ADC(26) #Set the GP26 pin as analog input
#Conversion factor translates the bits from the resistance of the 'brew time' dial into a useful value (default 0-10 seconds) 
conversion_factor = 10 / (65535)
#led is currently a light that turns on and off to emulate when the pump should be run. This will be replaced by a solid state relay.
relay=Pin(15,Pin.OUT)
#led_external = machine.Pin(15, machine.Pin.OUT) #Set GP15 as output mode

#button is currently a N/C button, which is causing some issues. This needs to be changed when we replace the button.
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
i2c_2 = machine.I2C(id=1, scl=machine.Pin(3), sda=machine.Pin(2))
i2c = I2C(id=0,scl=Pin(9),sda=Pin(8),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)


#this is the 'default' function/state that should always be running, waiting for a button press.
def sleeping():
    while True:
        global volt
        global shot
        volt = (potentiometer.read_u16() * conversion_factor)#Convert the sampled data to voltage value
        shot=int(volt)
        msg=(str("Shot = ") + str(shot) + str(" sec"))
        lcd.move_to(0,1)
        lcd.putstr(msg)
        lcd.clear()
        utime.sleep(.2)
        lcd.backlight_off()
        if button.value() == 0:
            print("Going to ready")
            utime.sleep(.2)
            return()

#function called when we press the button once. Wakes the display from 'sleep mode', displays current set shot time, and if pressed again will pull a shot.
def ready():
    print("Waking up ")
    utime.sleep(.5)
    seconds = 30
    lcd.clear()
    lcd.backlight_on()
    while True:
        if button.value() == 0:
            utime.sleep(.5)
            print("second press, going to Brewing")
            state="brewing"
            brewing()
        if seconds > 0:
            lcd.move_to(0,0)
            lcd.putstr('Ready to Brew ')
            lcd.putchar(chr(0))
            lcd.putchar(chr(1))
            lcd.move_to(0,1)
            volt = (potentiometer.read_u16() * conversion_factor)#Convert the sampled data to voltage value
            shot=int(volt)
            temp = ds_sensor.read_temp(roms[0])
            print(str(tof.ping()))
            msg=(str("wtr:") + str(tof.ping()) + str(" tmp: ") + str(temp))
            lcd.putstr(msg)
            utime.sleep(1)
            seconds = seconds - 1
        else:
            print("going back to sleep")
            return()

#function called when we pull an espresso shot. Displays a countdown and activates the led/relay for the time set.
def brewing():
    print("Brewing for " + str(shot))
    seconds = shot
    lcd.clear()
    relay.value(0)
    utime.sleep(.5)
    while True:
        if button.value() == 0:
            print("third press, aborting Brewing")
            state="cleanup"
            cleanup()
        if seconds > 0:
            stringseconds=str(seconds)
            lcd.move_to(0,0)
            lcd.putstr("Brewing Now!")
            lcd.move_to(8,1)
            lcd.putstr(stringseconds)
            utime.sleep(1)
            seconds = seconds - 1
        else:
            relay.value(1)
            print("Brewing Done")
            return()

#the other functions resolve to this, in order to ensure the displays and relays are set to a clean/safe state, before returning to Ready state.         
def cleanup():
    print("cleaning up")
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr('Cleaning Up')
    relay.value(1)
    utime.sleep(2)
    lcd.clear()
    lcd.backlight_off()
    print("all done")
    return()
    

#Code starts here, initialises custom logo (only needs to be done once) then calls the Ready function.
lcd.custom_char(1, bytearray([0x08,0x10,0x08,0x00,0x1C,0x1A,0x1C,0x10]))
lcd.custom_char(0, bytearray([0x04,0x08,0x04,0x00,0x1F,0x0F,0x0F,0x07]))
tof = VL53L0X(i2c_2)
budget = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)

# Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the
# given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
# to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
# Valid values are (even numbers only):

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)

# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

state = "sleeping"
#Iterates though various states to make it easier to track what it is currently doing.
while True:
    if state == "sleeping":
        sleeping()
        state = "ready"
    elif state == "ready":
        ready()
        state = "cleanup"
    elif state == "brewing":
        brewing()
        state = "cleanup"
    elif state == "cleanup":
        cleanup()
        state = "sleeping"
