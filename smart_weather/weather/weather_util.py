import requests, sys, traceback
from geopy.geocoders import Nominatim
import json
from datetime import datetime, timedelta, date
import re


def current_location():
    send_url = 'http://api.ipstack.com/check?access_key=ee0f77cc3b12451b989fccfde279255f'
    resp = requests.get(send_url)
    return json.loads(resp.text)


def convert_c_to_f(temp_in_c, decimal_places):
    ret_val = 9.0 / 5.0 * float(temp_in_c) + 32
    return round(ret_val, decimal_places)


def convert_kts_to_mph(speed_in_kts, decimal_places):
    ret_val = float(speed_in_kts) * 1.15078
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


def get_previous_date(_date):
    date_obj = datetime.strptime(_date, "%Y-%m-%d")
    date_obj = date_obj - timedelta(days=1)
    return date_obj.strftime("%Y-%m-%d")


def normalize_date_hour(_date, hour):
    new_date = _date
    new_hour = hour-5
    if new_hour < 0:
        new_date = get_previous_date(_date)
        new_hour = new_hour + 24
    return {
        'norm_date': new_date,
        'norm_hour': new_hour
    }


def get_date_hour_list(date_with_modifier):
    _date = date_with_modifier[0:10]
    hour = int(date_with_modifier[11:13])
    norm_date_hour = normalize_date_hour(_date, hour)
    _date = norm_date_hour['norm_date']
    hour = norm_date_hour['norm_hour']

    mod_day_hours = get_mod_day_hour(date_with_modifier)
    mod_days = int(mod_day_hours.get("mod_days"))
    mod_hours = int(mod_day_hours.get("mod_hours"))

    mod_hours = mod_hours + (mod_days * 24)

    date_obj = datetime.strptime(_date, "%Y-%m-%d")
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
        _date = valid_time[0:10]

        new_obj = {
            'date': _date,
            'value': value
        }
        ret_list.append(new_obj)
        ret_obj[_date] = new_obj

    if return_a_list:
        return ret_list
    else:
        return ret_obj


