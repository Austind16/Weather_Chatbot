import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if response.status_code == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "description": data["weather"][0]["description"],

                # New fields
                "country": data["sys"]["country"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0),
                "cloudiness": data["clouds"]["all"],
                "condition": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"],
                "sunrise": data["sys"]["sunrise"],
                "sunset": data["sys"]["sunset"],
                "wind_direction": data["wind"].get("deg", 0)
            }
            return weather
        else:
            return None

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
    
def generate_weather_advice(weather):

    advice = []

    if weather["temp"] > 35:
        advice.append("🔥 It's very hot today. Stay hydrated.")

    elif weather["temp"] < 10:
        advice.append("🧥 It's quite cold. Consider wearing a jacket.")

    if weather["humidity"] > 80:
        advice.append("💧 Humidity is high today.")

    if weather["wind"] > 8:
        advice.append("💨 Strong winds expected.")

    if "rain" in weather["description"].lower():
        advice.append("☔ Carry an umbrella.")

    if not advice:
        advice.append("🌤️ Weather conditions look pleasant.")

    return advice