import streamlit as st
from modules import data_handler as dh, data_sources as ds, map_handler as mh


@st.cache
def load_covid_data(url_list):
    return [dh.import_data(url) for url in url_list]


@st.cache
def load_geo_centers(url):
    return dh.import_data(url, filter_df=False)


def display_metrics(metric):
    title_type = '(Total)'
    cases = us_data['cases']
    deaths = us_data['deaths']
    if metric == 'rolling':
        title_type = '(Average per 100,000 people)'
        cases = us_rolling['cases_avg_per_100k']
        deaths = us_rolling['deaths_avg_per_100k']
    col1, col2, col3 = st.columns(3)
    col1.metric('Latest Data', dh.get_latest_date(us_data['date']).date().strftime('%b %d, %Y'))
    col2.metric(f'US Cases {title_type}',
                dh.get_latest_data(cases),
                delta=dh.get_delta(cases, metric),
                delta_color='inverse')
    col3.metric(f'US Deaths {title_type}',
                dh.get_latest_data(deaths),
                delta=dh.get_delta(deaths, metric),
                delta_color='inverse')


def data_to_map(met_type, loc):
    if met_type == 'rolling' and loc != 'United States':
        co_data = states_rolling
        geo_j = counties_geojson
    elif loc != 'United States':
        co_data = states_data
        geo_j = counties_geojson
    elif met_type == 'rolling':
        co_data = us_rolling
        geo_j = states_geojson
    else:
        co_data = us_data
        geo_j = states_geojson

    return [co_data, geo_j]


subtitle_markdown = """
_A Python ETL project on AWS_
***
"""

st.set_page_config(page_title='US & State Covid-19 Data', layout='wide')
st.title('US & State Covid-19 Data')
st.markdown(subtitle_markdown)

st.sidebar.title('Utilities')
st.sidebar.markdown('_Data processing status:_')
data_load_state = st.sidebar.text('Loading data and caching...')

us_data, states_data, us_rolling, states_rolling = load_covid_data(ds.US_STATES_LIST)
geo_centers = load_geo_centers(ds.GEO_CENTERS)
states_geojson = dh.load_json(ds.STATES_GEOJSON)
counties_geojson = dh.load_json(ds.COUNTIES_GEOJSON)

data_load_state.text('Data loaded and cached!')

metric_type = 'total'
st.sidebar.markdown('_Check to see current rolling averages:_')
if st.sidebar.checkbox('Rolling averages'):
    metric_type = 'rolling'

display_metrics(metric_type)

location = st.sidebar.selectbox('View data by state:', geo_centers)
map_state = mh.set_map_state(geo_centers, location)
covid_data, geo_json = data_to_map(metric_type, location)
covid_map = mh.create_map(geo_json, map_state)

st.pydeck_chart(covid_map)

st.sidebar.markdown('_App last updated: June 27, 2022_')
