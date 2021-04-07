import pandas as pd
import fed_data_api as fed
import pprint
import requests

KEY = 'd87219606729528c27784921b44c5630'

payload = {
    'api_key': KEY,
    'file_type': 'json',
    'frequency': 'a'
}


def main():
    r = requests.get(url='https://api.stlouisfed.org/fred/series/observations?series_id=CNP16OV', params=payload)
    population_lvl = r.json()
    population_lvl = population_lvl['observations']

    date = []
    value = []
    for i in population_lvl:
        date.append(i['date'])
        value.append(i['value'])

    for i, x in enumerate(date):
        date[i] = x[0:4]

    data_df = pd.DataFrame()
    data_df['date'] = date
    data_df['value'] = value

    data_df.to_csv('labor_data.csv', index=False)


if __name__ == '__main__':
    main()
