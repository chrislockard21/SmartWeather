from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth import login, authenticate, logout

from .models import Activity
from .weather_util import WeatherUtil, current_location
from .forms import RegisterForm, AddActivityForm
from django.contrib.auth.decorators import login_required

import json


# Create your views here.

def index(request):
    print('index: ' + str(request))
    print('User:  ' + str(request.user))
    template_name = 'weather/index.html'

    weather_utils = WeatherUtil()
    if not request.user.is_anonymous:
        activities = Activity.objects.filter(user__in=[request.user, 0])
    else:
        activities = Activity.objects.filter(user=0)

    activity_form = AddActivityForm()

    loc_text = request.GET.get('loc_text')
    if not loc_text:
        location = current_location()
        lat = location['latitude']
        long = location['longitude']
        location_name = "{city}, {state}".format(city=location['city'], state=location['region_name'])
    else:
        location = weather_utils.get_location(loc_text)
        lat = location.latitude
        long = location.longitude
        location_name = location.address

    weather_forecast = weather_utils.get_weather_forecast_by_lat_long(lat, long)

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
            'map_src': map_src,
            'activity_form': activity_form
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


# local_activities = Activity.objects.values()
# local_activities_list = list(local_activities)
# print("Activities -> " + str(local_activities_list))
# local_context = {
#     'activities': local_activities_list
# }
# print("Context -> " + str(local_context))
