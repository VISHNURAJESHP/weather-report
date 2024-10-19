import time
import threading
from django.core.management.base import BaseCommand
from records.views import fetch_weather_data_task  

class Command(BaseCommand):
    help = 'Run a scheduler to fetch weather data every 5 minutes'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting the weather data scheduler...')
        
        
        scheduler_thread = threading.Thread(target=self.run_scheduler)
        scheduler_thread.daemon = True 
        scheduler_thread.start()
        
        
        while True:
            time.sleep(60)

    def run_scheduler(self):
        """Runs the task every 5 minutes"""
        while True:
            self.stdout.write('Fetching weather data...')
            fetch_weather_data_task()
            self.stdout.write('Weather data fetch complete.')

            time.sleep(300)
