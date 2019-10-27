# DON'T USE THIS. THE HTTP CALLS ARE BROKEN AF

'''
This file contains everything that handles the
Nutritionix API calls
'''

import json
import urllib.parse
import urllib.request

APP_ID = ''
APP_KEY = ''

BASE_NUTRITIONIX_URL = 'https://api.nutritionix.com/v1_1'

def build_search_by_name_url(search_query: str, min_results: int, max_results: int) -> str:
    query_parameters = [
        ('results', str(min_results) + '%3A' + str(max_results)),
        ('fields', 'item_id,item_name'),
        ('appId', APP_ID),
        ('appKey', APP_KEY)
    ]
    return BASE_NUTRITIONIX_URL + '/search/'+ urllib.parse.quote_plus(search_query) \
    + '?' + urllib.parse.urlencode(query_parameters)

def build_search_by_item_id_url(search_query: str) -> str:
    query_parameters = [
        ('id', search_query), ('appId', APP_ID), ('appKey', APP_KEY)
    ]
    return BASE_NUTRITIONIX_URL + '/item?' + urllib.parse.urlencode(query_parameters)

def get_result(url: str) -> dict:
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()

def get_item_id(search_result: dict) -> str:
    index = 0 # need to change later
    return search_result['hits'][index]['fields']['item_id']

def get_calories(search_result: dict) -> int:
    return int(search_result['nf_calories'])
