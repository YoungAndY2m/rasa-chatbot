import requests
import os
from dotenv import load_dotenv

load_dotenv()


def Weather(city):

    WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')

    geocoding_api = 'http://api.openweathermap.org/geo/1.0/direct?q=' + \
        city + '&limit=1&appid=' + WEATHER_API_TOKEN
    json_data = requests.get(geocoding_api).json()

    # json_data[0] is the first data (limit = 1)
    lat = str(json_data[0]['lat'])
    lon = str(json_data[0]['lon'])
    print("Latitude is {0} Lontitude is {1}".format(lat, lon))

    current_api = 'https://api.openweathermap.org/data/2.5/weather?lat=' + \
        lat + '&lon=' + lon + '&appid=' + WEATHER_API_TOKEN
    weather_data = requests.get(current_api).json()
    print(weather_data)

    main = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description']
    temp_min = int(weather_data['main']['temp_min']-273)
    temp_max = int(weather_data['main']['temp_max']-272)
    print("Weather is {0} {1} Temperature is mininum {2} Celcius and maximum is {3} Celcius".format(
        main, description, temp_min, temp_max))

    return weather_data


def LatLngWeather(lat, lng):

    WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')

    current_api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={WEATHER_API_TOKEN}"
    weather_data = requests.get(current_api).json()
    print(weather_data)

    main = weather_data['weather'][0]['main']
    description = weather_data['weather'][0]['description']
    temp_min = int(weather_data['main']['temp_min']-273)
    temp_max = int(weather_data['main']['temp_max']-272)
    print("Weather is {0} {1} Temperature is mininum {2} Celcius and maximum is {3} Celcius".format(
        main, description, temp_min, temp_max))

    return weather_data
