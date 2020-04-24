from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

from .models import Activity, Clothing, PlantCare
from .weather_util import WeatherUtil, current_location
from .forms import RegisterForm, AddActivityForm, AddPlantCareForm
from django.contrib.auth.decorators import login_required

import json


# Create your views here.

def get_activities(forecast, user):
    # activities = Activity.objects.filter(user__in=[request.user, 0],
    #                                      min_temp__gte=forecast['min_temperature'],
    #                                      max_temp__lte=forecast['max_temperature'],
    #                                      min_wind__gte=forecast['min_wind_speed'],
    #                                      max_wind__lte=forecast['max_wind_speed'],
    #                                      min_precipitation_chance__gte=forecast['min_precipitation_probability'],
    #                                      max_precipitation_chance__lte=forecast['max_precipitation_probability']
    #                                      ).values().order_by('name')
    ret_activities = []
    print("forecast: " + str(forecast))
    activities = Activity.objects.filter(user__in=[user, 0])
    for activity in activities:
        if((activity.min_wind is None or activity.min_wind <= forecast['min_wind_speed']) and
                (activity.max_wind is None or activity.max_wind >= forecast['max_wind_speed']) and
                (activity.min_temp is None or activity.min_temp <= forecast['min_temperature']) and
                (activity.max_temp is None or activity.max_temp >= forecast['max_temperature']) and
                (activity.min_precipitation_chance is None or activity.min_precipitation_chance <= forecast['avg_precipitation_probability']) and
                (activity.max_precipitation_chance is None or activity.max_precipitation_chance >= forecast['avg_precipitation_probability'])):
            ret_activities.append(activity)

    return ret_activities


def get_clothing(forecast):
    # clothing = Clothing.objects.raw('SELECT * ' +
    #                                 'FROM weather_clothing ' +
    #                                 'WHERE (temp_value IS NULL OR ' +
    #                                 '(( temp_value IS NOT NULL AND temp_condition = "GT" AND temp_value <= %s ) OR ' +
    #                                 '( temp_value IS NOT NULL AND temp_condition = "LT" AND temp_value >= %s ))) ' +
    #
    #                                 'AND (wind_value IS NULL OR ' +
    #                                 '(( wind_value IS NOT NULL AND wind_condition = "GT" AND wind_value <= %s ) OR ' +
    #                                 '( wind_value IS NOT NULL AND wind_condition = "LT" AND wind_value >= %s )))' +
    #
    #                                 'AND (precipitation_chance_value IS NULL OR ' +
    #                                 '(( precipitation_chance_value IS NOT NULL AND precipitation_chance_condition = "GT" AND precipitation_chance_value <= %s ) OR ' +
    #                                 '( precipitation_chance_value IS NOT NULL AND precipitation_chance_condition = "LT" AND precipitation_chance_value >= %s ))) ' +
    #                                 'ORDER BY name',
    #                                 [weather_forecast['current_temp'], weather_forecast['current_temp'],
    #                                  weather_forecast['current_wind_speed'], weather_forecast['current_wind_speed'],
    #                                  weather_forecast['current_precipitation_probability'],
    #                                  weather_forecast['current_precipitation_probability']])
    ret_clothing = []
    clothing_opts = Clothing.objects.all()
    print(str(clothing_opts))
    for clothing_opt in clothing_opts:
        should_add = False
        if clothing_opt.temp_value is not None:
            if clothing_opt.temp_condition == "GT":
                if forecast['max_temperature'] >= clothing_opt.temp_value:
                    should_add = True
            else:
                if forecast['min_temperature'] <= clothing_opt.temp_value:
                    should_add = True
        if clothing_opt.wind_value is not None:
            if clothing_opt.wind_condition == "GT":
                if forecast['max_wind_speed'] >= clothing_opt.wind_value:
                    should_add = True
            else:
                if forecast['min_wind_speed'] <= clothing_opt.wind_value:
                    should_add = True
        if clothing_opt.precipitation_chance_value is not None:
            if clothing_opt.precipitation_chance_condition == "GT":
                if forecast['max_precipitation_probability'] >= clothing_opt.precipitation_chance_value:
                    should_add = True
            else:
                if forecast['avg_precipitation_probability'] <= clothing_opt.precipitation_chance_value:
                    should_add = True
        if should_add:
            ret_clothing.append(clothing_opt)
    return ret_clothing


