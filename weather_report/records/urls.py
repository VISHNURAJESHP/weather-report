from django.urls import path
from . import views

urlpatterns = [
    path('api/process-weather-data/', views.process_weather_data, name='process_weather_data'),
    path('api/get-weather-summary/', views.get_weather_summary, name='get_weather_summary'),
    path('api/get-alerts/', views.get_alerts, name='get_alerts'),
]