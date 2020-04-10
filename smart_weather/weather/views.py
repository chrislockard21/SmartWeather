from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.auth import login, authenticate, logout

from .models import Activity
from .weather_util import WeatherUtil
from .forms import RegisterForm, AddActivityForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    print('index')
    template_name = 'weather/index.html'
    weather_utils = WeatherUtil()
    activities = Activity.objects.values()
    activities_list = list(activities.values())
    print("Activities: " + str(activities_list))
    context = {
        'weather': weather_utils.get_weather_forecast_by_location_str("Raleigh"),
        'activities': activities_list
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


def add_activity(request):
    template_name = 'weather/add_activity.html'

    if request.method == 'POST':
        print("activity::POST")
        form = AddActivityForm(request.POST)
        if form.is_valid():
            # Holds off on writing to the database
            activity = form.save(commit=False)

            # Gets the cleaned form data
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']

            activity.name = name
            activity.description = description
            activity.save()
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
