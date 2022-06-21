import pandas as pd

US_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
STATE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
US_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us.csv"
STATE_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"
URL_LIST = [US_DATA, STATE_DATA, US_ROLLING, STATE_ROLLING]


def import_data(url):
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    try:
        drop_list = ['fips', 'geoid']
        for column in drop_list:
            if column in df.keys():
                df.drop(columns=[column], inplace=True)
    except KeyError as err:
        print(f'No such key: {err}')
    return df
