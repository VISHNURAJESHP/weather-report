import requests
from collections import Counter
from django.http import JsonResponse
from django.utils.timezone import now
from django.db.models import Max
from .models import WeatherData, WeatherAlert

API_KEY = "3fc5b3748eb7f2a9b55ce7d396cae714"  # Replace with your actual API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

THRESHOLD_TEMP = 35

def fetch_weather_data_task():
    today = now().date()
    current_time = now().time()  # Get the current time

    for city in CITIES:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            condition = data['weather'][0]['main']

            # Store the weather data with current time
            WeatherData.objects.create(
                city=city,
                date=today,
                time=current_time,
                avg_temp=temperature,
                max_temp=temperature,
                min_temp=temperature,
                dominant_condition=condition
            )

            # Check for alerts based on the current temperature
            check_alerts(city)

        else:
            print(f"Error fetching data for {city}: {response.json().get('message', 'Unknown error')}")

    # Update dominant condition for each city after processing
    for city in CITIES:
        dominant_condition = determine_dominant_condition(city, today)
        WeatherData.objects.filter(city=city, date=today).update(dominant_condition=dominant_condition)

def determine_dominant_condition(city, date):
    conditions = WeatherData.objects.filter(city=city, date=date).values_list('dominant_condition', flat=True)
    if conditions:
        return Counter(conditions).most_common(1)[0][0]
    return None

def check_alerts(city):
    last_two_temps = WeatherData.objects.filter(city=city).order_by('-date', '-time')[:2]  # Get the last two records
    if len(last_two_temps) == 2:
        avg_temp_1 = last_two_temps[0].avg_temp
        avg_temp_2 = last_two_temps[1].avg_temp
        if avg_temp_1 > THRESHOLD_TEMP and avg_temp_2 > THRESHOLD_TEMP:
            # Trigger alert if both last two updates exceed the threshold
            WeatherAlert.objects.create(
                city=city, 
                alert_message=f"Temperature exceeded {THRESHOLD_TEMP}°C for two consecutive updates."
            )

def convert_temperature(temp_celsius, preference='Celsius'):
    if preference == 'Celsius':
        return temp_celsius  # Already in Celsius
    elif preference == 'Fahrenheit':
        return (temp_celsius * 9/5) + 32  
    return temp_celsius  

def process_weather_data(request):
    fetch_weather_data_task()
    return JsonResponse({'status': 'Weather update task triggered'})

# API Endpoint to return weather summaries for all cities
def get_weather_summary(request):
    user_preference = request.GET.get('temperature_preference', 'Celsius')  # Get user preference
    today = now().date()
    weather_summaries = []
    
    # Retrieve only today's weather data
    weather_records = WeatherData.objects.filter(date=today)  

    # Group the weather records by city to get the latest record
    for city in CITIES:
        latest_record = weather_records.filter(city=city).order_by('-time').first()  # Get the latest record
        if latest_record:
            # Convert temperature based on user preference
            avg_temp_converted = convert_temperature(latest_record.avg_temp, user_preference)
            max_temp_converted = convert_temperature(latest_record.max_temp, user_preference)
            min_temp_converted = convert_temperature(latest_record.min_temp, user_preference)

            weather_summaries.append({
                'city': latest_record.city,
                'date': latest_record.date,
                'avg_temp': avg_temp_converted,
                'max_temp': max_temp_converted,
                'min_temp': min_temp_converted,
                'dominant_condition': latest_record.dominant_condition
            })

    return JsonResponse({'weather_data': weather_summaries})

# API Endpoint to return all weather alerts
def get_alerts(request):
    # Get the latest alert for each city
    latest_alerts = WeatherAlert.objects.values('city').annotate(latest_triggered_at=Max('triggered_at'))

    # Prepare the response data with the latest alerts
    alert_data = []
    for alert in latest_alerts:
        # Fetch the alert using the city and the latest triggered time
        latest_alert = WeatherAlert.objects.filter(city=alert['city'], triggered_at=alert['latest_triggered_at']).first()
        if latest_alert:
            alert_data.append({
                'city': latest_alert.city,
                'alert_message': latest_alert.alert_message,
                'triggered_at': latest_alert.triggered_at,
            })

    return JsonResponse({'alerts': alert_data})
