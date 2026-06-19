import sys
import requests


GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_coordinates(city_name):
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    resp = requests.get(GEO_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    if "results" not in data or not data["results"]:
        print(f"City '{city_name}' not found.")
        sys.exit(1)
    result = data["results"][0]
    return result["latitude"], result["longitude"], result.get("name", city_name)


def get_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "timezone": "auto",
    }
    resp = requests.get(WEATHER_URL, params=params)
    resp.raise_for_status()
    return resp.json()


def weather_code_description(code):
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
    }
    return codes.get(code, f"Unknown ({code})")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <city_name>")
        sys.exit(1)
    city = " ".join(sys.argv[1:])
    lat, lon, name = get_coordinates(city)
    weather = get_weather(lat, lon)
    current = weather["current"]
    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]
    wcode = current["weather_code"]
    desc = weather_code_description(wcode)
    print(f"Weather in {name}:")
    print(f"  Temperature: {temp}°C")
    print(f"  Humidity: {humidity}%")
    print(f"  Wind Speed: {wind} km/h")
    print(f"  Conditions: {desc}")


if __name__ == "__main__":
    main()
