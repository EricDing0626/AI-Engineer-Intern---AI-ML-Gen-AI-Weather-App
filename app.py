from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests, json
from models import db, WeatherQuery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def get_weather_data(location):
    # Call OpenWeatherMap API for current weather
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={app.config['WEATHER_API_KEY']}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={app.config['WEATHER_API_KEY']}&units=metric"
    weather_response = requests.get(weather_url)
    forecast_response = requests.get(forecast_url)
    if weather_response.status_code == 200 and forecast_response.status_code == 200:
        return weather_response.json(), forecast_response.json()
    else:
        return None, None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        date_range = request.form.get("date_range")  # e.g., "2025-03-15 to 2025-03-20"
        if not location:
            flash("Location is required.", "error")
            return redirect(url_for("index"))
        current_weather, forecast = get_weather_data(location)
        if current_weather is None:
            flash("Could not retrieve weather data. Please check your location input.", "error")
            return redirect(url_for("index"))
        # Save to DB
        new_query = WeatherQuery(
            location=location,
            date_range=date_range,
            current_weather=json.dumps(current_weather),
            forecast=json.dumps(forecast)
        )
        db.session.add(new_query)
        db.session.commit()
        return render_template("weather.html", weather=current_weather, forecast=forecast, location=location)
    return render_template("index.html")

@app.route("/records")
def records():
    queries = WeatherQuery.query.order_by(WeatherQuery.timestamp.desc()).all()
    return render_template("records.html", queries=queries)

@app.route("/edit/<int:query_id>", methods=["GET", "POST"])
def edit_record(query_id):
    record = WeatherQuery.query.get_or_404(query_id)
    if request.method == "POST":
        new_location = request.form.get("location")
        new_date_range = request.form.get("date_range")
        if new_location:
            record.location = new_location
            # Optionally, update weather data when location changes
            current_weather, forecast = get_weather_data(new_location)
            if current_weather:
                record.current_weather = json.dumps(current_weather)
                record.forecast = json.dumps(forecast)
            record.date_range = new_date_range
            db.session.commit()
            flash("Record updated successfully!", "success")
            return redirect(url_for("records"))
    return render_template("edit_record.html", record=record)

@app.route("/delete/<int:query_id>", methods=["POST"])
def delete_record(query_id):
    record = WeatherQuery.query.get_or_404(query_id)
    db.session.delete(record)
    db.session.commit()
    flash("Record deleted successfully!", "success")
    return redirect(url_for("records"))

# Optional: Data Export API endpoint
@app.route("/export", methods=["GET"])
def export_data():
    records = WeatherQuery.query.all()
    output = []
    for rec in records:
        output.append({
            "id": rec.id,
            "location": rec.location,
            "date_range": rec.date_range,
            "current_weather": json.loads(rec.current_weather),
            "forecast": json.loads(rec.forecast),
            "timestamp": rec.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
