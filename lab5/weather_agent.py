import sys
import json
import requests
from openai import OpenAI


OLLAMA_BASE = "http://localhost:11434/v1"
MODEL = "mistral"

client = OpenAI(base_url=OLLAMA_BASE, api_key="ollama")


def get_weather(city):
    geo = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count": 1}).json()
    if "results" not in geo:
        return f"City '{city}' not found."
    loc = geo["results"][0]
    lat, lon, name = loc["latitude"], loc["longitude"], loc.get("name", city)
    wx = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": lat, "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "timezone": "auto",
    }).json()
    c = wx["current"]
    codes = {0: "Clear", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Foggy",
             51: "Drizzle", 61: "Rain", 71: "Snow", 95: "Thunderstorm"}
    desc = codes.get(c["weather_code"], f"Code {c['weather_code']}")
    return f"Weather in {name}: {c['temperature_2m']}C, humidity {c['relative_humidity_2m']}%, wind {c['wind_speed_10m']} km/h, {desc}"


def weather_tool():
    return {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"],
            },
        },
    }


def plain_response(city):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"What is the current weather in {city}?"},
    ]
    r = client.chat.completions.create(model=MODEL, messages=messages)
    return r.choices[0].message.content


def tool_response(city):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use the get_weather tool to answer weather questions."},
        {"role": "user", "content": f"What is the current weather in {city}?"},
    ]
    r = client.chat.completions.create(model=MODEL, messages=messages, tools=[weather_tool()])
    msg = r.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            result = get_weather(args["city"])
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        r = client.chat.completions.create(model=MODEL, messages=messages, tools=[weather_tool()])
        return r.choices[0].message.content
    return msg.content


if __name__ == "__main__":
    city = " ".join(sys.argv[1:]) or "Bucharest"

    print("=" * 60)
    print(f"Query: What is the weather in {city}?")
    print("=" * 60)
    print()
    print("--- PLAIN MODEL (no tools) ---")
    print(plain_response(city))
    print()
    print("--- MODEL WITH TOOL CALLS ---")
    print(tool_response(city))
