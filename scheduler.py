import os
import os.path
import random
import uuid

import pandas as pd
import requests

import announcer
import config
import podcasts
import tts

def choose_programme(category, podcastlist):
    """
    Chooses a podcast of the given category from the list.
    Args:
        category (str): a category in the podcasts.csv file
        podcastlist (pd.DataFrame): the read version of podcasts.csv
    """

    pdl = podcastlist[podcastlist["category"] == category]
    show = random.choice(pdl["feed"].tolist())
    return show

def choose_episode(episode_list):
    # Change this for modifying episode selection algo
    return random.choice(episode_list)

def fill_schedule():
    """
    Generates a list of episode (3-tuples) that forms the schedule for the day.
    """

    print("Generating schedule")
    schedule = []

    pdl = pd.read_csv(config.PODCAST_LIST)

    for category in config.CATEGORY_ORDER:
        show_url = choose_programme(category, pdl)
        feed = podcasts.parse_feed(show_url)

        if category != "news" or config.OVERRIDE_LATEST_NEWS:
            episode = choose_episode(podcasts.get_recent_episodes(feed))
        else:
            episode = choose_episode(podcasts.get_recent_episodes(feed, 1))

        schedule.append((feed, episode))

    return schedule


def download_schedule_materials(schedule, target="default"):
    if target == "default":
        target = os.path.join(config.TEMP_DIR, "current/")
    os.makedirs(target, exist_ok=True)

    item_num = 1
    for feed, episode in schedule:
        print("Downloading episode:", episode[0])
        url = episode[2]
        data = requests.get(url)
        path = os.path.join(target, f"{item_num:03}.mp3")
        with open(path, "wb") as p:
            p.write(data.content)
        print("finished!")

        item_num += 1


def generate_all_announcements(schedule):
    announcements = []
    for feed, episode in schedule:
        announcements.append(announcer.generate_announcement(feed, episode[2]))

    return announcements

def generate_main_intro(schedule, date="default"):

    details = ""
    i = 0
    for feed, episode in schedule:
        category = config.CATEGORY_ORDER[i]
        details += f"Item {i}: Show -- {feed['title']}\tEpisode -- {episode[0]}\n"
        i += 1

    return announcer.generate_intro(date=date, extra_details=details)

def save_announcer_voices(schedule):

    # Save intro
    main_intro_text = generate_main_intro(schedule)
    tts.generate_voice_saying(main_intro_text, os.path.join(config.TEMP_DIR, "current/", "000.mp3"))

    # Continuity text
    announcements = generate_all_announcements(schedule)
    i = 0
    for announcement in announcements:
        tts.generate_voice_saying(announcement, os.path.join(config.TEMP_DIR, "current/", f"{i:03}a.mp3"))
        i += 1

if __name__ == "__main__":
    schedule = fill_schedule()
    download_schedule_materials(schedule)
    save_announcer_voices(schedule)
