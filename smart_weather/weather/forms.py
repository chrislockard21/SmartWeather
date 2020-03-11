from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class RegisterForm(UserCreationForm):
    '''
    Creates the registration form, allowing users to register for the site.
    This class also renders a duplciate password field for password validation
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), validators=[MinLengthValidator(10)])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), validators=[MinLengthValidator(10)])

    class Meta:
        '''Connects to the built in User class and grabs it's fields'''
        model = User
        fields = (
            'username',
            'password1',
            'password2'
        )
