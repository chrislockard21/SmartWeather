from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_temp = models.IntegerField(default=70)
    max_temp = models.IntegerField(default=90)
    min_wind = models.IntegerField(default=0)
    max_wind = models.IntegerField(default=20)
    # precipitation_chance_max = models.IntegerField

    def __str__(self):
        return self.name
