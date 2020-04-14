from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .models import Activity


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
    # precipitation_chance_max = forms.IntegerField(widget=forms.IntegerField(attrs={'class': 'form-control'}))

    class Meta:
        model = Activity
        fields = (
            'name',
            'description',
            'min_temp',
            'max_temp',
        )
