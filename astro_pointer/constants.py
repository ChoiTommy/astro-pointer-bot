"""
This file consists of constants used in this bot.

"""

import os
# from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


# Load credentials from environment variables
# load_dotenv()


# main.py
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DATABASE_URL = os.getenv("DATABASE_URL")


# Star Map
class Starmap:
    STAR_MAP_BASE_URL = "https://www.heavens-above.com/SkyAndTelescope/StSkyChartPDF.ashx"  # params to be injected: time, latitude, longitude, location, utcOffset(in ms)
    REFRESH_CALLBACK_DATA = "REFRESH_STARMAP"
    REFRESH_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("↻ Refresh", callback_data=REFRESH_CALLBACK_DATA)]
    ])

    REDSCALE_DB_KEY = "useRedscale"
    DEFAULT_PREFERENCES = {
        "showEquator": False,
        "showEcliptic": True,
        "showStarNames": False,
        "showPlanetNames": True,
        "showConsNames": True,
        "showConsLines": True,
        "showConsBoundaries": False,
        "showSpecials": False,
        "use24hClock": True,         # NEVER change this to False, 24-hr gang
        REDSCALE_DB_KEY: False,      # will be deleted when passed in the request
    }

    GENERATE_CALLBACK_DATA = "GENERATE_STAR_MAP"
    RESET_TO_DEFAULT_CALLBACK_DATA = "RESET_TO_DEFAULT_STAR_MAP"

    PREF_CALLBACK_DATA_PREFIX = "PREF_STAR_MAP"      # in the form of "PREF_STAR_MAP_<PARAM_NAME>"
    REDSCALE_CALLBACK_DATA = f"{PREF_CALLBACK_DATA_PREFIX}_REDSCALE"
    NAME_TO_CALLBACK_DATA = {       # for easy population of inline keyboard buttons
        "Equator": f"{PREF_CALLBACK_DATA_PREFIX}_EQUATOR",
        "Ecliptic": f"{PREF_CALLBACK_DATA_PREFIX}_ECLIPTIC",
        "Star Names": f"{PREF_CALLBACK_DATA_PREFIX}_STAR_NAMES",
        "Planet Names": f"{PREF_CALLBACK_DATA_PREFIX}_PLANET_NAMES",
        "Cons Names": f"{PREF_CALLBACK_DATA_PREFIX}_CONS_NAMES",
        "Cons Lines": f"{PREF_CALLBACK_DATA_PREFIX}_CONS_LINES",
        "Cons Bound": f"{PREF_CALLBACK_DATA_PREFIX}_CONS_BOUNDARIES",
        "Specials": f"{PREF_CALLBACK_DATA_PREFIX}_SPECIALS",
    }
    '''
PARAMETERS_DESCRIPTION = {
    "Equator": "an imaginary line around the middle of the celestial sphere",
    "Ecliptic": "the plane of Earth's orbit around the Sun",
    "Star Names": "names of stars",
    "Planet Names": "names of planets",
    "Cons Names": "names of constellations",
    "Cons Lines": "lines of constellations",
    "Cons Bound": "boundaries of constellations",
    "Specials": "special celestial objects",
    "Redscaling": "red light helps with maintaining scotopic vision (night vision)",
}
    '''
    CALLBACK_DATA_TO_DB_KEYS = {    # lookup table for getting db keys
        f"{PREF_CALLBACK_DATA_PREFIX}_EQUATOR": "showEquator",
        f"{PREF_CALLBACK_DATA_PREFIX}_ECLIPTIC": "showEcliptic",
        f"{PREF_CALLBACK_DATA_PREFIX}_STAR_NAMES": "showStarNames",
        f"{PREF_CALLBACK_DATA_PREFIX}_PLANET_NAMES": "showPlanetNames",
        f"{PREF_CALLBACK_DATA_PREFIX}_CONS_NAMES": "showConsNames",
        f"{PREF_CALLBACK_DATA_PREFIX}_CONS_LINES": "showConsLines",
        f"{PREF_CALLBACK_DATA_PREFIX}_CONS_BOUNDARIES": "showConsBoundaries",
        f"{PREF_CALLBACK_DATA_PREFIX}_SPECIALS": "showSpecials",
        REDSCALE_CALLBACK_DATA: REDSCALE_DB_KEY,
    }


