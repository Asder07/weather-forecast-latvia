from flask import Flask, render_template
import requests
import json

app = Flask(__name__)
API_KEY = "4a8b98824b73ded06b827c75181d90a2"

def get_weather(city_id):
    url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={API_KEY}&units=metric&lang=lv"
    return requests.get(url).json()

def select_background(weather_main):
    weather_main = weather_main.lower()
    if 'snow' in weather_main:
        return 'snow.gif'
    elif 'rain' in weather_main or 'drizzle' in weather_main:
        return 'rain.gif'
    elif 'clear' in weather_main:
        return 'sunny.gif'
    return 'sunny.gif'

@app.route("/")
def index():
    with open("latvia_cities.json", encoding="utf-8") as f:
        cities = json.load(f)

    riga_weather = get_weather(456172) 
    background = select_background(riga_weather['weather'][0]['main'])

    weather_data = [
        {
            'name': city['name'],
            'temp': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'city_id': city['id']
        }
        for city in cities
        if (city_weather := get_weather(city['id']))
    ]

    return render_template("index.html", cities=weather_data, background=background)

@app.route("/city/<int:city_id>")
def city_details(city_id):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={API_KEY}&units=metric&lang=lv"
    forecast_data = requests.get(forecast_url).json()
    background = select_background(get_weather(456172)['weather'][0]['main'])
    return render_template("city_details.html", city=forecast_data, background=background)

if __name__ == "__main__":
    app.run(debug=True)
