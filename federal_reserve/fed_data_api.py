import json
import requests
import pprint
KEY = 'd87219606729528c27784921b44c5630'

pp = pprint.PrettyPrinter()

# r = requests.get(url='https://api.stlouisfed.org/fred/series&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=GNPCA&api_key={0}&file_type=json'.format(KEY))
# r = requests.get(url='https://api.stlouisfed.org/fred/category&api_key={0}&file_type=json'.format(KEY))

# Get all Economic SERIES data that matches the string of text
# r = requests.get(url='https://api.stlouisfed.org/fred/series/search?search_text=flow&api_key={0}&file_type=json'.format(KEY))

# Find flow of funds category and series id, get observation/data

# This gives the parent categories
r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=0&api_key={0}&file_type=json'.format(KEY))
# pp.pprint(r.json())
a = r.json()

# Create a list of all the parent categories, append their ids to a list called parent_list
dict = a['categories']
parent_list = []
for a in dict:
    parent_list.append(a['id'])

# This gives the children of one of the parent categories, in this case, National Accounts
# r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32992&api_key={0}&file_type=json'.format(KEY))
# for i in parent_list:
#     r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id={0}&api_key={1}&file_type=json'.format(i, KEY))
#     pp.pprint(r.json())

# Need Flow of Funds observation/series data:

# This gets the children categories for the National Accounts category; which contains the Flow of Funds category
# r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32992&api_key={0}&file_type=json'.format(KEY))

# This will return children categories for the Flow of Funds category...
r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32251&api_key={0}&file_type=json'.format(KEY))
flow_of_funds_cat = r.json()
flow_of_funds_cat = flow_of_funds_cat['categories']
flow_sub_cat = []
for a in flow_of_funds_cat:
    flow_sub_cat.append(a['id'])

print('This is flow_sub_cat: ', flow_sub_cat)
bal_sheet_households = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32259&api_key={0}&file_type=json'.format(KEY))

pp.pprint(bal_sheet_households.json())

# print('This is the balance sheet of households and nonprofits: ', bal_sheet_households.json())

# Get the ids for all of the subcategories of the Flow of Funds...
# r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=33243&api_key={0}&file_type=json'.format(KEY))
# print(r.json())

# r = requests.get(url='https://api.stlouisfed.org/fred/series?series_id=FBAGSEA027N&api_key={0}&file_type=json'.format(KEY))

# r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=FBAGSEA027N&api_key={0}&file_type=json'.format(KEY))

# r = requests.get(url='https://api.stlouisfed.org/fred/category?category_id=32992&api_key={0}&file_type=json'.format(KEY))

# r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id=32992&api_key={0}&file_type=json'.format(KEY))


def get_sub_cat(id):
    r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id={0}&api_key={1}&file_type=json'.format(id, KEY))
    r = r.json()
    return r

def get_series(id):
    r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id={0}&api_key={1}&file_type=json'.format(id, KEY))


def main():
    sub_cat = get_sub_cat('32251')
    # sub_series = get_series()
    # print(sub_cat)


if __name__ == '__main__':
    main()