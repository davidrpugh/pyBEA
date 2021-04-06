import json
import requests
import pprint
import pandas as pd
import time

KEY = 'd87219606729528c27784921b44c5630'
BASE_URL = 'https://api.stlouisfed.org/fred/'

pp = pprint.PrettyPrinter()


payload = {
    'api_key': KEY,
    'file_type': 'json'
}


def get_sub_cat(id):
    r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id={0}'.format(id), params=payload)
    r = r.json()
    return r


def get_series(id):
    # Given an category id, returns all associated series
    r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id={0}'.format(id), params=payload)
    list_of_series = []
    temp_dict = r.json()
    # pp.pprint(temp_dict)
    temp_dict = temp_dict['seriess']
    for a in temp_dict:
        list_of_series.append(a['id'])

    return list_of_series


def get_observation(id):
    r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id={0}'.format(id, KEY),
                     params=payload)
    r = r.json()
    return r


def get_all_flow_funds_ids():
    # This will return children series_ids for everything in the Flow of Funds category...
    r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32251'.format(KEY),
                     params=payload)
    flow_of_funds_cat = r.json()
    flow_of_funds_cat = flow_of_funds_cat['categories']

    flow_sub_cat = []
    for a in flow_of_funds_cat:
        flow_sub_cat.append(a['id'])

    flow_of_funds_ids = []
    for i in flow_sub_cat:
        flow_of_funds_ids.append(get_series(i))
        get_sub_cat(i)

    # Flattens list of lists to list of flow of funds series ids
    flow_of_funds_ids = [val for sublist in flow_of_funds_ids for val in sublist]

    return flow_of_funds_ids


def download_all_observations(series_ids):
    """ This downloads all observations in separate files. Probably should not be used."""
    date = []
    value = []
    print(series_ids)
    for i in series_ids:

        print(i)
        temp = get_observation(i)
        temp = temp['observations']
        # pp.pprint(temp)

        for y, x in enumerate(temp):
            date.append(temp[y]['date'])
            value.append(temp[y]['value'])

        resulting_df = pd.DataFrame()
        resulting_df['date'] = date
        resulting_df['value'] = value
        resulting_df.to_csv('../FED_DATA/{0}.csv'.format(i), index=False)
        time.sleep(.2)


def get_source_ids(id):
    # From Category IDs, get all the source ids.
    r = requests.get(url='https://api.stlouisfed.org/fred/category/series?category_id={0}'.format(id), params=payload)
    r = r.json()

    return r


def main():
    # Find a sub categories of a given category
    sub_cat = get_sub_cat('32251')
    pp.pprint(sub_cat)

    # Find the series within a category
    sub_series = get_series('33246')
    pp.pprint(sub_series)

    # Extract time series data from particular series
    series_observations = get_observation('BOGZ1FA716140005A')
    print(series_observations)

    # Get all series ids for Flow of Funds data
    flow_of_funds_all = get_all_flow_funds_ids()
    print(flow_of_funds_all)

    download_all_observations(flow_of_funds_all)

    # Find flow of funds category and series id, get observation/data
    # Create a list of all the parent categories, append their ids to a list called parent_list
    # dict = a['categories']
    # parent_list = []
    # for a in dict:
    #     parent_list.append(a['id'])

    # This gives the children of one of the parent categories, in this case, National Accounts
    # r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32992'.format(KEY),
    #                  params=payload)
    # for i in parent_list:
    #     r = requests.get(url='https://api.stlouisfed.org/fred/children?category_id={0}'.format(i), params=payload)
    #     pp.pprint(r.json())

    # Need Flow of Funds observation/series data:
    # This gets the children categories for the National Accounts category; which contains the Flow of Funds category
    # r = requests.get(url='https://api.stlouisfed.org/fred/category/children?category_id=32992'.format(KEY),
    #                  params=payload)


if __name__ == '__main__':
    main()
