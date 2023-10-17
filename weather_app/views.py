from django.shortcuts import render

# Create your views here.
import datetime
import calendar
import requests
from datetime import datetime
from django.shortcuts import render

# https://www.weatherbit.io/api/swaggerui/weather-api-v2#/Current32Weather32Data
# Create your views here.

def index(request):
    API_KEY = open("C:\\Users\\44791\DjangoProjects\\weather_project\\weather_app\\API_KEY", "r").read()
    current_weather_url = "https://api.weatherbit.io/v2.0/current?city={}&country={}&key={}"
    forecast_url = "https://api.weatherbit.io/v2.0/forecast/daily?lat={}&lon={}&days=5&key={}"

    if request.method == "POST":
        city = request.POST['city']
        country_code = request.POST['country_code']
        weather_data, daily_forecasts = fetch_weather_and_forecast(city, country_code, API_KEY, current_weather_url, forecast_url)
        
        context = {
            "weather_data": weather_data,
            "daily_forecasts": daily_forecasts,
        }

        return render(request, "weather_app/index.html", context)

    else:
        return render(request, "weather_app/index.html")
    

# send requests to the URL, and capturing the responses
def fetch_weather_and_forecast(city, country_code, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, country_code, api_key)).json()
    lat, lon = response['data'][0]['lat'], response['data'][0]['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        "city": city,
        "temperature": response['data'][0]['temp'],
        "description": response['data'][0]['weather']['description'],
        "icon": response['data'][0]['weather']['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['data']:
        daily_forecasts.append({
            "day": calendar.day_name[datetime.strptime(daily_data['datetime'], '%Y-%m-%d').weekday()],
            "min_temp": daily_data['min_temp'],
            "max_temp": daily_data['max_temp'],
            "description": daily_data['weather']['description'],
            "icon": daily_data['weather']['icon'],
        })
    

    return weather_data, daily_forecasts

