import pydeck as pdk
from re import search
import geopandas as gpd


# TODO: different zoom levels depending on state size
def set_map_state(df, location='United States'):
    for index in df.index:
        if search(location, df['location'][index]):
            state = None
            zoom = 2.5
            pitch = 0
            if location != 'United States':
                state = f"{int(df['state'][index]):02d}"
                zoom = 5.5
            return {'location': location,
                    'state': state,
                    'lat': df.lat[index],
                    'lon': df.lon[index],
                    'zoom': zoom,
                    'pitch': pitch}


def create_map(geojson_data, map_state, metric_type):
    state = map_state['state']
    if state is not None:
        features = []
        for feature in geojson_data['features']:
            if feature['properties']['STATE'] == state:
                features.append(feature)
        geojson_data = features

    geodata = gpd.GeoDataFrame.from_features(geojson_data)

    view_state = pdk.ViewState(latitude=map_state['lat'],
                               longitude=map_state['lon'],
                               zoom=map_state['zoom'],
                               bearing=0,
                               pitch=map_state['pitch']
                               )

    fill_color = {
        'total': 'properties.casescolor',
        'rolling': 'properties.cases_avg_per_100kcolor'
    }

    geojson_layer = pdk.Layer('GeoJsonLayer',
                              geojson_data,
                              id='jsonlayer',
                              opacity=0.5,
                              stroked=True,
                              filled=True,
                              extruded=True,
                              wireframe=True,
                              get_fill_color=fill_color[metric_type],
                              get_line_color=[255, 255, 255],
                              pickable=False
                              )

    tooltip_layer = pdk.Layer('GeoJsonLayer',
                              geodata,
                              id='tooltiplayer',
                              opacity=0,
                              stroked=True,
                              filled=True,
                              extruded=True,
                              wireframe=True,
                              get_line_color=[255, 255, 255],
                              pickable=True
                              )

    layers = [geojson_layer, tooltip_layer]

    tooltip = {
        'total': {
            'text': '{NAME}\nCases: {cases}\nDeaths: {deaths}'
        },
        'rolling': {
            'text': '{NAME}\nCases per 100k: {cases_avg_per_100k}\nDeaths per 100k: {deaths_avg_per_100k}'
        }
    }

    # TODO: add map_style argument?
    covid_map = pdk.Deck(map_provider='mapbox',
                         layers=layers,
                         # map_style=a_map_style_if_desired,
                         initial_view_state=view_state,
                         tooltip=tooltip[metric_type]
                         )

    return covid_map
