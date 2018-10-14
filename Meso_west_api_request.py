# source of API keys https://synopticlabs.org/api/guides/?getstarted
# to get a token https://api.mesowest.net/v2/auth?apikey=Kz0A8wRVMV8igVGtlXEtIbSRzRrd2vV2l2G
# variable reference https://synopticlabs.org/api/mesonet/reference/#stationstimeseries
# beginners help guide https://blog.synopticlabs.org/blog/2016/06/07/mesonet-api-for-beginners.html
# assist in developing correct URl string https://synopticlabs.org/api/explore/

import urllib
import json
import time
import pandas as pd

'''
This is a token service that is used by the Meso West api as a key to determine who the user is and 
is then used by any further API data requests

You will need to get a API key to have this fucntion work from https://synopticlabs.org/api/guides/?getstarted
'''
def get_a_new_token(key):
    url = "https://api.mesowest.net/v2/auth?apikey=" + key
    response = urllib.request.urlopen(url)
    html = json.loads(response.read())

    return html["TOKEN"]

'''
key: API key for the Meso West service. Obtian a key from https://synopticlabs.org/api/guides/?getstarted
latitude: the point latitude
longitude: the point longitude
point_radius: the radius of the circle that is used to find the station in the area. Default is 10 miles
time: Time that is being used to make the request. Needs to be in format year-month-day-hour-minutes.
    example of required input "201810081210". Will default to the current time on the machine
station_number: the cap on the number of reporting stations for the given request. Default is 1
oldest_datapoint: the oldest value acceptable for the given request. In minutes
units: either english or metric units are possible. Default is english
simple: Method to change the resulting csv file to either a file with only a recorded time and sensor value
    or a file the includes a bunch of the station data. Default is False
    
This function will make a API request to the Meso West API. It will take a point from a given latitude and longitude
then from a radius around that point the request will be made. The resulting data will be outputted into a csv file.
'''
def new_staion_data(key, latitude, longitude, file_output_name="Resulting Weather.csv", point_radius=10, time=time.strftime("%Y%m%d%H%m"),
                                   station_number=1, oldest_datapoint=60, units="english", simple=False):
    url = "https://api.synopticlabs.org/v2/stations/nearesttime?&token="\
          + get_a_new_token() + "&attime=" + str(time) + "&within=" + str(oldest_datapoint) + "&obtimezone=local"\
          +"&state=AK&country=us&status=active&radius=" + str(latitude) + "," + \
          "%20" + str(longitude) + "," + str(point_radius) + "&limit=" + str(station_number) + "&units=" + units
    response = urllib.request.urlopen(url)
    html = response.read()
    data = json.loads(html)

    df_station_observation = pd.DataFrame.from_dict(data["STATION"][0])
    df_remove_no_observations = df_station_observation.dropna(how="all", subset=["OBSERVATIONS"])
    df_time_observation_value = df_remove_no_observations["OBSERVATIONS"].apply(pd.Series)

    if simple:
        df_time_observation_value.to_csv(file_output_name)
    else:
        df_values_with_station_data = pd.concat([df_remove_no_observations, df_time_observation_value], axis=1).drop(
            "OBSERVATIONS", axis=1)
        df_values_with_station_data.to_csv(file_output_name)
