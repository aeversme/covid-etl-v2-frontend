import pandas as pd
import json
import datetime

COLORS = {
    0: {
        'red': 255,
        'green': 255,
        'blue': 255
    },
    1: {
        'red': 255,
        'green': 186,
        'blue': 186
    },
    2: {
        'red': 255,
        'green': 123,
        'blue': 123
    },
    3: {
        'red': 255,
        'green': 82,
        'blue': 82
    },
    4: {
        'red': 255,
        'green': 0,
        'blue': 0
    },
    5: {
        'red': 167,
        'green': 0,
        'blue': 0
    }
}

COLORS_LISTS = {
    0: [255, 255, 255],
    1: [255, 186, 186],
    2: [255, 123, 123],
    3: [255, 82, 82],
    4: [255, 0, 0],
    5: [167, 0, 0]
}


def load_json_data(files):
    return [json.load(open(file)) for file in files]


def import_data(url, filter_df=True):
    df = pd.read_csv(url)
    if filter_df:
        return filter_data(df)
    return df


def filter_data(df):
    df['date'] = pd.to_datetime(df['date'])
    labels = ['fips', 'cases', 'deaths']
    for label in labels:
        df[label] = df[label].fillna(value=0)
        df = df.astype({label: 'int64'})
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


def set_color_from_data(data, label='cases'):
    data_range = [1, 2e+06, 4e+06, 6e+06, 8e+06]
    if label == 'deaths':
        data_range = [1, 2e+04, 4e+04, 6e+04, 8e+04]
    color = COLORS[5]
    for i, num in enumerate(data_range):
        if float(data) > num:
            color = COLORS_LISTS[i + 1]
    return color


def add_covid_data_to_json(covid_data, geojson, location):
    data_label = ['cases', 'deaths']
    colors = ['red', 'green', 'blue']
    for feature in geojson['features']:
        location_identifier = int(feature['properties']['STATE'])
        if location != 'United States':
            location_identifier = int(feature['properties']['STATE'] + feature['properties']['COUNTY'])
        for label in data_label:
            try:
                feature['properties'][label] = str(covid_data.loc[covid_data['fips'] ==
                                                                  location_identifier, label].values[-1])
                # color_dict = set_color_from_data(feature['properties'][label])
                # for color in colors:
                #     feature['properties'][f'{label}{color}color'] = color_dict[f'{color}']
                feature['properties'][f'{label}color'] = set_color_from_data(feature['properties'][label])
            except IndexError:
                # for color in colors:
                #     feature['properties'][f'{label}{color}color'] = '255'
                feature['properties'][f'{label}color'] = COLORS_LISTS[0]
                continue
    return geojson
