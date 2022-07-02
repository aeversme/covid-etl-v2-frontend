import streamlit as st
from modules import data_handler as dh, data_sources as ds, map_handler as mh, markdown as md


@st.cache
def load_covid_data(url_list):
    return [dh.import_data(url) for url in url_list]


@st.cache
def load_geo_centers(url):
    return dh.import_data(url, filter_df=False)


def display_metrics(metric):
    title_type = '(Total)'
    dataframe = us_data
    cases_label = 'cases'
    deaths_label = 'deaths'
    if metric == 'rolling':
        title_type = '(Average per 100,000 people)'
        dataframe = us_rolling
        cases_label = 'cases_avg_per_100k'
        deaths_label = 'deaths_avg_per_100k'
    col1, col2, col3 = st.columns(3)
    col1.metric('Latest Data', dh.get_latest_date(dataframe).date().strftime('%b %d, %Y'))
    col2.metric(f'US Cases {title_type}',
                dh.format_metric(dh.get_latest_metric(cases_label, dataframe), metric),
                delta=dh.format_metric(dh.get_delta(cases_label, dataframe), metric),
                delta_color='inverse')
    col3.metric(f'US Deaths {title_type}',
                dh.format_metric(dh.get_latest_metric(deaths_label, dataframe), metric),
                delta=dh.format_metric(dh.get_delta(deaths_label, dataframe), metric),
                delta_color='inverse')


def data_to_map(met_type, loc):
    if met_type == 'rolling' and loc != 'United States':
        co_data = counties_rolling
        geo_j = counties_geojson
    elif loc != 'United States':
        co_data = counties_data
        geo_j = counties_geojson
    elif met_type == 'rolling':
        co_data = states_rolling
        geo_j = states_geojson
    else:
        co_data = states_data
        geo_j = states_geojson
    return [co_data, geo_j]


st.set_page_config(page_title='US & State Covid-19 Data', layout='wide')
st.title('US & State Covid-19 Data')
st.markdown(md.subtitle_markdown)

st.sidebar.title('Utilities')
st.sidebar.markdown('_Data processing status:_')
data_load_state = st.sidebar.text('Loading data and caching...')

us_data, states_data, us_rolling, states_rolling = load_covid_data(ds.US_STATES_LIST)
counties_data, counties_rolling = load_covid_data(ds.COUNTIES_2022_LIST)
geo_centers = load_geo_centers(ds.GEO_CENTERS)
states_geojson, counties_geojson = dh.load_json_data(ds.JSON_FILES)

data_load_state.text('Data loaded and cached!')

metric_type = 'total'
st.sidebar.markdown('_Check to see current rolling averages:_')
if st.sidebar.checkbox('Rolling averages'):
    metric_type = 'rolling'

display_metrics(metric_type)

location = st.sidebar.selectbox('View data by state:', geo_centers)
map_state = mh.set_map_state(geo_centers, location)
covid_data, geo_json = data_to_map(metric_type, location)
geo_json_with_data = dh.add_covid_data_to_json(covid_data, geo_json, location)
covid_map = mh.create_map(geo_json_with_data, map_state)

st.markdown(md.map_markdown)
st.pydeck_chart(covid_map)
st.markdown(md.map_credit)

st.sidebar.markdown('_App last updated: June 27, 2022_')
