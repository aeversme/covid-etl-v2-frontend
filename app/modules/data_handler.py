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
