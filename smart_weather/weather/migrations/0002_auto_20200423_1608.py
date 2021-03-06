# Generated by Django 2.2.10 on 2020-04-23 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='max_precipitation_chance',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='max_temp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='max_wind',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='min_precipitation_chance',
            field=models.DecimalField(blank=True, decimal_places=1, default=None, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='min_temp',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='min_wind',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
