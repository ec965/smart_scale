#Enoch Chau 2019
#SD HACKS
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from RPLCD.gpio import CharLCD

import multitasking
import signal
# kill all tasks on ctrl-c
signal.signal(signal.SIGINT, multitasking.killall)

#hx711 reference value
referenceUnit = -278

#button setup
button_pin = 8 #GPIO8
button_pin2 = 7 #GPIO7

def cleanAndExit():
    lcd.clear()
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

@multitasking.task
def tare_button(hx, lcd):
    if GPIO.input(button_pin) == GPIO.HIGH:
        print("tare button pushed")
        hx.tare()
        lcd.clear()
        lcd.write_string("0 g")
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

if __name__ == "__main__":
    # Initialize the LCD using the pins above.
    lcd = CharLCD(pin_rs = 25, pin_rw = None, pin_e = 24, pins_data = [23,17,18,22], numbering_mode = GPIO.BCM, cols=16, rows=2, dotsize=8)

    #init hx711
    hx = HX711(5, 6)#DT to 5, SCK to 6
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    #init tare button
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #init weigh button
    GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    print("Tare done! Add weight now...")

    while True:
        try:
            tare_button(hx, lcd)
            # if GPIO.input(button_pin2) == GPIO.HIGH:
            val = hx.get_weight(5)
            val = round(val,2)
            print(str(val) + " g")
            lcd.clear()
            lcd.write_string(str(val) + " g")
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)



        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
