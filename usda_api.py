'''
This file contains everything that handles the
USDA API calls
'''

import json
from urllib import request, parse

API_KEY = 'pbGv6UeN2LMmlpJA3IjIa9VYIs8hO8TEyGkvXbTS'

BASE_USDA_URL = 'https://api.nal.usda.gov/fdc/v1'

CALORIES_ID = 1008

def build_search_by_item_id_url(item_id: str) -> str:
    return BASE_USDA_URL + '/{}?api_key={}'.format(item_id, API_KEY)

# Rebecca To do: Fix the 403 forbidden error -> API key?
# def get_search_by_name(search_query: str) -> dict:
#     query_parameters = {'generalSearchInput' : search_query, 'requireAllWords': 'true','api_key' : API_KEY}
#     query_parameters = parse.urlencode(query_parameters).encode()
#     response = None
#     try:
#         req = request.Request(BASE_USDA_URL + '/search?api_key=' + API_KEY, data=query_parameters)
#         response = request.urlopen(req)
#         json_text = response.read().decode(encoding = 'utf-8')
#         return json.loads(json_text)
#
# def get_item_id(search_query: str) -> str:
#     return

def get_result(url: str) -> dict:
    response = None
    try:
        response = request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

def get_calories(search_result: dict) -> int:
    all_nutrients = search_result['foodNutrients']
    for x in all_nutrients:
        if x['nutrient']['id'] == CALORIES_ID and x['nutrient']['name'].lower() == 'energy':
            return int(x['amount'])

def get_grams(search_result: dict) -> float:
    total_grams = 0.0
    try:
        all_foods = search_result['inputFoods']
        for food in all_foods:
            total_grams += food['gramWeight']
        return total_grams
    except:
        return 0

def get_calories_per_gram(search_result: dict) -> float:
    total_calories = get_calories(search_result)
    total_grams = get_grams(search_result)
    if total_grams <= 0:
        total_grams = 100
    return float(total_calories) / total_grams
