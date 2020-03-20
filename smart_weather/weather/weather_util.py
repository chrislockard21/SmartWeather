import requests
from geopy.geocoders import Nominatim

class weather_util():
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
        print("Grid request URL: " + str(req_url))
        grid = requests.get(req_url, headers=self.request_header)
        return grid.json()

    def get_location(self, locaction_str):
        geo_locator = Nominatim(user_agent="smartweatherapp")
        location = geo_locator.geocode(locaction_str)
        print(str(location.raw))
        print("latitude: " + str(location.latitude))
        print("longitude: " + str(location.longitude))
        return location

    def get_current_weather(self, location_str):
        location = self.get_location(location_str)
        print("location: " + str(location.raw))
        grid = self.get_weather_grid(location.latitude, location.longitude)
        print("grid: " + str(grid))
        cwa = grid.get("properties").get("cwa")
        grid_x = grid.get("properties").get("gridX")
        grid_y = grid.get("properties").get("gridY")

        url = self.base_url + "gridpoints/" + str(cwa) + "/" + str(grid_x) + "," + str(grid_y)
        res = requests.get(url, headers=self.request_header)
        data = res.json()
        print("weather forecast: " + str(data))


weatherUtil = weather_util()
# weatherUtil.get_weather_grid()
# weatherUtil.get_location("raliegh, nc")
weatherUtil.get_current_weather("raliegh, nc")
