
import datetime as dt
import random
import time
import urllib.request

import requests
import podcastparser

def parse_feed(podcast_feed_url):
    response = requests.get(podcast_feed_url)
    feed_data = response.content.decode('utf-8')

    # Parse the podcast feed and get the URL of the latest episode
    feed = podcastparser.parse(feed_data, urllib.request.urlopen(podcast_feed_url))
    return feed

def podcast_meta_string(feed):

    s = ""
    s += f"Podcast Title:{feed['title']}"
    if 'itunes_author' in feed:
        s += f"\nPodcast Owner:{feed['itunes_author']}"
    if 'description' in feed:
        s += f"\nPodcast Description:{feed['description']}"

    return s

def episode_meta_string(episode):

    s = ""
    s += f"Episode Title:{episode['title']}"
    if 'subtitle' in episode:
        s += f"\nEpisode Subtitle:{episode['subtitle']}"
    if 'description' in episode:
        s += f"\nEpisode Description:{episode['description']}"
    if 'published' in episode:
        s += f"\nEpisode Release Date:{dt.datetime.fromtimestamp(episode['published'])}"

    return s

def latest_episode(podcast_feed_url):
    """
    Returns the URL of the mp3 for the last podcast upload.
    """
    # Download the podcast feed and get the XML data as a string
    feed = parse_feed(podcast_feed_url)
    latest_episode_url = feed['episodes'][0]['enclosures'][0]['url']
    try:
        title = feed['episodes'][0]['enclosures'][0]['title']
    except IndexError:
        print(feed['episodes'][0]['enclosures'])

    return latest_episode_url

def get_recent_episodes(feed, n=None):
    # Download the podcast feed and get the XML data as a string
    episodes = feed['episodes']
    if n is not None:
        episodes = episodes[:n]
    episodes_data = []
    for episode in episodes:
        name = episode['title']
        if 'duration' in episode:
            duration = episode['duration']
        else:
            duration = None
        try:
            url = episode['enclosures'][0]['url']
        except IndexError:
            pass # This stupid error only happens with the music podcasts for some reason. It is a cursed error. Stay well away from it.
        episodes_data.append((name, duration, url, episode))

    return episodes_data

def download_episode(episode, filename):
    """
    Downloads and saves the episode from a given episode entity
    """
    print(episode[2])

    data = requests.get(episode[2])
    with open(filename, "wb") as f:
        f.write(data.content)


if __name__ == "__main__":
    feed = parse_feed('https://podcasts.files.bbci.co.uk/p02nq0gn.rss')
    episodes = get_recent_episodes(feed, 1)
    download_episode(episodes[0], "hello.mp3")
