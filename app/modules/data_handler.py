import pandas as pd
import requests


def import_data(url, filter_df=True):
    df = pd.read_csv(url)
    if filter_df:
        return filter_data(df)
    return df


def filter_data(df):
    df['date'] = pd.to_datetime(df['date'])
    return df


def load_json(url):
    json = None
    response = requests.get(url)
    if response.raise_for_status() is None:
        try:
            json = response.json()
        except requests.exceptions.ContentDecodingError:
            print("JSON could not be decoded.")
    return json


def get_latest_date(column):
    return column.max()


# TODO: convert to using latest date - add dataframe to parameters, call get_latest_date
def get_latest_data(column):
    data = column.iat[-1]
    return '{:,}'.format(data)


# TODO: convert to using latest date and day-1 - add dataframe to parameters, call get_latest_date
def get_delta(column, metric_type=None):
    delta = column.iat[-1] - column.iat[-2]
    if metric_type == 'rolling':
        return '{:.2f}'.format(delta)
    return '{:,}'.format(delta)
