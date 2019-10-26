Initial Calibration
https://tutorials-raspberrypi.com/digital-raspberry-pi-scale-weight-sensor-hx711/
1. Using out of box scale, record the weight on an object.
2. disassemble scale and connect load cell to hx711 and hx711 to Raspberry pi.
3. run sample code for hx711 and calibrate load scale using weight of object previously found.

Google Vision
https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Fruit Calorie Dictionary
Fruits: apple, banana, orange to start

Food Nutrition API (Nutritionix)
1. API GET request: search by object name
    > https://api.nutritionix.com/v1_1/search/{name_of_object}?results={min_results}%3A{max_results}&fields=item_id%2Citem_name&appId={id}}&appKey={key}
2. Get item_id
3. API GET request: get nutrition information by item_id
    > https://api.nutritionix.com/v1_1/item?id={item_id}&appId&appId={id}}&appKey={key}

Food Nutrition API (USDA)
1. API POST request: search by object name
    > https://api.nal.usda.gov/fdc/v1/search?api_key={key}
2. Get fdcId
3. API GET request: get nutrition information by fdcId
    > https://api.nal.usda.gov/fdc/v1/{id}?api_key={key}
4. Get calories value by getting foodNutrients id 1008

Food scale hardware
1. be able to tare scale using button
2. set up LED to blink when scale is done processing calories
3. LCD to display weight (grams), fruit type, calories

Algorithm
1. Weight is recorded from load cell.
2. Fruit type is recorded from google vision/pi camera.
3. Grams per calorie is calculated using dictionary.
4. LED blinks, LCD is updated.
5. Calories are recorded somewhere (google sheet with iftt?)

Reach Goals
1. Implement a database to collect caloric data.
2. implement user facing android app or website that can record calories.