# Astrodata
class Astrodata:
    API_BASE_URL = "https://api.weatherapi.com/v1/astronomy.json"
    API_KEY = os.getenv("WEATHER_API_KEY")
    MOON_PHASE_DICT = {             # dict for getting the corresponding moon phase emojis
        "New Moon" : "🌑",
        "Waxing Crescent" : "🌒",
        "First Quarter" : "🌓",
        "Waxing Gibbous" : "🌔",
        "Full Moon" : "🌕",
        "Waning Gibbous" : "🌖",
        "Third Quarter" : "🌗",
        "Waning Crescent" : "🌘"
    }
    REFRESH_CALLBACK_DATA = "REFRESH_ASTRODATA"
    REFRESH_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("↻ Refresh", callback_data=REFRESH_CALLBACK_DATA)]
    ])


# Weather
class Weather:
    API_KEY = Astrodata.API_KEY
    API_BASE_URL = "https://api.weatherapi.com/v1/current.json"
    REFRESH_CALLBACK_DATA = "REFRESH_WEATHER"
    REFRESH_BUTTON = InlineKeyboardMarkup([
        [InlineKeyboardButton("↻ Refresh", callback_data=REFRESH_CALLBACK_DATA)]
    ])


# Sun
class Sun:
    UPDATE_PHOTO = "SUN"
    SHOW_DESCRIPTION = "SHOW"
    HIDE_DESCRIPTION = "HIDE"
    PHOTO_URLS = [  # 19 photos, indices from 0..18
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0193.jpg",          # AIA 193 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg",          # AIA 304 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0171.jpg",          # AIA 171 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0211.jpg",          # AIA 211 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0131.jpg",          # AIA 131 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0335.jpg",          # AIA 335 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0094.jpg",          # AIA 094 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_1600.jpg",          # AIA 1600 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_1700.jpg",          # AIA 1700 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_211193171.jpg",     # AIA 211 Å, 193 Å, 171 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/f_304_211_171_1024.jpg",        # AIA 304 Å, 211 Å, 171 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/f_094_335_193_1024.jpg",        # AIA 094 Å, 335 Å, 193 Å
        "https://sdo.gsfc.nasa.gov/assets/img/latest/f_HMImag_171_1024.jpg",         # AIA 171 Å & HMIB
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIB.jpg",          # HMI Magnetogram
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBC.jpg",         # HMI Colorized Magnetogram
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIC.jpg",         # HMI Intensitygram - colored
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg",         # HMI Intensitygram - Flattened
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMII.jpg",          # HMI Intensitygram
        "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMID.jpg"           # HMI Dopplergram
    ]
    PHOTO_COUNT = len(PHOTO_URLS)
    PHOTO_NAMES = [
        "AIA 193 Å",
        "AIA 304 Å",
        "AIA 171 Å",
        "AIA 211 Å",
        "AIA 131 Å",
        "AIA 335 Å",
        "AIA 094 Å",
        "AIA 1600 Å",
        "AIA 1700 Å",
        "AIA 211 Å, 193 Å, 171 Å",
        "AIA 304 Å, 211 Å, 171 Å",
        "AIA 094 Å, 335 Å, 193 Å",
        "AIA 171 Å & HMIB",
        "HMI Magnetogram",
        "HMI Colorized Magnetogram",
        "HMI Intensitygram - colored",
        "HMI Intensitygram - Flattened",
        "HMI Intensitygram",
        "HMI Dopplergram",
    ]
    PHOTO_DESCRIPTIONS = [
        # 193
        "This channel highlights the outer atmosphere of the Sun - called the corona - as well as hot flare plasma. Hot active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - called coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles.\n\n<strong>Where:</strong> Corona and hot flare plasma\n<strong>Wavelength:</strong>  193 angstroms (0.0000000193 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong> 11 times ionized iron (Fe XII)\n<strong>Characteristic temperature:</strong> 1.25 million K (2.25 million F)",
        # 304
        "This channel is especially good at showing areas where cooler dense plumes of plasma (filaments and prominences) are located above the visible surface of the Sun. Many of these features either can't be seen or appear as dark lines in the other channels. The bright areas show places where the plasma has a high density.\n\n<strong>Where:</strong> Upper chromosphere and lower transition region\n<strong>Wavelength:</strong> 304 angstroms (0.0000000304 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong> singly ionized helium (He II)\n<strong>Characteristic temperature:</strong> 50,000 K (90,000 F)",
        # 171
        "This channel is especially good at showing coronal loops - the arcs extending off of the Sun where plasma moves along magnetic field lines. The brightest spots seen here are locations where the magnetic field near the surface is exceptionally strong.\n\n<strong>Where:</strong> Quiet corona and upper transition region\n<strong>Wavelength:</strong> 171 angstroms (0.0000000171 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong>  8 times ionized iron (Fe IX)\n<strong>Characteristic temperature:</strong> 1 million K (1.8 million F)",
        # 211
        "This channel (as well as AIA 335) highlights the active region of the outer atmosphere of the Sun - the corona. Active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - called coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles.\n\n<strong>Where:</strong> Active regions of the corona\n<strong>Wavelength:</strong>  211 angstroms (0.0000000211 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong> 13 times ionized iron (Fe XIV)\n<strong>Characteristic temperature:</strong> 2 million K (3.6 million F)",
        # 131
        "This channel (as well as AIA 094) is designed to study solar flares. It measures extremely hot temperatures around 10 million K (18 million F), as well as cool plasmas around 400,000 K (720,000 F). It can take images every 2 seconds (instead of 10) in a reduced field of view in order to look at flares in more detail.\n\n<strong>Where:</strong> Flaring regions of the corona\n<strong>Wavelength:</strong>  131 angstroms (0.0000000131 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong>  20 and 7 times ionized iron (Fe VIII, Fe XXI)\n<strong>Characteristic temperatures:</strong> 10 million K (18 million F)",
        # 335
        "This channel (as well as AIA 211) highlights the active region of the outer atmosphere of the Sun - the corona. Active regions, solar flares, and coronal mass ejections will appear bright here. The dark areas - or coronal holes - are places where very little radiation is emitted, yet are the main source of solar wind particles.\n\n<strong>Where:</strong> Active regions of the corona\n<strong>Wavelength:</strong>  335 angstroms (0.0000000335 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong> 15 times ionized iron (Fe XVI)\n<strong>Characteristic temperature:</strong> 2.8 million K (5 million F)",
        # 094
        "This channel (as well as AIA 131) is designed to study solar flares. It measures extremely hot temperatures around 6 million Kelvin (10.8 million F). It can take images every 2 seconds (instead of 10) in a reduced field of view in order to look at flares in more detail.\n\n<strong>Where:</strong> Flaring regions of the corona\n<strong>Wavelength:</strong>  94 angstroms (0.0000000094 m) = Extreme Ultraviolet/soft X-rays\n<strong>Primary ions seen:</strong>  17 times ionized iron (Fe XVIII)\n<strong>Characteristic temperature:</strong> 6 million K (10.8 million F)",
        # 1600
        "This channel (as well as AIA 1700) often shows a web-like pattern of bright areas that highlight places where bundles of magnetic fields lines are concentrated. However, small areas with a lot of field lines will appear black, usually near sunspots and active regions.\n\n<strong>Where:</strong> Transition region and upper photosphere\n<strong>Wavelength:</strong>  1600 angstroms (0.00000016 m) = Far Ultraviolet\n<strong>Primary ions seen:</strong>  thrice ionized carbon (C IV) and Continuum\n<strong>Characteristic temperatures:</strong> 6,000 K (11,000 F), and 100,000 K (180,000 F)",
        # 1700
        "This channel (as well as AIA 1600) often shows a web-like pattern of bright areas that highlight places where bundles of magnetic fields lines are concentrated. However, small areas with a lot of field lines will appear black, usually near sunspots and active regions.\n\n<strong>Where:</strong> Temperature minimum and photosphere\n<strong>Wavelength:</strong> 1700 angstroms (0.00000017 m) = Far Ultraviolet\n<strong>Primary ions seen:</strong> Continuum\n<strong>Characteristic temperature:</strong> 6,000 K (11,000 F)",
        # 211, 193, 171
        "This image combines three images with different, but very similar, temperatures. The colors are assigned differently than in the single images. Here AIA 211 is red, AIA 193 is green, and AIA 171 is blue.  Each highlights a different part of the corona.",
        # 304, 211, 171
        "This image combines three images with quite different temperatures. The colors are assigned differently than in the single images. Here AIA 304 is red (showing the chromosphere), AIA 211 is green (corona), and AIA 171 is dark blue (corona).",
        # 094, 335, 193
        "This image combines three images with different temperatures. Each image is assigned a color, and they are not the same used in the single images. Here AIA 094 is red, AIA 335 is green, and AIA 193 is blue.  Each highlights a different part of the corona.",
        # 171, HMIB
        "This channel is especially good at showing coronal loops - the arcs extending off of the Sun where plasma moves along magnetic field lines. The brightest spots seen here are locations where the magnetic field near the surface is exceptionally strong.\n\n<strong>Where:</strong> Quiet corona and upper transition region\n<strong>Wavelength:</strong> 171 angstroms (0.0000000171 m) = Extreme Ultraviolet\n<strong>Primary ions seen:</strong>  8 times ionized iron (Fe IX)\n<strong>Characteristic temperature:</strong> 1 million K (1.8 million F)",
        # Magnetogram
        "Read more: <a href='https://svs.gsfc.nasa.gov/3989'>HMI Magnetogram</a>",
        # Colorized Magnetogram
        "<a href='https://sdo.gsfc.nasa.gov/assets/docs/HMI_M.ColorTable.pdf'>Read information on colorized magnetograms.</a>",
        # Intensitygram - colored
        "Read more: <a href='https://svs.gsfc.nasa.gov/3988'>HMI Intensity</a>",
        # Intensitygram - flattened
        "Read more: <a href='https://svs.gsfc.nasa.gov/3988'>HMI Intensity</a>",
        # Intensitygram
        "Read more: <a href='https://svs.gsfc.nasa.gov/3988'>HMI Intensity</a>",
        # Dopplergram
        "Read more: <a href='https://svs.gsfc.nasa.gov/3990'>HMI Dopplergram</a>"
    ]
    PHOTO_PATH = "assets/sun/"


