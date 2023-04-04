import os.path
import random

OWNER_NAME = "Pranav Minasandra" #Change this into your own name.

RESOURCE_DIR = "resources"
TEMP_DIR = "temp"
TTS_TLD = "co.uk"

PODCAST_LIST = os.path.join(RESOURCE_DIR, "podcasts.csv")

CATEGORY_ORDER = random.choice([["news", "music", "science"], ["news", "music", "history"]])
#CATEGORY_ORDER = ["misc"]

# Set OVERRIDE_LATEST_NEWS to True if you want non-latest news episodes to be played as well.
OVERRIDE_LATEST_NEWS = False

SUPPRESS_AUDIO_MIXING = False # Set to True if you are a buzzkill who hates music, Ebenezer,
AUDIO_LEAD_IN_FILE = os.path.join(RESOURCE_DIR, "lead-in_29.mp3")
AUDIO_LEAD_IN_INTERVAL = 29*1000
AUDIO_CONTINUITY_FILE = os.path.join(RESOURCE_DIR, "lead-in_29.mp3")
AUDIO_CONTINUITY_INTERVAL = 12*1000
