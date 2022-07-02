import pandas as pd
from re import search
from modules import data_handler as dh, map_handler
import datetime
import json
import requests

STATES_JSON_URL = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json"
COUNTIES_JSON_URL = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_5m.json"
GEO_CENTERS = "https://raw.githubusercontent.com/aeversme/us-state-geocenters/main/geo_centers.csv"

US_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
STATE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
COUNTY_2022_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv"

state_data = dh.import_data(STATE_DATA)
print(state_data.tail(3))

county_data = dh.import_data(COUNTY_2022_DATA)
print(county_data.tail(3))


#
# latest_date = us_data['date'].max()
# print(latest_date)
#
# previous_day = latest_date + datetime.timedelta(days=-1)
# print(previous_day)
#
# day_list = [latest_date, previous_day]
#
# us_data_filtered = us_data[us_data['date'].isin(day_list)]
# print(us_data_filtered)
#
# state_data_filtered = state_data[state_data['date'].isin(day_list)]
# print(len(state_data_filtered))

#
# us_dates = [item['date'] for item in us_data]
# print(len(us_dates))


def get_json(url):
    json = None
    response = requests.get(url)
    if response.raise_for_status() is None:
        try:
            json = response.json()
        except requests.exceptions.ContentDecodingError:
            print("JSON could not be decoded.")
    return json


states_geojson = get_json(STATES_JSON_URL)
counties_json = get_json(COUNTIES_JSON_URL)

print(type(states_geojson))
print(len(states_geojson['features']))
print(counties_json['features'][0]['properties'])

#
# for index, value in enumerate(states_geojson['features']):
#     if value['properties']['NAME'] == 'Puerto Rico':
#         states_geojson['features'].pop(index)
# print(index, f"{value['properties']['NAME']}: STATE {value['properties']['STATE']}")
# print(type(states_geojson['features'][0]['geometry']['coordinates'][0][0][0][0]))

# print(state_data.loc[state_data['fips'] == int('01'), 'cases'])
# print(county_data.loc[county_data['fips'] ==
#                       float(counties_json['features'][2]['properties']['STATE'] +
#                             counties_json['features'][2]['properties']['COUNTY']), 'cases'].values[-1])


def add_covid_data_to_json(covid_data, geojson, location='United States'):
    data_label = ['cases', 'deaths']
    for feature in geojson['features']:
        location_identifier = int(feature['properties']['STATE'])
        if location != 'United States':
            location_identifier = float(feature['properties']['STATE'] + feature['properties']['COUNTY'])
        for label in data_label:
            try:
                feature['properties'][label.upper()] = str(covid_data.loc[covid_data['fips'] == location_identifier, label].values[-1])
            except IndexError:
                continue
    print(f'Type of the modified geojson in the function: {type(geojson)}')

    # WHY DOES THIS NOT RETURN A VALID DICTIONARY???

    return geojson


states_json_with_extra_data = add_covid_data_to_json(state_data, states_geojson)
print(states_json_with_extra_data['features'][0]['properties'])
print(type(states_json_with_extra_data))

counties_json_with_extra_data = add_covid_data_to_json(county_data, counties_json, 'Alabama')
print(counties_json_with_extra_data['features'][0]['properties'])
print(type(counties_json_with_extra_data))

# def load_geo_centers(url):
#     return data_handler.import_data(url, filter_df=False)
#
#
# geo_centers = load_geo_centers(GEO_CENTERS)
# print(geo_centers.head(5))
# print(geo_centers.keys())
# print(geo_centers.state[2])
#
# map_state = map_handler.set_map_state(geo_centers, 'Mississippi')
# print(map_state)


# def get_coordinates(df, location='United States'):
#     for index in df.index:
#         if search(location, df['location'][index]):
#             return [df.lat[index], df.lon[index]]
#
#
# lat_lon = get_coordinates(geocenters)
# print(lat_lon)
# print(lat_lon[0])
# print(type(lat_lon[0]))
