import os
from flask import Flask, render_template, request, session
from services.chatbot_service import get_chatbot_response, parse_message
from services.weather_service import get_weather
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if "current_weather" not in session:
        session["current_weather"] = None

    if request.method == "POST":
        if "clear" in request.form:
            session["chat_history"] = []
            session["current_weather"] = None
            session.modified = True

        else:
            user_message = request.form.get("message")

            if user_message:
                bot_reply = get_chatbot_response(user_message)

                parsed = parse_message(user_message)
                intent = parsed["intent"]
                city = parsed["city"]

                if intent in ["weather", "humidity", "wind"] and city:
                    weather_data = get_weather(city)

                    if weather_data:
                        session["current_weather"] = weather_data

                session["chat_history"].append({
                    "user": user_message,
                    "bot": bot_reply
                })

                session.modified = True

    return render_template(
        "index.html",
         chat_history = session["chat_history"],
         current_weather = session["current_weather"]
    )


if __name__ == "__main__":
    app.run(debug=True)