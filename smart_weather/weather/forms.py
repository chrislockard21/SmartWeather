from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .models import Activity, PlantCare


class RegisterForm(UserCreationForm):
    '''
    Creates the registration form, allowing users to register for the site.
    This class also renders a duplciate password field for password validation
    '''
    # Defines the widgets that will be used in the UI for the form field.
    # This is not required but is routinely used to add css classes and
    # validators to fields
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[MinLengthValidator(10)])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                validators=[MinLengthValidator(10)])

    class Meta:
        '''Connects to the built in User class and grabs it's fields'''
        model = User
        fields = (
            'username',
            'password1',
            'password2'
        )


class AddActivityForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    min_temp = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_temp = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_wind = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_wind = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_precipitation_chance = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_precipitation_chance = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Activity
        fields = (
            'name',
            'description',
            'min_temp',
            'max_temp',
            'min_wind',
            'max_wind',
            'min_precipitation_chance',
            'max_precipitation_chance'
        )


class AddPlantCareForm(forms.ModelForm):
    name = forms.CharField(label="Name:",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    action = forms.CharField(label="Action to Take:",
                             widget=forms.Textarea(attrs={'class': 'form-control'}))
    temp_condition = forms.CharField(label="Temperature Condition:",
                                     widget=forms.Select(choices=PlantCare.CONDITION_CHOICES,
                                                         attrs={'class': 'form-control'}))
    temp_value = forms.IntegerField(label="Temperature Value:",
                                    required=False,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    wind_condition = forms.CharField(label="Wind Condition:",
                                     widget=forms.Select(choices=PlantCare.CONDITION_CHOICES,
                                                         attrs={'class': 'form-control'}))
    wind_value = forms.IntegerField(label="Wind Value:",
                                    required=False,
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    precipitation_chance_condition = forms.CharField(label="Precipitation Chance Condition:",
                                                     widget=forms.Select(choices=PlantCare.CONDITION_CHOICES,
                                                                         attrs={'class': 'form-control'}))
    precipitation_chance_value = forms.IntegerField(label="Precipitation Chance Value:",
                                                    required=False,
                                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PlantCare
        fields = (
            'name',
            'action',
            'temp_value',
            'temp_condition',
            'wind_value',
            'wind_condition',
            'precipitation_chance_value',
            'precipitation_chance_condition'
        )
