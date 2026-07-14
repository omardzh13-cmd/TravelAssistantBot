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


if __name__ == "__main__":


    city = input("Введите город: ")
    result = get_weather(city)


    if result is None:
        print("Город не найден.")
    else:
        print(f"\nГород: {result['city']}")
        print(f"Страна: {result['country']}")
        print(f"Температура: {result['temperature']}°C")
        print(f"Ветер: {result['wind']} км/ч")
        print(f"Последнее обновление: {result['time']}")