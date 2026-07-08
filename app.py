import os

from flask import (
    Flask,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
)

from services.chatbot_service import get_chatbot_response, parse_message
from services.weather_service import get_weather

from dotenv import load_dotenv

from extensions import db

from werkzeug.security import generate_password_hash, check_password_hash

from models import Chat, User

load_dotenv()

app = Flask(__name__)

app.config.from_object("config.Config")

database_url = app.config["SQLALCHEMY_DATABASE_URI"]

if database_url.startswith("postgres://"):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

db.init_app(app)
from extensions import migrate
migrate.init_app(app, db)

app.secret_key = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def index():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    if "chat_history" not in session:
        session["chat_history"] = []

    if "current_weather" not in session:
        session["current_weather"] = None

    
    user = db.session.get(User, session["user_id"])

    if request.method == "POST":
        if "clear" in request.form:
            user = db.session.get(User, session["user_id"])

            if user:
                for chat in list(user.chats):
                    db.session.delete(chat)

                db.session.commit()

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

                chat = Chat(
                user_message=user_message,
                bot_response=bot_reply,
                user_id=session["user_id"]
                )

                db.session.add(chat)
                db.session.commit()

    return render_template(
        "index.html",
        chat_history=user.chats,
        current_weather=session["current_weather"]
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already registered.")
            return redirect(url_for("register"))
        
        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            flash("Username already taken.")
            return redirect(url_for("register"))
        
        if len(password) < 8:
            flash("Password must be at least 8 characters.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user = User(
        username=username,
        email=email,
        password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful.")

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect(url_for("index"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        
        if not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.")
            return redirect(url_for("login"))
        
        session["user_id"] = user.id
        flash("Login successful!")
        return redirect(url_for("index"))
    
    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user_id", None)

    flash("Logged out successfully.")

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()