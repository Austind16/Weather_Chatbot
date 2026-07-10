import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from services.weather_service import get_weather

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

def parse_message(message, last_city=None):
    message_lower = message.lower()

    # ---- STEP 1: Try RULE-BASED first ----
    weather_keywords = ["weather", "temperature", "hot", "cold", "warm", "cool"]
    humidity_keywords = ["humidity", "humid"]
    wind_keywords = ["wind", "windy", "breeze"]

    intent = None

    if any(word in message_lower for word in weather_keywords):
        intent = "weather"

    elif any(word in message_lower for word in humidity_keywords):
        intent = "humidity"

    elif any(word in message_lower for word in wind_keywords):
        intent = "wind"

    elif message_lower in ["hi", "hello"]:
        intent = "greeting"

    # if we successfully detected intent → DON'T use Gemini
    city = extract_city(message) 
    if not city:
        city = last_city
    if intent:
        return {
            "intent": intent,
            "city": city
        }
    

    # ---- STEP 2: fallback to GEMINI ----
    prompt = f"""
    Extract the intent and city from this message.

    Possible intents:
    - weather
    - humidity
    - wind
    - greeting
    - unknown

    Message: "{message}"

    Respond ONLY in JSON:
    {{
        "intent": "...",
        "city": "..."
    }}
    """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        import json
        import re

        # remove markdown formatting if present
        text = text.replace("```json", "").replace("```", "").strip()

        # extract JSON safely
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            data = json.loads(match.group())
            # if only city is detected, assume weather intent
            if data["intent"] == "unknown" and data["city"]:
                data["intent"] = "weather"

            return data
        else:
            return {
                "intent": "unknown",
                "city": ""
            }

    except Exception as e:
        print("GEMINI ERROR:", e)

        return {
            "intent": "unknown",
            "city": ""
        }

import re

def extract_city(message):
    message = message.lower()

    match = re.search(r"\b(?:in|of)\s+(.+)", message)

    if match:
        city = match.group(1)
    else:
        return ""

    # remove extra phrases
    remove_phrases = [
        "today", "now", "right now", "please", "pls",
        "in detail", "details", "detail", "rn", "?"
    ]

    for phrase in remove_phrases:
        city = city.replace(phrase, "")

    return city.strip().title()


def get_chatbot_response(message, last_city):
    parsed = parse_message(message, last_city)

    intent = parsed["intent"]
    city = parsed["city"]

    # GREETING
    if intent == "greeting":
        return "Hello! Ask me about the weather."

    # WEATHER
    elif intent == "weather":
        weather = get_weather(city)

        if weather:
            return f"In {weather['city']}, it's {weather['temp']}°C with {weather['description']}."
        else:
            return "Sorry, I couldn't find that city."

    # HUMIDITY
    elif intent == "humidity":
        weather = get_weather(city)

        if weather:
            return f"Humidity in {weather['city']} is {weather['humidity']}%."
        else:
            return "Sorry, I couldn't find that city."

    # WIND
    elif intent == "wind":
        weather = get_weather(city)

        if weather:
            return f"Wind speed in {weather['city']} is {weather['wind']} m/s."
        else:
            return "Sorry, I couldn't find that city."

    # UNKNOWN
    else:
        return "Try asking something like 'weather in Mumbai' or 'is it windy in Delhi?'"