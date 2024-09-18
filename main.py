import typing 
import fastapi
import dotenv
import os
import requests

dotenv.load_dotenv()
api_key = os.getenv("API_KEY")

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"OpenWeather": "API"}


@app.get("/city/")
def get_city(city: str = fastapi.Query(description="City name")):
    """Retrieve latitude and longitude for given city."""
    open_weather_api = f"http://api.openweathermap.org/geo/1.0/direct?q={city}=&appid={api_key}"
    city_results = requests.get(open_weather_api).json()
    if city_results:
        latitude = city_results[0]["lat"]
        longitude = city_results[0]["lon"]
        return {"Latitude": latitude, "Longitude": longitude}
    return {"Error": "No results found"}

