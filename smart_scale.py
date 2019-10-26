#Enoch Chau 2019
#SD HACKS
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

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

if __name__ == "__main__":
    # Initialize the LCD using the pins above.
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)

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
            if GPIO.input(button_pin) == GPIO.HIGH:
                print("tare button pushed")
                hx.tare()
                lcd.clear()
                lcd.message("0 g")
            if GPIO.input(button_pin2) == GPIO.HIGH:
                val = hx.get_weight(5)
                val = round(val)
                print(str(val) + " g")
                lcd.clear()
                lcd.message(str(val) + " g")

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()
