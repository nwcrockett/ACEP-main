
# accu weather API https://developer.accuweather.com/apis

import urllib
import json
from pandas.io.json import json_normalize


def get_location_key(key, latitude, longitude):
    """
    source of url: https://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/cities/geoposition/search
    This function is required since the station API will only take in location keys. This function gets that key
    :param key: API key
    :param latitude:
    :param longitude:
    :return: the station key
    """
    url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + \
    key + "&q=" + str(latitude) + "%2C%20" + str(longitude)
    response = urllib.request.urlopen(url)
    html = response.read()
    data = json.loads(html)
    return data["Key"]


def accu_api_request(key, latitude, longitude, file_output_name="Resulting_Accu_Weather", details="true"
                     , output_type="json"):
    """
    source of url: https://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D
    Makes request. Then outputs the data to a csv with a single row.
    If details is true a lot of information will be returned. If details is not true only the
    temperature will be returned.
    :param key: API key for ACCU weather
    :param latitude:
    :param longitude:
    :param file_output_name: name of the file
    :param details: Adds in further information from the request. If details is true a lot of information
     will be returned. If details is not true only the temperature will be returned.
    :param output_type: Changes the output type of
    :return:
    """

    if details is not "true" and details is not "false":
        raise ValueError("details must be a string of either true or false")
    url = "http://dataservice.accuweather.com/currentconditions/v1/" + \
          get_location_key(key, latitude, longitude) + "?apikey=" + key + "&details=" + details
    response = urllib.request.urlopen(url)
    html = response.read()
    data = json.loads(html)
    if output_type == "json":
        with open(file_output_name + ".json", 'w') as outfile:
            json.dump(data, outfile)
    else:
        df_accu = json_normalize(data)
        df_accu.to_csv(file_output_name + ".csv")

