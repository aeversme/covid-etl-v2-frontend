import pydeck as pdk
from re import search


def set_map_state(df, location='United States'):
    for index in df.index:
        if search(location, df['location'][index]):
            zoom = 2.5
            pitch = 0
            if location != 'United States':
                zoom = 6
                pitch = 30
            return {'lat': df.lat[index], 'lon': df.lon[index], 'zoom': zoom, 'pitch': pitch}


def create_map(geojson_data, map_state):
    view_state = pdk.ViewState(latitude=map_state['lat'],
                               longitude=map_state['lon'],
                               zoom=map_state['zoom'],
                               bearing=0,
                               pitch=map_state['pitch']
                               )

    geojson_layer = pdk.Layer('GeoJsonLayer',
                              geojson_data,
                              opacity=0.8,
                              stroked=True,
                              filled=True,
                              extruded=True,
                              wireframe=True,
                              # get_elevation='some_data_if_using_this',
                              # get_fill_color='[255, 255, data_translated_to_255_scale]',
                              get_line_color=[255, 255, 255],
                              pickable=True
                              )

    layers = [geojson_layer]

    # TODO: add map_style argument?
    covid_map = pdk.Deck(map_provider='mapbox',
                         layers=layers,
                         # map_style=a_map_style_if_desired,
                         initial_view_state=view_state
                         )

    return covid_map
