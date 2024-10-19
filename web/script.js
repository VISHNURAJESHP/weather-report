document.addEventListener('DOMContentLoaded', () => {
    const tempUnitSelector = document.getElementById('tempUnit');
    const weatherDataContainer = document.getElementById('weatherData');
    const alertsContainer = document.getElementById('alerts');
    const refreshButton = document.getElementById('refreshButton');

    tempUnitSelector.addEventListener('change', fetchWeatherData);
    refreshButton.addEventListener('click', fetchWeatherDataAndAlerts);
    
    // Call fetchWeatherDataAndAlerts on page load
    fetchWeatherDataAndAlerts();

    // Set interval to fetch weather data every 5 minutes
    setInterval(fetchWeatherData, 300000); 

    // Function to fetch weather data
    function fetchWeatherData() {
        const unit = tempUnitSelector.value;
        fetch(`http://127.0.0.1:8000/api/get-weather-summary/?temperature_preference=${unit}`)
            .then(response => response.json())
            .then(data => {
                weatherDataContainer.innerHTML = '';
                data.weather_data.forEach(cityData => {
                    const cityWeatherElement = document.createElement('div');
                    cityWeatherElement.classList.add('city-weather');

                    cityWeatherElement.innerHTML = `
                        <div>
                            <h3>${cityData.city}</h3>
                            <p><strong>Date:</strong> ${cityData.date}</p>
                            <p><strong>Avg Temp:</strong> ${cityData.avg_temp.toFixed(2)}°${unit}</p>
                            <p><strong>Max Temp:</strong> ${cityData.max_temp.toFixed(2)}°${unit}</p>
                            <p><strong>Min Temp:</strong> ${cityData.min_temp.toFixed(2)}°${unit}</p>
                        </div>
                        <div class="condition">
                            ${cityData.dominant_condition}
                        </div>
                    `;
                    weatherDataContainer.appendChild(cityWeatherElement);
                });
            })
            .catch(error => console.error('Error fetching weather data:', error));
    }

    // Function to fetch weather alerts
    function fetchWeatherAlerts() {
        fetch('http://127.0.0.1:8000/api/get-alerts/')
            .then(response => response.json())
            .then(data => {
                alertsContainer.innerHTML = '';
                data.alerts.forEach(alert => {
                    const alertElement = document.createElement('div');
                    alertElement.classList.add('alert');

                    alertElement.innerHTML = `
                        <p><strong>City:</strong> ${alert.city}</p>
                        <p><strong>Alert:</strong> ${alert.alert_message}</p>
                        <p><strong>Triggered At:</strong> ${new Date(alert.triggered_at).toLocaleString()}</p>
                    `;
                    alertsContainer.appendChild(alertElement);
                });
            })
            .catch(error => console.error('Error fetching weather alerts:', error));
    }

    // Function to fetch weather data and alerts
    function fetchWeatherDataAndAlerts() {
        refreshButton.disabled = true;  // Disable the refresh button here
        fetch('http://127.0.0.1:8000/api/process-weather-data/')
            .then(response => {
                if (response.ok) {
                    // If the fetch was successful, also fetch the latest weather data and alerts
                    fetchWeatherData();  // Fetch the latest weather summary
                    fetchWeatherAlerts(); // Fetch the latest alerts
                } else {
                    console.error('Error triggering weather data fetch:', response.statusText);
                }
            })
            .catch(error => console.error('Error fetching weather data:', error))
            .finally(() => {
                refreshButton.disabled = false; // Re-enable the button after fetching
            });
    }

    // Call fetchWeatherAlerts on page load
    fetchWeatherAlerts();

    // Set interval to fetch weather alerts every 5 minutes
    setInterval(fetchWeatherAlerts, 300000);
});
