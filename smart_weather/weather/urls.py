from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('add_activity', views.add_activity, name='add_activity'),
    
    # Build in URL's to handle login and logout. The login form and login
    # template are editible in the login template
    path('login', LoginView.as_view(template_name='weather/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
