import requests
from geopy.geocoders import Nominatim
import json
from datetime import datetime, timedelta, date
import re


def convert_c_to_f(temp_in_c, decimal_places):
    ret_val = 9.0 / 5.0 * float(temp_in_c) + 32
    return round(ret_val, decimal_places)


def get_mod_day_hour(date_with_modifier):
    modifier = date_with_modifier[26:]
    mod_days = re.findall(r'^P(\d+)D.*', modifier)
    mod_hours = re.findall(r'.*T(\d+)H$', modifier)
    if len(mod_days) == 1:
        mod_days = str(mod_days[0])
    else:
        mod_days = 0
    if len(mod_hours) == 1:
        mod_hours = str(mod_hours[0])
    else:
        mod_hours = 0

    return {
        'mod_days': mod_days,
        'mod_hours': mod_hours
    }


def get_date_hour_list(date_with_modifier):
    date = date_with_modifier[0:10]
    hour = int(date_with_modifier[11:13])

    mod_day_hours = get_mod_day_hour(date_with_modifier)
    mod_days = int(mod_day_hours.get("mod_days"))
    mod_hours = int(mod_day_hours.get("mod_hours"))

    mod_hours = mod_hours + (mod_days * 24)

    date_obj = datetime.strptime(date, "%Y-%m-%d")
    date_hour_list = []
    while int(mod_hours) > 0:
        if hour == 24:
            hour = 0
            date_obj = date_obj + timedelta(days=1)

        date_hour_list.append({
            'date': date_obj.strftime("%Y-%m-%d"),
            'hour': hour
        })

        hour = hour + 1
        mod_hours = mod_hours - 1

    return date_hour_list


def get_max_min_temp_values(json_list, return_a_list):
    """
    MaxTemperature and MinTemperature are unique and are parsed with this logic
    """
    ret_list = []
    ret_obj = {}
    for rec in json_list["values"]:
        valid_time = rec["validTime"]
        value = rec["value"]
        date = valid_time[0:10]

        new_obj = {
            'date': date,
            'value': value
        }
        ret_list.append(new_obj)
        ret_obj[date] = new_obj

    if return_a_list:
        return ret_list
    else:
        return ret_obj


def normalize_time_and_values(json_list, return_list):
    norm_time_val_obj = {}
    norm_time_val_list = []

    for rec in json_list["values"]:
        valid_time = rec["validTime"]
        value = rec["value"]

        date_hour_list = get_date_hour_list(valid_time)

        for date_hour in date_hour_list:
            date = date_hour.get("date")
            hour = date_hour.get("hour")
            new_val = {
                'date': date,
                'hour': hour,
                'value': value
            }
            norm_time_val_obj[date + "_" + str(hour)] = new_val
            norm_time_val_list.append(new_val)

    if return_list:
        return norm_time_val_list
    else:
        return norm_time_val_obj
    # for ntv in norm_time_val_list:
    #     print("Date:" + ntv.get("date") + " Hour:" + str(ntv.get("hour")) + " Value:" + str(ntv.get("value")))


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
        return res

    def get_weather_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_by_lat_long(location.latitude, location.longitude)

    def get_weather_forecast_by_lat_long(self, lat, long):
        weather = self.get_weather_by_lat_long(lat, long)

        def get_hourly_forecast(weather_json_str):
            weather_props = json.loads(weather_json_str.text)["properties"]
            hourly_temps = normalize_time_and_values(weather_props["temperature"], True)
            precipitation_probabilities = normalize_time_and_values(weather_props["probabilityOfPrecipitation"], False)
            wind_speeds = normalize_time_and_values(weather_props["windSpeed"], False)

            hourly_forecast = []
            count = 0
            for temp in hourly_temps:
                date = temp.get("date")
                hour = temp.get("hour")
                precipitation_probability = precipitation_probabilities[date + "_" + str(hour)]
                wind_speed = wind_speeds[date + "_" + str(hour)]
                hourly_forecast.append({
                    'date': date,
                    'hour': hour,
                    'temperature': convert_c_to_f(temp.get("value"), 0),
                    'precipitation_probability': precipitation_probability.get("value"),
                    'wind_speed': round(wind_speed.get("value"), 2)
                })
                count += 1
                if count == 24:
                    break
            return hourly_forecast

        def get_daily_forecast(weather_json_str):
            weather_props = json.loads(weather_json_str.text)["properties"]
            max_temps = get_max_min_temp_values(weather_props["maxTemperature"], True)
            min_temps = get_max_min_temp_values(weather_props["minTemperature"], False)

            hourly_forecast = []

            for temp in max_temps:
                d = temp.get("date")
                max_temp = temp.get("value")
                min_temp = min_temps.get(d, {}).get("value", None)
                day = datetime.strptime(d, "%Y-%m-%d").strftime('%A')
                if date.today().strftime("%Y-%m-%d") == d:
                    day = "Today"

                if min_temp:
                    hourly_forecast.append({
                        'date': d,
                        'day': day,
                        'max_temperature': convert_c_to_f(max_temp, 0),
                        'min_temperature': convert_c_to_f(min_temp, 0)
                    })

            return hourly_forecast

        hourly = get_hourly_forecast(weather)
        weather_forecast = {
            'hourly_forecast': hourly,
            'daily_forecast': get_daily_forecast(weather),
            'current_temp': hourly[0]['temperature']

        }
        return weather_forecast

    def get_weather_forecast_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_forecast_by_lat_long(location.latitude, location.longitude)

# weather_utils = WeatherUtil()
# weather_utils.get_weather_grid()
# weather_utils.get_location("raliegh, nc")
# print(weather_utils.get_weather_forecast_by_location_str("Raleigh"))
