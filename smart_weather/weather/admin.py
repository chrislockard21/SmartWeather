from django.contrib import admin
from . import models

# Register your models here. Below is an example of how you can register a model
# admin.site.register(models.Foo)

admin.site.register(models.Activity)
admin.site.register(models.Clothing)
admin.site.register(models.PlantCare)
admin.site.register(models.Promotions)