def get_plant_care(forecast, user):
        # plants = PlantCare.objects.raw('SELECT * ' +
        #                                 'FROM weather_plantcare ' +
        #                                 'WHERE (temp_value IS NULL OR ' +
        #                                 '(( temp_value IS NOT NULL AND temp_condition = "GT" AND temp_value <= %s ) OR ' +
        #                                 '( temp_value IS NOT NULL AND temp_condition = "LT" AND temp_value >= %s ))) ' +
        #
        #                                 'AND (wind_value IS NULL OR ' +
        #                                 '(( wind_value IS NOT NULL AND wind_condition = "GT" AND wind_value <= %s ) OR ' +
        #                                 '( wind_value IS NOT NULL AND wind_condition = "LT" AND wind_value >= %s )))' +
        #
        #                                 'AND (precipitation_chance_value IS NULL OR ' +
        #                                 '(( precipitation_chance_value IS NOT NULL AND precipitation_chance_condition = "GT" AND precipitation_chance_value <= %s ) OR ' +
        #                                 '( precipitation_chance_value IS NOT NULL AND precipitation_chance_condition = "LT" AND precipitation_chance_value >= %s ))) ' +
        #                               #  'AND user = %s ' +       #this would have the user filter
        #                                 'ORDER BY name',
        #                                 [weather_forecast['current_temp'], weather_forecast['current_temp'],
        #                                  weather_forecast['current_wind_speed'], weather_forecast['current_wind_speed'],
        #                                  weather_forecast['current_precipitation_probability'], weather_forecast['current_precipitation_probability']])
        #                               #  str(request.user)])   #this would have the user parameter
    ret_plants = []
    plants = PlantCare.objects.filter(user__in=[user, 0])
    for plant in plants:
        should_add = False
        if plant.temp_value is not None:
            if plant.temp_condition == "GT":
                if forecast['max_temperature'] >= plant.temp_value:
                    should_add = True
            else:
                if forecast['min_temperature'] <= plant.temp_value:
                    should_add = True
        if plant.wind_value is not None:
            if plant.wind_condition == "GT":
                if forecast['max_wind_speed'] >= plant.wind_value:
                    should_add = True
            else:
                if forecast['min_wind_speed'] <= plant.wind_value:
                    should_add = True
        if plant.precipitation_chance_value is not None:
            if plant.precipitation_chance_condition == "GT":
                if forecast['max_precipitation_probability'] >= plant.precipitation_chance_value:
                    should_add = True
            else:
                if forecast['avg_precipitation_probability'] <= plant.precipitation_chance_value:
                    should_add = True
        if should_add:
            ret_plants.append(plant)

    return ret_plants


def index(request):
    print('index: ' + str(request))
    print('User:  ' + str(request.user))
    template_name = 'weather/index.html'

    weather_utils = WeatherUtil()

    loc_text = request.GET.get('loc_text')
    if not loc_text:
        # Find current location
        location = current_location()
        lat = location['latitude']
        long = location['longitude']
        location_name = "{city}, {state}".format(city=location['city'], state=location['region_name'])
    else:
        if len(loc_text) == 5 and loc_text.isdigit():
            loc_text = loc_text + " US"  # force US zip code lookup
        # Search for location based on text
        location = weather_utils.get_location(loc_text)
        if location is None:
            context = {
                'location_name': "Forecast Unavailable for Location"
            }
            return render(request, template_name, context)
        lat = location.latitude
        long = location.longitude
        location_name = location.address

    weather_forecast = weather_utils.get_weather_forecast_by_lat_long(lat, long)

    if weather_forecast is None:
        context = {
            'location_name': "Forecast Unavailable for {loc}".format(loc=location_name)
        }
        return render(request, template_name, context)

    forecast = weather_forecast['daily_forecast'][0]

    if not request.user.is_anonymous:
        activities = get_activities(forecast, request.user)
        clothing = get_clothing(forecast)
        plants = get_plant_care(forecast, request.user)
    else:
        activities = Activity.objects.filter(user=0)
        clothing = Clothing.objects.filter()
        plants = PlantCare.objects.filter(user=0)

    if weather_forecast:
        print("{name}: {lat}, {long}".format(name=location_name, lat=lat, long=long))

        map_src = "//cobra.maps.arcgis.com/apps/Embed/index.html?webmap=c4fcd13aa52e4dcfb24cc6e90a970a59&" \
                  "zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light&" \
                  "marker={longitude},{latitude}&center={longitude},{latitude}&level=10"\
            .format(longitude=long, latitude=lat)

        context = {
            'location_name': location_name,
            'weather': weather_forecast,
            'activities': activities,
            'clothing': clothing,
            'plants': plants,
            'map_src': map_src,
            'activity_form': AddActivityForm(),
            'plant_care_form': AddPlantCareForm()
        }
    else:
        context = {
            'location_name': "Forecast Unavailable for Location"
        }

    return render(request, template_name, context)


def register(request):
    template_name = 'weather/register.html'

    if request.method == 'POST':
        print("register::POST")
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Holds off on writing to the database
            user = form.save(commit=False)

            # Gets the cleaned form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Gets and sets the users password
            if password == form.cleaned_data['password2']:
                user.set_password(password)
                user.save()

                # Authenticates the user for initial login
                user = authenticate(username=username, password=password)
                if user is not None:
                    # Logs in the user
                    if user.is_active:
                        login(request, user)
                        return redirect('weather:index')
    else:
        print("register::GET")
        form = RegisterForm(None)

    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def add_activity(request):
    template_name = 'weather/add_activity.html'

    if request.method == 'POST':
        print("activity::POST")
        form = AddActivityForm(request.POST)
        if form.is_valid():
            # Holds off on writing to the database
            activity = form.save(commit=False)

            # Sets the user for the activity
            activity.user = request.user
            activity.save()

            # Redirects the user to the index
            return redirect('weather:index')
    else:
        print("activity::GET")
        form = AddActivityForm(None)

    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def add_plant_care(request):
    template_name = 'weather/add_plant_care.html'

    if request.method == 'POST':
        print("activity::POST")
        form = AddPlantCareForm(request.POST)
        if form.is_valid():
            # Holds off on writing to the database
            plant_care = form.save(commit=False)

            # Sets the user for the activity
            plant_care.user = request.user
            plant_care.save()

            # Redirects the user to the index
            return redirect('weather:index')
    else:
        print("activity::GET")
        form = AddPlantCareForm(None)

    context = {
        'form': form
    }
    return render(request, template_name, context)


# local_activities = Activity.objects.values()
# local_activities_list = list(local_activities)
# print("Activities -> " + str(local_activities_list))
# local_context = {
#     'activities': local_activities_list
# }
# print("Context -> " + str(local_context))
