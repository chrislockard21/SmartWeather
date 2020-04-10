from django.db import models

# Create your models here.


class Activity(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField
    # min_temp = models.IntegerField
    # max_temp = models.IntegerField
    # precipitation_chance_max = models.IntegerField


# Example model
# class Foo(models.Model):
#     # A foreignkey can be used to relate models, so the model Foo will have a
#     # one to many relationship with the user.
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bar = models.CharField(max_length=30)
