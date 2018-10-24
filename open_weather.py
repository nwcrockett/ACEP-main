
"""
Help in understanding the resulting data

source: https://openweathermap.org/current
with the free account that I have no more that 60 calls per minute can be made
Variable breakdown for the resulting csv
temp: all in Kelvin
weather.main: A grouping of weather parameters. Example Rain, Snow, Extreme etc.
weather.description: Further description of of the weather main. Example main is cloudy so
    description can be "broken clouds, fully cloudy, etc"
Humidity: %
wind.speed: meter/sec
"""
import urllib
import json
import pandas as pd
from pandas.io.json import json_normalize


def new_open_weather_data(latitude, longitude, key, file_output_name="Resulting_Open_Weather", output_type="json"):
    """
    key: API key. If you need it ask Nelson
clean_up_data: the "weather" key in the original dataframe is a list with a dict inside.
    clean_up_data is used to break it up so that each element of the data in now in a separate column
    :param latitude:
    :param longitude:
    :param key: API key foe open weather
    :param file_output_name: output file
    :return:
    """
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + \
          str(latitude) + "&lon=" + str(longitude) + "&APPID=" + key
    response = urllib.request.urlopen(url)
    html = response.read()
    data = json.loads(html)
    if output_type == "json":
        with open(file_output_name + ".json", 'w') as outfile:
            json.dump(data, outfile)
    else:
        df_open = json_normalize(data)
        clean_up_data = df_open["weather"].apply(pd.Series)
        clean_up_data = pd.DataFrame.from_dict(clean_up_data[0][0], orient="index")
        clean_up_data = clean_up_data.transpose()
        clean_up_data = clean_up_data.rename(columns={"id": "weather.id", "main": "weather.main",
                                                      "description": "weather.description", "icon": "weather.icon"})
        df_open = df_open.drop(columns=["weather"])
        df_open = df_open.join(clean_up_data)
        df_open.to_csv(file_output_name + ".csv")

