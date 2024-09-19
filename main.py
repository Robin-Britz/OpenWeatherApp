import fastapi
import dotenv
import os
import requests
import json
import datetime

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")

date_format = "%Y-%m-%d %H:%M:%S.%f"

app = fastapi.FastAPI()


def cached_data():
    if os.path.isfile("weather_data.json"):
        with open("weather_data.json", "r") as weather_file:
            timestamp = json.load(weather_file)["Timestamp"]
            timestamp = datetime.datetime.strptime(timestamp, date_format)
            difference = datetime.datetime.now() - timestamp

            # 10800 seconds == 3 hours
            if difference.total_seconds() < 10800:
                return True
    return False


@app.get("/")
def read_root():
    return {"Python Fun": "OpenWeather API"}


@app.get("/city/")
def get_city(city: str = fastapi.Query(description="City name")):
    """Retrieve latitude and longitude for given city."""
    geocode_api = f"http://api.openweathermap.org/geo/1.0/direct?q={city}=&appid={api_key}"
    geocode_api_results = requests.get(geocode_api).json()
    if geocode_api_results:
        latitude = geocode_api_results[0]["lat"]
        longitude = geocode_api_results[0]["lon"]
        return {"Latitude": latitude, "Longitude": longitude}
    return {"Error": "No results found"}


@app.get("/weather-by-city/")
def weather_by_city(latitude: float, longitude: float):
    """Retrieve weather data for city based on latitude and longitude"""
    if cached_data():
        with open("weather_data.json", "r") as weather_file:
            return json.load(weather_file)

    else:
        weather_api = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={api_key}"
        weather_data = requests.get(weather_api).json()
        timestamp = datetime.datetime.now()
        weather_data["Timestamp"] = str(timestamp)

        with open("weather_data.json", "w") as weather_file:
            json.dump(weather_data, weather_file)

        with open("weather_data.json", "r") as weather_file:
            return json.load(weather_file)


weather_by_city(-23.0379481, 30.6493787)