# ISS
class ISS:
    API_BASE_URL = "http://api.open-notify.org/iss-now.json"


# User Info
NOMINATIM_REVERSE_API_BASE_URL = "https://nominatim.openstreetmap.org/reverse"


# Misc
TUTORIAL_TEXT = """
<code>astro* bot;</code> is your ultimate companion for stargazing adventures, providing easy access to essential information.

To unlock the bot's full potential, it's important to set your location using /setlocation. This location data enables us to generate star maps and display weather and astronomical data specific to your chosen spot. Rest assured, you have full control over your data and can delete it anytime using /deletemyinfo.

Since weather and astronomical conditions don't vary significantly within a few kilometers, feel free to disable the 'Precise Location' setting on iOS or choose 'Approximate location' on Android within your Telegram app settings. When setting up your location, you can move the map around in the app to pinpoint your desired spot.

To navigate through the bot's features, simply tap the menu button located at the bottom right. This allows you to effortlessly switch between commands and the keyboard.

Get ready to enjoy the wonders of the night sky with <code>astro* bot;</code> by your side! 🌌✨
"""

COMMAND_KEYBOARD = ReplyKeyboardMarkup(
    [
        ['/starmap', '/starmap skip', '/astrodata'],
        ['/sun', '/weather', '/iss'],
        ['/sub', '/unsub'],
        ['/myinfo', '/setlocation', '/deletemyinfo'],
        ['/allcommands']
    ],
    resize_keyboard = True
)

COMMAND_DESCRIPTIONS = """
Command list:

/starmap - Get a starmap of the current sky
Option: skip, -s to generate a star map right away
/astrodata - Get astronomical data
/sun - View Sun images in various wavelengths
/weather - Know the weather before stargazing 
/iss - Track the live location of ISS for 2 mins
/sub - Subscribe to receive notifications every day 
/unsub - Unsubscribe from features
/myinfo - Display your set location
/setlocation - Modify your location
/deletemyinfo - Delete your data
/cancel - Halt any conversation
/credits - Learn more on the data source provider
/start - Brief introduction of the bot
/allcommands - Feel the power of self-referencing
"""
