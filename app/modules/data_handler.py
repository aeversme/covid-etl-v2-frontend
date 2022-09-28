import pandas as pd
import json
import datetime

COLORS_DICT = {
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


# TODO: add transform for US 'geoid' to be last two digits - check format in counties, probably a different transform
def filter_data(df):
    df['date'] = pd.to_datetime(df['date'])
    labels = ['fips', 'cases', 'deaths']
    for label in labels:
        if label in df.keys():
            df[label] = df[label].fillna(value='0')
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


def format_location_identifier(feature, loc, met_type):
    if met_type == 'rolling' and loc != 'United States':
        # counties in state map, rolling
        location_id = 'USA-' + feature['properties']['STATE'] + feature['properties']['COUNTY']
    elif loc != 'United States':
        # counties in state map, totals
        location_id = int(feature['properties']['STATE'] + feature['properties']['COUNTY'])
    elif met_type == 'rolling':
        # states in US map, rolling
        location_id = 'USA-' + feature['properties']['STATE']
    else:
        # states in US map, totals
        location_id = int(feature['properties']['STATE'])
    return location_id


def set_color_from_data(data, is_us, met_type):
    if met_type == 'rolling' and not is_us:
        # counties in state map, rolling
        data_range = [1, 5, 10, 15, 20]
    elif not is_us:
        # counties in state map, totals
        data_range = [1, 3e+03, 5e+04, 3e+05, 1e+06]
    elif met_type == 'rolling':
        # states in US map, rolling
        data_range = [1, 5, 10, 15, 20]
    else:
        # states in US map, totals
        data_range = [1, 5e+05, 1.5e+06, 3e+06, 6e+06]

    color = COLORS_DICT[5]
    data = ''.join(data.split(','))
    for i, num in enumerate(data_range):
        if float(data) > num:
            color = COLORS_DICT[i + 1]
    return color


def add_covid_data_to_json(covid_data, geojson, location, metric_type):
    data_label = ['cases', 'deaths']
    if metric_type == 'rolling':
        data_label = ['cases_avg_per_100k', 'deaths_avg_per_100k']

    is_us = True
    if location != 'United States':
        is_us = False

    # TODO: this feels cumbersome
    location_data_column = None
    if 'fips' in covid_data.keys():
        location_data_column = covid_data['fips']
    elif 'geoid' in covid_data.keys():
        location_data_column = covid_data['geoid']
    else:
        print('Location header key not found.')

    for feature in geojson['features']:
        # TODO: function here to transform location_identifier into same format as 'fips' or 'geoid' columns in
        #  covid_data
        # location_identifier = int(feature['properties']['STATE'])
        location_identifier = format_location_identifier(feature, location, metric_type)
        if not is_us:
            location_identifier = int(feature['properties']['STATE'] + feature['properties']['COUNTY'])
        for label in data_label:
            try:
                if label in covid_data.keys():
                    feature['properties'][label] = '{:,}'.format(covid_data.loc[location_data_column ==
                                                                                location_identifier, label].values[-1])
                    feature['properties'][f'{label}color'] = set_color_from_data(feature['properties'][label],
                                                                                 is_us,
                                                                                 metric_type)
            except IndexError:
                feature['properties'][f'{label}color'] = COLORS_DICT[0]
                continue
    return geojson
