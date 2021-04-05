import requests
import pandas as pd
import json
from datetime import date
import pprint

API_KEY = 'f9e4a8b8496e4c519a56caab831c4eaa'

# Daily limit of 25 queries!!! Registering is supposed to increase limit to 500, but that did not seem to work.


def grab_bls_data(start_year, end_year):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['LNU00000000'], "startyear": start_year, "endyear": end_year})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    print(json_data)

    for series in json_data['Results']['series']:
        print(series)
        seriesId = series['seriesID']
        year = []
        period = []
        value = []
        for item in series['data']:
            if item['period'] == 'M01':
                print(item)
                year.append(item['year'])
                period.append(item['period'])
                value.append(item['value'])

        data = pd.DataFrame()
        data['Year'] = year
        data['Annual'] = value

        data.to_csv('{0}.csv'.format(seriesId), index=False)
    pass


def main():
    current_date = date.today()
    print(current_date.year)

    grab_bls_data(2011, current_date.year)


if __name__ == '__main__':
    main()
