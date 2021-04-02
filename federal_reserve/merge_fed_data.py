import json
import requests
import pprint
import pandas as pd
import time
import fed_data_api as fed

KEY = 'd87219606729528c27784921b44c5630'
BASE_URL = 'https://api.stlouisfed.org/fred/'

pp = pprint.PrettyPrinter()


def parse_metadata(id):
    # Incomplete, use to populate df with other relevant information
    metadata = fed.get_series(id)
    temp_list = []
    return temp_list


def remove_pre_1960():
    # Remove everything pre-1960
    fed_df = pd.read_csv('output_fed_merge.csv')
    fed_df = fed_df[fed_df.date >= 1960]
    fed_df.to_csv('output_fed_merge.csv', index=False)

    return fed_df


def append_observation(fed_data, id):
    obj = fed.get_observation(id)
    # metadata = fed.get_series(id)
    # pp.pprint(metadata)
    # print(id)
    obj = obj['observations']
    # pp.pprint(obj)

    temp_df = pd.DataFrame()
    temp_values = []
    temp_dates = []

    # Create temporary lists of values and dates
    for i in obj:
        temp_values.append(i['value'])
        temp_dates.append(i['date'])

    # Extract only the year from the date.
    for i, x in enumerate(temp_dates):
        temp_dates[i] = x[0:4]

    temp_df['date'] = temp_dates
    temp_df['value'] = temp_values

    fed_data = fed_data.append(temp_df)
    print(id, fed_data)

    # Need the sleep otherwise it fails, might be another throttling issue.
    time.sleep(2)
    return fed_data


def main():
    mapping = pd.read_csv('map_name_to_id.csv')
    series_ids = mapping['Series ID'].tolist()
    print(series_ids)

    fed_key_merged = pd.DataFrame()

    for i, x in enumerate(series_ids):
        fed_key_merged = append_observation(fed_key_merged, x)

    print(fed_key_merged)
    fed_key_merged.to_csv('output_fed_merge.csv', index=False)
    remove_pre_1960()


if __name__ == '__main__':
    main()
