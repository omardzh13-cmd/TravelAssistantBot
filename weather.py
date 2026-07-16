

import requests

def get_weather(city):

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    city_info = data["results"][0]

    latitude = city_info["latitude"]
    longitude = city_info["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&current_weather=true"
    )

    weather_response = requests.get(weather_url)

    if weather_response.status_code != 200:
        return None

    weather = weather_response.json()["current_weather"]

    return {
        "city": city_info["name"],
        "country": city_info["country"],
        "temperature": weather["temperature"],
        "wind": weather["windspeed"],
        "time": weather["time"]
    }



def get_forecast(city):

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    city_info = data["results"][0]

    latitude = city_info["latitude"]
    longitude = city_info["longitude"]


    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone=auto"
    )


    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code != 200:
        return None


    daily = forecast_response.json()["daily"]


    return {
        "city": city_info["name"],
        "country": city_info["country"],
        "dates": daily["time"],
        "max": daily["temperature_2m_max"],
        "min": daily["temperature_2m_min"]
    }