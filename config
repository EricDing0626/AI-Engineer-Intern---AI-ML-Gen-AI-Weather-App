import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///weather.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # OpenWeatherMap API key (replace with your actual key)
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY") or "YOUR_OPENWEATHERMAP_API_KEY"
