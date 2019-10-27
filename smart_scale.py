#Enoch Chau 2019
#SD HACKS
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from RPLCD.gpio import CharLCD

import google_vision
#for IFTT
import requests

#threading
import threading

#API calling
import usda_api

# Hardcoded food id's with their names for demo purposes only
COMMON_FRUITS = {
    ('apple', 'gala apple', 'fuji apple', 'apples', 'gala apples', 'fuji apples') : '341508',
    ('orange', 'oranges') : '169919',
    ('tangerine', 'clementine', 'mandarin orange', 'tangerines', 'clementines', 'mandarin oranges') : '169105',
    ('banana', 'bananas') : '173944',
    ('lemon', 'lemons') : '167746',
    ('pear', 'pears') : '169118',
    ('blueberry', 'blueberries') : '171711',
    ('strawberry', 'strawberries'): '341668',
    ('apricot', 'apricots') : '171697',
    ('grapefruit', 'grapefruits') : '341423'
}

#hx711 reference value
referenceUnit = -278

#button setup
button_pin = 8 #GPIO8
button_pin2 = 7 #GPIO7

val = 0

def tare_task(hx, lock, run_event):
    #init tare button
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while run_event.is_set():
        if GPIO.input(button_pin) == GPIO.HIGH:
            lock.acquire()
            print("tare button pushed")
            hx.tare()
            hx.power_down()
            hx.power_up()
            lock.release()

def weigh_task(hx, lock, lcd, run_event):
    global val
    while run_event.is_set():
        lock.acquire()
        # print('pre-val')
        # print(val)
        val = hx.get_weight(5)
        val = round(val,2)
        # print('real-val')
        print(str(val) + " g")
        lcd.clear()
        lcd.write_string(str(val) + " g")
        hx.power_down()
        hx.power_up()
        lock.release()
        time.sleep(0.1)

def get_cal(hx, lock, lcd, run_event):
    #init capture buttons
    GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    global val
    global COMMON_FRUITS
    while run_event.is_set():
        if GPIO.input(button_pin2) == GPIO.HIGH:
            lock.acquire()
            #get labels from google vision
            print("taking photo")
            labels = google_vision.main()
            print("photo done")

            #IFTT call to post to google sheet and ios health app
            food = _get_food_name(labels)
            weight = val
            calories = _get_total_calories(food, weight)
            print("food: ")
            print(labels)
            print("weight (g): {}".format(weight))
            print("calores (kcal): {}".format(calories))
            sheet_r = requests.post('https://maker.ifttt.com/trigger/calorie_get/with/key/ceLI0vmThKLzD52zpCCPjw', params={"value1":food ,"value2":weight,"value3":calories})
            health_app_r = requests.post('https://maker.ifttt.com/trigger/ios_health_cal/with/key/ceLI0vmThKLzD52zpCCPjw', params={"value1":str(calories) ,"value2":food})
            lock.release()

# HELPER FUNCTIONS
def _get_food_name(labels: list) -> str:
    fruits = tuple(COMMON_FRUITS.keys())
    fruits = sum(fruits, ())
    for label in labels:
        fruit_name = labels.description
        fruit_name = fruit_name.lower()
        if fruit_name in fruits:
            return fruit_name

def _get_total_calories(food:str, weight:float) -> float:
    global COMMON_FRUITS
    food_id = _get_food_id(food)
    search_url = usda_api.build_search_by_item_id_url(food_id)
    result = usda_api.get_result(search_url)
    calories = usda_api.get_calories_per_gram(result) * weight
    return calories

def _get_food_id(food:str) -> str:
    for k, v in COMMON_FRUITS.items():
        if food in k:
            return v

if __name__ == "__main__":
    # Initialize the LCD using the pins above.
    lcd = CharLCD(pin_rs = 25, pin_rw = None, pin_e = 24, pins_data = [23,17,18,22], numbering_mode = GPIO.BCM, cols=16, rows=2, dotsize=8)

    #init hx711
    hx = HX711(5, 6)#DT to 5, SCK to 6
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()

    print("Tare done! Add weight now...")

    lock = threading.Lock()

    run_event = threading.Event()
    run_event.set()
    # creating threads
    t1 = threading.Thread(target=tare_task, args=(hx,lock,run_event))
    t2 = threading.Thread(target=weigh_task, args=(hx,lock,lcd,run_event))
    t3 = threading.Thread(target=get_cal, args=(hx,lock,lcd,run_event))
    t1.start()
    t2.start()
    t3.start()
    try:
        while True:
            time.sleep(.1)
    except (KeyboardInterrupt, SystemExit):
        run_event.clear()
        t1.join()
        t2.join()
        t3.join()
        print("threads joined")
        lcd.clear()
        print("lcd cleared")
        GPIO.cleanup()
        print("pins cleaned")

        print("Bye!")
        sys.exit()
