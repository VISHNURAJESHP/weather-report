from django.db import models
from django.utils.timezone import now

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()  # Add time field to store specific update times
    avg_temp = models.FloatField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    dominant_condition = models.CharField(max_length=100)

    class Meta:
        unique_together = ('city', 'date', 'time') 

class WeatherAlert(models.Model):
    city = models.CharField(max_length=100)
    alert_message = models.TextField()
    triggered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.city} at {self.triggered_at}"
