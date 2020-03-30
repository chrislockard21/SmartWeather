import requests
from geopy.geocoders import Nominatim
# import json


def convert_c_to_f(temp_in_c, decimal_places):
    ret_val = 9.0 / 5.0 * float(temp_in_c) + 32
    return round(ret_val, decimal_places)


# from datetime import datetime
# from dateutil import tz
# def convert_utc_to_local(utc_date_time):
#     from_zone = tz.gettz('GMT')
#     to_zone = tz.tzlocal()
#     utc = datetime.strptime(utc_date_time, '%Y-%m-%d %H:%M:%S')
#     utc = utc.replace(tzinfo=from_zone)
#     return utc.astimezone(to_zone)


def get_temp_list(weather):
    temp_list = []
    for temp in weather.get("properties").get("temperature").get("values"):
        temp_list.append({
            "datetime": temp.get("validTime")[0:13],
            "temp": convert_c_to_f(temp.get("value"), 0)
        })
    return temp_list


def get_max_temp_list(weather):
    max_temp_list = []
    for temp in weather.get("properties").get("maxTemperature").get("values"):
        max_temp_list.append({
            "datetime": temp.get("validTime")[0:10],
            "temp": convert_c_to_f(temp.get("value"), 0)
        })
        # max_temp_list += dict({
        #     "datetime": temp.get("validTime")[0:10],
        #     "temp": convert_c_to_f(temp.get("value"))
        # })
    return max_temp_list


def get_min_temp_list(weather):
    temp_list = []
    for temp in weather.get("properties").get("minTemperature").get("values"):
        temp_list.append({
            'datetime': temp.get("validTime")[0:10],
            'temp': convert_c_to_f(temp.get("value"), 0)
        })
    return temp_list


class WeatherUtil:
    # API Docs: https://www.weather.gov/documentation/services-web-api

    def __init__(self):
        self.request_header = {
            'User-Agent': 'smartweather@gmail.com',
            'Accept': 'application/geo+json'
        }
        self.base_url = 'https://api.weather.gov/'

    """ 
    weather.gov manages grids of weather information, need to know the grid before getting the weather report
    latitude and longitude needed to find a grid
    """
    def get_weather_grid(self, lat, long):
        req_url = self.base_url + "points/" + str(lat) + "%2C" + str(long)
        grid = requests.get(req_url, headers=self.request_header)
        return grid.json()

    def get_location(self, locaction_str):
        geo_locator = Nominatim(user_agent="smartweatherapp")
        location = geo_locator.geocode(locaction_str)
        return location

    def get_weather_by_lat_long(self, lat, long):
        grid = self.get_weather_grid(lat, long)
        cwa = grid.get("properties").get("cwa")
        grid_x = grid.get("properties").get("gridX")
        grid_y = grid.get("properties").get("gridY")
        print("latitude({0}), longitude({1}), cwa({2}), gridx({3}), gridy({4})"
              .format(lat, long, str(cwa), str(grid_x), str(grid_y)))

        url = self.base_url + "gridpoints/" + str(cwa) + "/" + str(grid_x) + "," + str(grid_y)
        res = requests.get(url, headers=self.request_header)
        return res.json()

    def get_weather_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_by_lat_long(location.latitude, location.longitude)

    def get_weather_forcast_by_lat_long(self, lat, long):
        weather = self.get_weather_by_lat_long(lat, long)
        weather_forecast = {
            # 'temps':        weather.get("properties").get("temperature").get("values"),
            'max_temps':    get_max_temp_list(weather),
            'min_temps':    get_min_temp_list(weather)
        }
        return weather_forecast

    def get_weather_forecast_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_forcast_by_lat_long(location.latitude, location.longitude)


# weather_utils = WeatherUtil()
# weather_utils.get_weather_grid()
# weather_utils.get_location("raliegh, nc")
# print("weather test: " + str(weather_utils.get_weather_by_location_str("Raleigh")))
# print(convert_c_to_f("13.333"), 0)
# print(convert_utc_to_local("2020-03-23 08:00:00"))

# print(weather_utils.get_weather_forecast_by_location_str("Raleigh"))
