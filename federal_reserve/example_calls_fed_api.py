import requests
import pprint

KEY = 'd87219606729528c27784921b44c5630'
pp = pprint.PrettyPrinter()

# Some examples using the Federal Reserve API

payload = {
    'api_key': KEY,
    'file_type': 'json'
}

# Get all Economic SERIES data that matches the string of text
r = requests.get(url='https://api.stlouisfed.org/fred/series/search?search_text=SEARCH_TXT', params=payload)

r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=LNU00000000&', params=payload)

# This gives all the parent categories
r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=0', params=payload)

# This gives the child categories of the specified id
r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=10', params=payload)

r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=104&', params=payload)

r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=32992&', params=payload)

# Children of Flow of Funds
r = requests.get(
    url='https://api.stlouisfed.org/fred/category/children?category_id=32251', params=payload)

r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33205', params=payload)

# This gets the series contained in a given category id
bal_sheet_households = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32258',
                                    params=payload)

# Get the ids for all of the subcategories of the Flow of Funds...
r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33243', params=payload)

# Get metadata about the series
r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=FBAGSEA027N&', params=payload)

# Get the series observation data, either directly or from imported functions
r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=CNP16OV', params=payload)

# Get the sub categories of the given category id
r = requests.get(url='https://api.stlouisfed.org/fred/category?category_id=32992&', params=payload)

# Get the series of the given category
r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32992&', params=payload)