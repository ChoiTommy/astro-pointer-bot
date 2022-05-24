"""
weather is a module that consists of functions fetching and displaying weather data relevant to stargazing.

Usage:
Command /weather is defined by show_weather_data
"""

import constants
import requests
from firebase_admin import db
from telegram import Update, ParseMode
from telegram.ext import CallbackContext


def show_weather_data(update: Update, context: CallbackContext) -> None:
    """Fetch and send a simple weather report showing weather data necessary for stargazing."""

    user_id = str(update.effective_user.id)
    ref = db.reference(f"/Users/{user_id}")
    data = ref.get()

    if data != None:
        lat = data["latitude"]
        longi = data["longitude"]

        WEATHER_API_URL = ("https://api.weatherapi.com/v1/"
                            "current.json"
                            f"?key={constants.WEATHER_API_KEY}"
                            f"&q={lat},{longi}")

        response = requests.get(WEATHER_API_URL)
        weather_data = response.json()

        current_condition_text = weather_data["current"]["condition"]["text"]
        current_condition_icon_url = weather_data["current"]["condition"]["icon"]
        temperature = weather_data["current"]["temp_c"]
        precipitation_mm = weather_data["current"]["precip_mm"]
        cloud_percentage = weather_data["current"]["cloud"]
        visibility_km = weather_data["current"]["vis_km"]
        uv_index = weather_data["current"]["uv"]

        current_date_time = weather_data["location"]["localtime"]

        update.message.reply_photo(
            photo = f"https:{current_condition_icon_url}",
            caption = ("Weather at your location: \n"                           # TODO better formatting for data display
                        f"Condition: <b>{current_condition_text}</b> \n"
                        f"Temperature: <b>{temperature}°C</b> \n"
                        f"Precipitation: <b>{precipitation_mm} mm</b> \n"
                        f"Cloud coverage: <b>{cloud_percentage}%</b> \n"
                        f"Visibility: <b>{visibility_km} km</b> \n"
                        f"UV index: <b>{uv_index}</b> \n"
                        f"({current_date_time}) \n\n"

                        "Be prepared before setting out for stargazing!"),
            parse_mode = ParseMode.HTML
        )

    else:
        update.message.reply_text("Please set your location with /setlocation first!")