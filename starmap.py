"""
starmap is a module that consists of functions fetching and forwarding a star map (sky chart) to user.

Usage:
Command /starmap is defined by send_star_map
"""

import json, time
import requests
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
import fitz


# Star map URL
STAR_MAP_URL = "https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx"
# params to be injected: time, latitude, longitude, location, utcOffset(in ms)
REST_OF_THE_URL =  ("&showEquator=false"
                    "&showEcliptic=true"
                    "&showStarNames=true"
                    "&showPlanetNames=true"
                    "&showConsNames=true"
                    "&showConsLines=true"
                    "&showConsBoundaries=false"
                    "&showSpecials=false"
                    "&use24hClock=true")


def send_star_map(update: Update, context: CallbackContext) -> None:
    """Fetch and forward a star map to user based on the set location and the current time."""

    user_id = str(update.effective_user.id)
    with open("locations.json", 'r') as file:
        data = json.load(file)

    if user_id in data:

        lat = str(data[user_id]["latitude"])
        longi = str(data[user_id]["longitude"])
        address = data[user_id]["address"].replace(',', "%2c").replace(' ', "%20")
        utcOffset = str(data[user_id]["utcOffset"])

        fetch_target = (f"{STAR_MAP_URL}"
                        f"?time={str(int(time.time()*1000))}" # time.time(): seconds (floating point) since the epoch in UTC
                        f"&latitude={lat}"
                        f"&longitude={longi}"
                        f"&location={address}"
                        f"&utcOffset={utcOffset}"
                        f"{REST_OF_THE_URL}")

        response = requests.get(fetch_target) # Download the data behind the URL
        doc = fitz.open(stream=response.content)
        page = doc.load_page(0)  # number of page
        pix = page.get_pixmap(
            dpi = 200,
            colorspace = fitz.csRGB,
            annots = False,
            clip = fitz.IRect(1, 1, 600, 650)
        )
        pix.tint_with(black=-129010, white=0) # no idea on how these values work, just do trial and error

        # update.message.reply_document(document = fetch_target) # pdf
        update.message.reply_document(
            document = pix.tobytes(),
            caption = "Enjoy the stunning stars\! Be considerate and *leave no trace* while stargazing\!",
            parse_mode = ParseMode.MARKDOWN_V2
        )

        doc.close()

    else:
        update.message.reply_text("Please set your location with /setlocation first!")