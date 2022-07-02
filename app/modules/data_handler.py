import pandas as pd
import json
import datetime


def load_json_data(files):
    return [json.load(open(file)) for file in files]


def import_data(url, filter_df=True):
    df = pd.read_csv(url)
    if filter_df:
        return filter_data(df)
    return df


def filter_data(df):
    df['date'] = pd.to_datetime(df['date'])
    return df


def get_latest_date(df):
    return df['date'].max()


def get_associated_metric(date, column_label, df):
    return df.loc[df['date'] == date, column_label].values[0]


def get_latest_metric(column_label, df):
    latest_date = get_latest_date(df)
    return get_associated_metric(latest_date, column_label, df)


def get_delta(column_label, df):
    latest_date = get_latest_date(df)
    previous_date = latest_date + datetime.timedelta(days=-1)
    latest_value = df.loc[df['date'] == latest_date, column_label].values[0]
    previous_value = df.loc[df['date'] == previous_date, column_label].values[0]
    return latest_value - previous_value


def format_metric(metric, metric_type):
    if metric_type == 'rolling':
        return '{:.2f}'.format(metric)
    return '{:,}'.format(metric)
