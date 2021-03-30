import requests
import json
import pprint
KEY = 'd87219606729528c27784921b44c5630'

pp = pprint.PrettyPrinter()

# r = requests.get(url='https://api.stlouisfed.org/fred/series&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=GNPCA&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category&api_key={0}&file_type=json'.format(KEY))

# Get all Economic SERIES data that matches the string of text
# r = requests.get(url='https://api.stlouisfed.org/fred/series/search?search_text=flow&api_key={0}&file_type=json'.format(KEY))


# Find flow of funds category and series id, get observation/data
# r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=0&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32992&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32251&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33243&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=FBAGSEA027N&api_key={0}&file_type=json'.format(KEY))
r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=FBAGSEA027N&api_key={0}&file_type=json'.format(KEY))

# r = requests.get(url='https://api.stlouisfed.org/fred/category?category_id=32992&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32992&api_key={0}&file_type=json'.format(KEY))

print(pp.pprint(r.json()))

# print(r.json())