<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>README - Weather App</title>
</head>
<body>

<h1>Weather Monitoring Django Application</h1>

<p>This Django project allows you to monitor weather conditions for different cities using the OpenWeatherMap API. It includes a background scheduler to fetch weather data periodically and API endpoints for fetching weather summaries and alerts.</p>

<h2>Features</h2>
<ul>
    <li>Fetches weather data for multiple cities at regular intervals (every 5 minutes).</li>
    <li>Stores temperature, weather conditions, and generates alerts if temperatures exceed a threshold.</li>
    <li>Provides API endpoints for retrieving weather summaries and alerts.</li>
</ul>

<h2>Project Setup</h2>
<ol>
    <li>Clone the repository: <code>git clone https://github.com/VISHNURAJESHP/weather-report.git</code></li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Run database migrations: <code>python manage.py migrate</code></li>
    <li>Set up your OpenWeatherMap API key by replacing the value of <code>API_KEY</code> in <code>views.py</code>.</li>
    <li>Start the Django development server: <code>python manage.py runserver</code> <strong>(Run the backend first)</strong></li>
</ol>

<h2>Running the Project</h2>
<p>Here are the commands to run the backend, scheduler, and frontend:</p>

<ul>
    <li><strong>Run Backend (Django):</strong> <code>python manage.py runserver</code> (This should run first)</li>
    <li><strong>Run Scheduler:</strong> <code>python manage.py weather_schedular</code></li>
    <li><strong>Run Frontend:</strong> 
        <ol>
            <li>Navigate to the <code>web</code> folder: <code>cd web</code></li>
            <li>Start the frontend server: <code>python -m http.server 8080</code></li>
            <li>Access the dashboard at: <code>http://localhost:8080/dashboard.html</code></li>
        </ol>
    </li>
</ul>

<h2>API Endpoints</h2>
<p>The following API endpoints are available:</p>

<ul>
    <li>
        <strong>Process Weather Data:</strong><br>
        <code>GET /api/process-weather-data/</code><br>
        This endpoint triggers an immediate weather data fetch and update task.
    </li>

    <li>
        <strong>Get Weather Summary:</strong><br>
        <code>GET /api/get-weather-summary/?temperature_preference=Celsius|Fahrenheit</code><br>
        This endpoint returns the latest weather summary for all cities, with temperature preferences as either Celsius or Fahrenheit.
    </li>

    <li>
        <strong>Get Alerts:</strong><br>
        <code>GET /api/get-alerts/</code><br>
        This endpoint returns the latest weather alerts for each city where temperature exceeds the threshold (35°C).
    </li>
</ul>

<h2>Screenshots</h2>
<p>Below are some screenshots of the project in action:</p>

<h3>1. Weather Summary Page</h3>
<img src="weather_report/images/Screenshot (123).png" alt="Weather Summary Screenshot" width="600">

<h3>2. Alerts Page</h3>
<img src="weather_report/images/Screenshot (124).png" alt="Weather Alerts Screenshot" width="600">

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>

</body>
</html>
