# Generated by Django 2.2.10 on 2020-04-17 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('business_name', models.CharField(max_length=500)),
                ('min_temp', models.IntegerField(default=70)),
                ('max_temp', models.IntegerField(default=90)),
                ('min_wind', models.IntegerField(default=0)),
                ('max_wind', models.IntegerField(default=20)),
                ('min_precipitation_chance', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('max_precipitation_chance', models.DecimalField(decimal_places=1, default=100, max_digits=4)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlantCare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('min_temp', models.IntegerField(default=70)),
                ('max_temp', models.IntegerField(default=90)),
                ('min_wind', models.IntegerField(default=0)),
                ('max_wind', models.IntegerField(default=20)),
                ('min_precipitation_chance', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('max_precipitation_chance', models.DecimalField(decimal_places=1, default=50, max_digits=4)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Clothing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('min_temp', models.IntegerField(default=70)),
                ('max_temp', models.IntegerField(default=90)),
                ('min_wind', models.IntegerField(default=0)),
                ('max_wind', models.IntegerField(default=20)),
                ('min_precipitation_chance', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('max_precipitation_chance', models.DecimalField(decimal_places=1, default=50, max_digits=4)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('min_temp', models.IntegerField(default=70)),
                ('max_temp', models.IntegerField(default=90)),
                ('min_wind', models.IntegerField(default=0)),
                ('max_wind', models.IntegerField(default=20)),
                ('min_precipitation_chance', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('max_precipitation_chance', models.DecimalField(decimal_places=1, default=50, max_digits=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
