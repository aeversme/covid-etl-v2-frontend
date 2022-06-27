import pandas as pd
from re import search
from modules import data_handler, map_handler
import datetime
# import requests

STATES_JSON_URL = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json"
COUNTIES_JSON_URL = "https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_5m.json"
GEO_CENTERS = "https://raw.githubusercontent.com/aeversme/us-state-geocenters/main/geo_centers.csv"

US_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
STATE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

us_data = data_handler.import_data(US_DATA)
print(us_data.tail(3))

state_data = data_handler.import_data(STATE_DATA)
print(state_data.tail(3))

latest_date = us_data['date'].max()
print(latest_date)

previous_day = latest_date + datetime.timedelta(days=-1)
print(previous_day)

day_list = [latest_date, previous_day]

us_data_filtered = us_data[us_data['date'].isin(day_list)]
print(us_data_filtered)

state_data_filtered = state_data[state_data['date'].isin(day_list)]
print(len(state_data_filtered))

#
# us_dates = [item['date'] for item in us_data]
# print(len(us_dates))


# def get_json(url):
#     json = None
#     response = requests.get(url)
#     if response.raise_for_status() is None:
#         try:
#             json = response.json()
#         except requests.exceptions.ContentDecodingError:
#             print("JSON could not be decoded.")
#     return json
#
#
# states_geojson = get_json(STATES_JSON_URL)
#
# print(type(states_geojson))
# print(len(states_geojson['features']))
#
# for index, value in enumerate(states_geojson['features']):
#     if value['properties']['NAME'] == 'Puerto Rico':
#         states_geojson['features'].pop(index)
# print(index, f"{value['properties']['NAME']}: STATE {value['properties']['STATE']}")
# print(type(states_geojson['features'][0]['geometry']['coordinates'][0][0][0][0]))
# for i in range(len(states_geojson['features'])):
#     print(states_geojson['features'][i]['properties']['NAME'])


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
