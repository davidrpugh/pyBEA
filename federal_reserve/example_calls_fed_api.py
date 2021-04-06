import json
import requests
import pprint
import pandas as pd
import time

import fed_data_api

KEY = 'd87219606729528c27784921b44c5630'
BASE_URL = 'https://api.stlouisfed.org/fred/'

pp = pprint.PrettyPrinter()

# Get all Economic SERIES data that matches the string of text
r = requests.get(url='https://api.stlouisfed.org/fred/series/search?search_text=federal reserve compensation employees&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())

r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=LNU00000000&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())

# This gives all the parent categories
r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=0&api_key={0}&file_type=json'.format(KEY))
pp.pprint(r.json())

r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=10&api_key={0}&file_type=json'.format(KEY))
pp.pprint(r.json())

r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=104&api_key={0}&file_type=json'.format(KEY))
pp.pprint(r.json())

r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=32992&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())

# Children of Flow of Funds
r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=32251&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())

r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33205&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())

# This gets the series contained in a given category id
# bal_sheet_households = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32258&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(bal_sheet_households.json())

# Get the ids for all of the subcategories of the Flow of Funds...
r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33243&api_key={0}&file_type=json'.format(KEY))

# Get metadata about the series
r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=FBAGSEA027N&api_key={0}&file_type=json'.format(KEY))

# Get the series observation data, either directly or from imported functions
r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=CNP16OV&api_key={0}&file_type=json&frequency=a'.format(KEY))
pp.pprint(r.json())

# mon_auth = fed_data_api.get_observation('BOGZ1FA716025005A')
# print(mon_auth)

# Get the sub categories of the given category id
r = requests.get(url='https://api.stlouisfed.org/fred/category?category_id=32992&api_key={0}&file_type=json'.format(KEY))

# Get the series of the given category
r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32992&api_key={0}&file_type=json'.format(KEY))
# print(r.json())

# FL153061705