def get_daily_values(json_list, return_a_list):
    """
    Get the min values from a list for a day
    :param op_type:
    :param json_list:
    :param return_a_list:
    :return:
    """
    norm_values = normalize_time_and_values(json_list, True)

    ret_list = []
    ret_obj = {}
    cur_max_val = None
    cur_min_val = None
    cur_date = None
    cur_total = 0
    cur_cnt = 0
    for norm_value in norm_values:
        norm_date = norm_value['date']
        norm_val = norm_value['value']

        if not cur_date:
            cur_date = norm_date
            cur_max_val = norm_val
            cur_min_val = norm_val
            cur_total = norm_val
            cur_cnt = 1
        elif cur_date != norm_date:
            new_obj = {
                'date': cur_date,
                'max_value': cur_max_val,
                'min_value': cur_min_val,
                'avg_value': round(cur_total/cur_cnt, 2)
            }
            ret_obj[cur_date] = new_obj
            ret_list.append(new_obj)
            cur_date = norm_date
            cur_max_val = norm_val
            cur_min_val = norm_val
            cur_total = norm_val
            cur_cnt = 1
        else:
            if norm_val > cur_max_val:
                cur_max_val = norm_val
            if norm_val < cur_min_val:
                cur_min_val = norm_val
            cur_total += norm_val
            cur_cnt += 1

    if not ret_list.__contains__(cur_date):
        new_obj = {
            'date': cur_date,
            'max_value': cur_max_val,
            'min_value': cur_min_val,
            'avg_value': round(cur_total/cur_cnt, 2)
        }
        ret_obj[cur_date] = new_obj
        ret_list.append(new_obj)

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
            _date = date_hour.get("date")
            hour = date_hour.get("hour")

            new_val = {
                'date': _date,
                'hour': hour,
                'value': value
            }
            norm_time_val_obj[_date + "_" + str(hour)] = new_val
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
        try:
            grid = self.get_weather_grid(lat, long)
            cwa = grid.get("properties").get("cwa")
            grid_x = grid.get("properties").get("gridX")
            grid_y = grid.get("properties").get("gridY")
            forecast_zone = str(grid.get("properties").get("forecastZone"))
            zone_id = forecast_zone.split("/")[-1]
            print("latitude({0}), longitude({1}), cwa({2}), gridx({3}), gridy({4}), zoneID({5})"
                  .format(lat, long, str(cwa), str(grid_x), str(grid_y), str(zone_id)))

            weather_url = self.base_url + "gridpoints/" + str(cwa) + "/" + str(grid_x) + "," + str(grid_y)
            weather_forecast = requests.get(weather_url, headers=self.request_header)
            alerts_url = self.base_url + "alerts/active/zone/" + str(zone_id)
            alerts = requests.get(alerts_url, headers=self.request_header)
            return {
                "weather_forecast": weather_forecast.text,
                "alerts": alerts.text
            }
        except:
            return None

    def get_weather_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_by_lat_long(location.latitude, location.longitude)

    def get_weather_forecast_by_lat_long(self, lat, long):
        weather = self.get_weather_by_lat_long(lat, long)
        if weather is None:
            return None

        def get_hourly_forecast(weather_json_str, start_hour):
            weather_props = json.loads(weather_json_str)["properties"]
            hourly_temps = normalize_time_and_values(weather_props["temperature"], True)
            precipitation_probabilities = normalize_time_and_values(weather_props["probabilityOfPrecipitation"], False)
            wind_speeds = normalize_time_and_values(weather_props["windSpeed"], False)

            hourly_forecast = []
            count = 0
            for temp in hourly_temps:
                _date = temp.get("date")
                hour = temp.get("hour")

                # Condition used to start the hourly forecast from the current hour
                if count != 0 or start_hour == hour:
                    precipitation_probability = precipitation_probabilities[_date + "_" + str(hour)]
                    wind_speed = wind_speeds[_date + "_" + str(hour)]
                    standard_time = datetime.strptime(str(hour) + ':00', '%H:%M').strftime('%I:%M %p')

                    hourly_forecast.append({
                        'date': _date,
                        'hour': hour,
                        'standard_time': standard_time,
                        'temperature': convert_c_to_f(temp.get("value"), 0),
                        'precipitation_probability': precipitation_probability.get("value"),
                        'wind_speed': convert_kts_to_mph(wind_speed.get("value"), 0)
                    })
                    count += 1
                    if count == 24:
                        break
            return hourly_forecast

        def get_daily_forecast(weather_json_str):
            weather_props = json.loads(weather_json_str)["properties"]
            max_temps = get_max_min_temp_values(weather_props["maxTemperature"], True)
            min_temps = get_max_min_temp_values(weather_props["minTemperature"], False)
            precip_prob_vals = get_daily_values(weather_props["probabilityOfPrecipitation"], False)
            wind_speed_vals = get_daily_values(weather_props["windSpeed"], False)

            hourly_forecast = []

            for temp in max_temps:
                d = temp.get("date")
                max_temp = temp.get("value")
                min_temp = min_temps.get(d, {}).get("value", None)
                max_precip_prob = precip_prob_vals.get(d).get("max_value", None)
                min_precip_prob = precip_prob_vals.get(d).get("min_value", None)
                avg_precip_prob = precip_prob_vals.get(d).get("avg_value", None)
                max_wind = wind_speed_vals.get(d).get("max_value", None)
                min_wind = wind_speed_vals.get(d).get("min_value", None)

                day = datetime.strptime(d, "%Y-%m-%d").strftime('%A')
                if date.today().strftime("%Y-%m-%d") == d:
                    day = "Today"

                if min_temp:
                    hourly_forecast.append({
                        'date': d,
                        'day': day,
                        'max_temperature': convert_c_to_f(max_temp, 0),
                        'min_temperature': convert_c_to_f(min_temp, 0),
                        'max_precipitation_probability': max_precip_prob,
                        'min_precipitation_probability': min_precip_prob,
                        'avg_precipitation_probability': avg_precip_prob,
                        'max_wind_speed': convert_kts_to_mph(max_wind, 0),
                        'min_wind_speed': convert_kts_to_mph(min_wind, 0)
                    })

            return hourly_forecast

        def get_alerts(alerts_json_str):
            # print("alerts: " + alerts_json_str)
            alerts = []
            alerts_features = json.loads(alerts_json_str)["features"]
            for alerts_feature in alerts_features:
                alert_props = alerts_feature["properties"]
                alerts.append({
                    'event': alert_props["event"],
                    'headline': alert_props["headline"],
                    'severity': alert_props["severity"],
                    'description': alert_props["description"]
                })
            return alerts

        try:
            cur_hour = datetime.now().hour
            hourly = get_hourly_forecast(weather["weather_forecast"], cur_hour)
            cur_hour_forecast = hourly[0]
            for _hour in hourly:
                if _hour['hour'] == cur_hour:
                    cur_hour_forecast = _hour

            weather_image = ''
            if cur_hour > 18:
                weather_image = 'night'
            elif cur_hour_forecast['precipitation_probability'] > 50:
                weather_image = 'rain'
            else:
                weather_image = 'sun'

            weather_forecast = {
                'hourly_forecast': hourly,
                'daily_forecast': get_daily_forecast(weather["weather_forecast"]),
                'current_temp': cur_hour_forecast['temperature'],
                'current_wind_speed': cur_hour_forecast['wind_speed'],
                'current_precipitation_probability': cur_hour_forecast['precipitation_probability'],
                'weather_image': weather_image,
                'alerts': get_alerts(weather["alerts"])
            }
            return weather_forecast
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return None

    def get_weather_forecast_by_location_str(self, location_str):
        location = self.get_location(location_str)
        return self.get_weather_forecast_by_lat_long(location.latitude, location.longitude)


# weather_utils = WeatherUtil()
# weather_utils.get_weather_grid()
# weather_utils.get_location("raliegh, nc")
# print(weather_utils.get_weather_forecast_by_location_str("Warsaw"))
# print(weather_utils.get_weather_forecast_by_lat_long(35.7803977, -78.6390989))
