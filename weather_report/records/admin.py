from django.contrib import admin
from .models import WeatherAlert, WeatherData

admin.site.register(WeatherData),
admin.site.register(WeatherAlert)
