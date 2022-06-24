import pandas as pd


def import_data(url):
    df = pd.read_csv(url)
    return filter_data(df)


def filter_data(dataframe):
    """
    Filter dataframe.
    :param dataframe:
    :return:
    """
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    return dataframe
