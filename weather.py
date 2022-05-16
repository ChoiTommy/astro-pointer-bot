"""
weather is a module that consists of functions fetching and displaying weather data relevant to stargazing.

Usage:
Command /weather is defined by show_weather_data
"""

import main
import json, urllib.request, ssl
from telegram import Update, ParseMode
from telegram.ext import CallbackContext


def show_weather_data(update: Update, context: CallbackContext) -> None:
    """Fetch and send a simple weather report showing weather data necessary for stargazing."""

    user_id = str(update.effective_user.id)
    with open("locations.json", 'r') as file:
        data = json.load(file)

    if user_id in data:
        lat = data[user_id]["latitude"]
        longi = data[user_id]["longitude"]

        WEATHER_API_URL =  (f"https://api.weatherapi.com/v1/current.json"
                            f"?key={main.WEATHER_API_KEY}"
                            f"&q={lat},{longi}")

        context = ssl._create_unverified_context()
        with urllib.request.urlopen(WEATHER_API_URL, context=context) as weather_file:
            weather_data = json.load(weather_file)

        current_condition_text = weather_data["current"]["condition"]["text"]
        current_condition_icon_url = weather_data["current"]["condition"]["icon"]
        temperature = weather_data["current"]["temp_c"]
        precipitation_mm = weather_data["current"]["precip_mm"]
        cloud_percentage = weather_data["current"]["cloud"]
        current_date_time = weather_data["location"]["localtime"]

        update.message.reply_photo(
            photo = f"https:{current_condition_icon_url}",
            caption =  (f"The weather now is <b>{current_condition_text}</b> at a temperature of <b>{temperature}°C</b>. "
                        f"Precipitation is <b>{precipitation_mm}mm</b>, with cloud coverage of <b>{cloud_percentage}%</b>. \n"
                        f"({current_date_time}) \n\n"

                        "Be prepared before setting out for stargazing!"
            ),
            parse_mode = ParseMode.HTML
        )

    else:
        update.message.reply_text("Please set your location with /setlocation first!")