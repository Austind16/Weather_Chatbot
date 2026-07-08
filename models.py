from extensions import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    chats = db.relationship("Chat", backref="user", lazy=True)

class Chat(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable = False)
    created_at = db.Column(
    db.DateTime,
    default=datetime.utcnow,
    nullable=False
    )
    user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=False
    )