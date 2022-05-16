"""
@star_map_bot is an easy-to-use stargazing bot that provides you with
all the necessary stargazing information including star maps (sky
charts), weather and astronomical data, etc.

Usage:
Send /start to get a welcome message from the bot.
Send /setlocation to set your location to enable the the core features.
Send /starmap to get a star map pdf at the location set.
Send /astrodata to get a list of astronomical data at the location set.
Send /weather to get a weather report at the location set.
Send /myinfo to view the data associate with you stored on the server.
Send /deletemyinfo to purge you data permanently on the server.
Send /credits to view the data sources of all the infomation this bot provides.
Send /cancel to halt any operations.
"""

# TODO pdf to image, red scale img, star map features toggles, etc.
import misc, userinfo, settings, starmap, astrodata, weather

import logging
import os
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from dotenv import load_dotenv


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO
)
logger = logging.getLogger(__name__)

# Load credentials from environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def main() -> None:
    """Entry point of the script."""

    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", misc.bot_tutorial))
    dispatcher.add_handler(CommandHandler("credits", misc.show_credits))
    dispatcher.add_handler(CommandHandler("starmap", starmap.send_star_map))
    dispatcher.add_handler(CommandHandler("myinfo", userinfo.show_user_info))
    dispatcher.add_handler(CommandHandler("astrodata", astrodata.show_astro_data))
    dispatcher.add_handler(CommandHandler("weather", weather.show_weather_data))

    dispatcher.add_handler(ConversationHandler(
        entry_points = [CommandHandler("setlocation", settings.set_location)],
        states = {
            0: [MessageHandler(Filters.location, settings.update_location)]
        },
        fallbacks = [CommandHandler("cancel", settings.cancel)],
        conversation_timeout = 120 # 2 mins
    ))

    dispatcher.add_handler(ConversationHandler(
        entry_points = [CommandHandler("deletemyinfo", userinfo.deletion_confirmation)],
        states = {
            0: [MessageHandler(Filters.regex("^(Yes|No)$"), userinfo.delete_user_info)]
        },
        fallbacks = [CommandHandler("cancel", userinfo.cancel_deletion)],
        conversation_timeout = 120
    ))

    # Start the Bot using polling
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()