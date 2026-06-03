# Weather Chatbot

A web-based chatbot built with Flask that provides real-time weather information and natural conversation. Users can ask about the weather, humidity, or wind in any city, and the chatbot responds with up-to-date data using the OpenWeatherMap API and Google Gemini for enhanced understanding.

## Features

- **Conversational Chatbot:** Ask about weather, humidity, or wind in any city.
- **Live Weather Data:** Fetches current weather using OpenWeatherMap API.
- **Natural Language Understanding:** Uses Google Gemini for intent detection and city extraction.
- **Session-based Chat History:** Remembers your conversation during the session.
- **Simple Web Interface:** Clean UI with weather panels and chat.

## Installation

1. **Clone the repository:**
	```
	git clone <repo-url>
	cd Weather_Chatbot
	```

2. **Install dependencies:**
	```
	pip install -r requirements.txt
	```

3. **Set up environment variables:**
	- Create a `.env` file in the root directory.
	- Add your OpenWeatherMap API key and Gemini API key:
	  ```
	  API_KEY=your_openweathermap_api_key
	  GEMINI_API_KEY=your_gemini_api_key
	  SECRET_KEY=your_flask_secret_key
	  ```

4. **Run the app:**
	```
	python app.py
	```

5. **Open your browser:**  
	Visit `http://127.0.0.1:5000/`

## Project Structure

- `app.py` — Main Flask application.
- `services/`
  - `chatbot_service.py` — Handles chatbot logic and intent parsing.
  - `weather_service.py` — Fetches weather data from OpenWeatherMap.
- `templates/` — HTML templates.
- `static/` — CSS, JS, and images.
- `utils/` — Helper functions.

## Requirements

- Flask
- requests
- python-dotenv
- google-generativeai

## Example Usage

- “What’s the weather in London?”
- “Is it humid in Mumbai?”
- “How windy is it in New York?”

## License

MIT License
