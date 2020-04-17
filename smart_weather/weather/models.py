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
    min_precipitation_chance = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    max_precipitation_chance = models.DecimalField(default=50, decimal_places=1, max_digits=4)

    #for future recommendations
    #sunny = models.BooleanField(default=True)
    #lightning = models.BooleanField(default=False)
    #air_quality_index = models.IntegerField(default=50) #0-50 is healthy

    def __str__(self):
        return self.name


class PlantCare(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    min_temp = models.IntegerField(default=70)
    max_temp = models.IntegerField(default=90)
    min_wind = models.IntegerField(default=0)
    max_wind = models.IntegerField(default=20)
    min_precipitation_chance = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    max_precipitation_chance = models.DecimalField(default=50, decimal_places=1, max_digits=4)

    #for future recommendations
    #sunny = models.BooleanField(default=True)
    #lightning = models.BooleanField(default=False)
    #air_quality_index = models.IntegerField(default=50) #0-50 is healthy

    def __str__(self):
        return self.name


class Clothing(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    min_temp = models.IntegerField(default=70)
    max_temp = models.IntegerField(default=90)
    min_wind = models.IntegerField(default=0)
    max_wind = models.IntegerField(default=20)
    min_precipitation_chance = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    max_precipitation_chance = models.DecimalField(default=50, decimal_places=1, max_digits=4)

    #for future recommendations
    #sunny = models.BooleanField(default=True)
    #lightning = models.BooleanField(default=False)
    #air_quality_index = models.IntegerField(default=50) #0-50 is healthy

    def __str__(self):
        return self.name


class Promotions(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    business_name = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    min_temp = models.IntegerField(default=70)
    max_temp = models.IntegerField(default=90)
    min_wind = models.IntegerField(default=0)
    max_wind = models.IntegerField(default=20)
    min_precipitation_chance = models.DecimalField(default=0, decimal_places=1, max_digits=4)
    max_precipitation_chance = models.DecimalField(default=100, decimal_places=1, max_digits=4)

    #for future recommendations
    #sunny = models.BooleanField(default=True)
    #lightning = models.BooleanField(default=False)
    #air_quality_index = models.IntegerField(default=50) #0-50 is healthy

    def __str__(self):
        return self.name
