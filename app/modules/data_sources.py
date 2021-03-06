US_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
US_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us.csv"

STATE_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
STATE_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"

COUNTY_2020_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2020.csv"
COUNTY_2020_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties" \
                      "-2020.csv "

COUNTY_2021_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2021.csv"
COUNTY_2021_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties" \
                      "-2021.csv "

COUNTY_2022_DATA = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv"
COUNTY_2022_ROLLING = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-counties" \
                      "-2022.csv "

GEO_CENTERS = "https://raw.githubusercontent.com/aeversme/us-state-geocenters/main/geo_centers.csv"

US_STATES_LIST = [US_DATA,
                  STATE_DATA,
                  US_ROLLING,
                  STATE_ROLLING]
COUNTIES_LIST = [COUNTY_2020_DATA,
                 COUNTY_2021_DATA,
                 COUNTY_2022_DATA,
                 COUNTY_2020_ROLLING,
                 COUNTY_2021_ROLLING,
                 COUNTY_2022_ROLLING]
COUNTIES_2022_LIST = [COUNTY_2022_DATA, COUNTY_2022_ROLLING]
JSON_FILES = ['app/src/json/states.json', 'app/src/json/counties.json']
