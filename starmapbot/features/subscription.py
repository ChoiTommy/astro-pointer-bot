'''
TODO better onboarding
Syntax: /subscribe [starmap|astrodata|weather|iss|sun] [timings]
timings: time on a day, scheduled daily, UTC time for now # TODO support timezones
one subscription per feature, old sub timings will get replaced by the new one

e.g. /subscribe weather,starmap,sun 20:00,22:30,12:00

without 2/1 arguments: show subscription information only

Database
"Subscription": {
    "user_id": {
        "chat_id": {
            "starmap": {"enabled": bool, "timing": {"hour": str, "minute": str}},
            "astrodata": {"enabled": bool, "timing": {"hour": str, "minute": str}},
            "weather": {"enabled": bool, "timing": {"hour": str, "minute": str}},
            "iss": {"enabled": bool, "timing": {"hour": str, "minute": str}},
            "sun": {"enabled": bool, "timing": {"hour": str, "minute": str}}
        }
    }
}

Syntax: /unsubscribe [starmap|astrodata|weather|iss|sun]
'''
from starmapbot.features.starmap import star_map_subscription
from starmapbot.features.astrodata import astro_data_subscription
from starmapbot.features.weather import weather_subscription
from starmapbot.features.iss import iss_subscription
from starmapbot.features.sun import sun_subscription
from datetime import time
from firebase_admin import db
from telegram import Update
from telegram.ext import CallbackContext
from tabulate import tabulate


DEFAULT_FEATURES = {
    "starmap": star_map_subscription,
    "astrodata": astro_data_subscription,
    "weather": weather_subscription,
    "iss": iss_subscription,
    "sun": sun_subscription
}

DEFAULT_DB = {
    key: {
        "enabled": False,
        "timing": {
            "hour": "-1",
            "minute": "-1"
        }
    }
    for key in DEFAULT_FEATURES
}

def are_timings_valid(li: list[str]) -> (bool, list[str], list[str]):
    # check colon, check ranges
    hour, minute = [], []
    for l in li:
        timing = l.split(':')
        if len(timing) != 2:
            return False, [], []
        if int(timing[0]) not in range(24):
            return False, [], []
        if int(timing[1]) not in range(60):
            return False, [], []
        hour.append(timing[0])
        minute.append(timing[1])
    return True, hour, minute


def are_features_valid(li: list[str]) -> bool:
    for l in li:
        if l not in DEFAULT_FEATURES:
            return False
    return True


async def subscribe(update: Update, context: CallbackContext) -> None:

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    args = context.args

    if len(args) == 2:
        f, t = context.args

        features = [f.lower() for f in f.split(',')]
        timings = t.split(',')

        if len(features) != len(timings):
            # number of features is not equal to number of timings
            await update.message.reply_text(text="The number of features must be equal to that of the timings. Please set again.")
            return

        if not are_features_valid(features):
            # some features are invalid
            await update.message.reply_text(text="Make sure the features are of the 5 presets only. Please set again.")
            return

        valid_time, hour, minute = are_timings_valid(timings)
        if not valid_time:
            # timings do not follow the format
            await update.message.reply_text(text="Please follow the format for timings `<hour:minute>`. Please set again.")
            return

    else:
        # not providing enough arguments
        tble = get_user_subscription_info(user_id, chat_id)
        await update.message.reply_markdown_v2(
            text = ("Arguments missing\. \n"
                    "Syntax: `/subscribe [starmap|astrodata|weather|iss|sun] [timings]` \n"
                    "Here are your current subscriptions: \n"
                    f"`{tabulate(tble, tablefmt='fancy_grid', headers=['Feature', 'Daily Time'])}`")
        )
        return

    ref = db.reference(f"/Subscriptions/{user_id}/{chat_id}")
    user_data = DEFAULT_DB if ref.get() is None else ref.get()

    display_text = []

    # add to user_data for pushing to the db & add to job queue
    for feature, h, m, timing in zip(features, hour, minute, timings):
        if user_data[feature]["enabled"]:
            jobs_list = context.job_queue.get_jobs_by_name(f"{user_id}_{chat_id}_{feature}")
            for job in jobs_list:
                job.schedule_removal()
            display_text.append([feature, f"{user_data[feature]['timing']['hour']}:{user_data[feature]['timing']['minute']} -> {timing}"])
        else:
            display_text.append([feature, timing])

        user_data[feature]["enabled"] = True
        user_data[feature]["timing"]["hour"] = h
        user_data[feature]["timing"]["minute"] = m

        t = time(hour=int(h), minute=int(m))
        context.job_queue.run_daily(
            callback = DEFAULT_FEATURES[feature],
            time = t,
            name = f"{user_id}_{chat_id}_{feature}",
            user_id = user_id,
            chat_id = chat_id
        )

    ref.update(user_data)

    await update.message.reply_markdown_v2(
        text = ("Newly subscribed/modified daily notifications: \n"
                f"`{tabulate(display_text, tablefmt='fancy_grid', headers=['Feature', 'Daily Time'])}`")
    )


async def unsubscribe(update: Update, context: CallbackContext) -> None:

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    ref = db.reference(f"/Subscriptions/{user_id}/{chat_id}")

    if ref.get() is None:
        update.message.reply_text(text="You have yet to subscribe to any features. Nothing has been unsubscribed.")

    else:
        user_data = ref.get()
        args = context.args

        if len(args) == 1:
            f = context.args[0]
            features = [f.lower() for f in f.split(',')]

            if not are_features_valid(features):
                # some features are invalid
                await update.message.reply_text(text="Make sure the features are of the 5 presets only.")
                return

        else:
            # not providing enough arguments
            await update.message.reply_text(text="Arguments missing. Please set again.")
            return

        display_text = []

        for feature in features:
            if user_data[feature]["enabled"]:
                jobs_list = context.job_queue.get_jobs_by_name(f"{user_id}_{chat_id}_{feature}")
                for job in jobs_list:
                    job.schedule_removal()

                user_data[feature]["enabled"] = False
                user_data[feature]["timing"]["hour"] = -1
                user_data[feature]["timing"]["minute"] = -1
                display_text.append([feature])
            else:
                display_text.append([f"{feature} (already disabled)"])

        ref.update(user_data)

        await update.message.reply_markdown_v2(
            text = ("You have been successfully unsubscribed from \n"
                    f"`{tabulate(display_text, tablefmt='pretty', headers=['Feature'])}`")
        )


def load_jobs_into_jobqueue(application): # during startup

    ref = db.reference(f"/Subscriptions")
    user_sub_data = ref.get()

    if user_sub_data is not None:
        for user_id, chat_info in user_sub_data.items():
            for chat_id, feature_info in chat_info.items():
                for feature_name, sub_info in feature_info.items():
                    if sub_info["enabled"]:
                        t = time(hour=int(sub_info["timing"]["hour"]), minute=int(sub_info["timing"]["minute"]))
                        application.job_queue.run_daily(
                            callback = DEFAULT_FEATURES[feature_name],
                            time = t,
                            name = f"{user_id}_{chat_id}_{feature_name}",
                            user_id = user_id,
                            chat_id = chat_id
                        )


def get_user_subscription_info(user_id, chat_id) -> list[list[str]]:
    ref = db.reference(f"/Subscriptions/{user_id}/{chat_id}")
    display_text = []
    user_data = ref.get() if ref.get() is not None else DEFAULT_DB
    for feature, info in user_data.items():
        if info["enabled"]:
            display_text.append([feature, f"{info['timing']['hour']}:{info['timing']['minute']}"])
        else:
            display_text.append([feature, "Not subscribed"])

    return display_text