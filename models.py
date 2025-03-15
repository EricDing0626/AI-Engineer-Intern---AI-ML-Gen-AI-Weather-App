from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120), nullable=False)
    date_range = db.Column(db.String(50))  # For simplicity, stored as a string "YYYY-MM-DD to YYYY-MM-DD"
    current_weather = db.Column(db.Text)   # Store the API response (JSON string)
    forecast = db.Column(db.Text)          # Store forecast data (JSON string)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
