from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    min_temp = models.IntegerField()
    max_temp = models.IntegerField()
    # precipitation_chance_max = models.IntegerField
