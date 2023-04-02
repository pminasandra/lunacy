import os.path
import random

RESOURCE_DIR = "resources"
TEMP_DIR = "temp"
TTS_TLD = "co.uk"

PODCAST_LIST = os.path.join(RESOURCE_DIR, "podcasts.csv")

CATEGORY_ORDER = random.choice([["news", "music", "science"], ["news", "music", "history"]])

# Set OVERRIDE_LATEST_NEWS to True if you want non-latest news episodes to be played as well.
OVERRIDE_LATEST_NEWS = False
