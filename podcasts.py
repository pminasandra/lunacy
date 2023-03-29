
import datetime as dt
import random
import requests
import time
import urllib.request

import podcastparser
import vlc

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

def play_latest_episode(podcast_feed_url):
    # Download the podcast feed and get the XML data as a string
    feed = parse_feed(podcast_feed_url)
    latest_episode_url = feed['episodes'][0]['enclosures'][0]['url']
    title = feed['episodes'][0]['enclosures'][0]['title']

    instance = vlc.Instance('--no-xlib')
    media_player = instance.media_player_new()
    media = vlc.Media(latest_episode_url)
    media_player.set_media(media)
    media_player.play()

    # Wait for the episode to finish playing before exiting the function
    time.sleep(5)
    duration = media_player.get_length()
    print_now_playing(title, duration/1000)
    time.sleep(duration / 1000 + 1)# Create a VLC media player instance and play the latest episode

def print_now_playing(name, duration):
    if duration:
        duration_str = f"{duration // 60}:{duration % 60:02d}"
    else:
        duration_str = "Unknown"
    print("Now Playing:")
    print(f"{name} [{duration_str}]")

def get_recent_episode_urls(podcast_feed_url, n=None):
    # Download the podcast feed and get the XML data as a string
    feed = parse_feed(podcast_feed_url)
    episodes = feed['episodes']
    if n is not None:
        episodes = episodes[:n]
    episode_data = []
    for episode in episodes:
        name = episode['title']
        if 'duration' in episode:
            duration = episode['duration']
        else:
            duration = None
        url = episode['enclosures'][0]['url']
        episode_data.append((name, duration, url))

    return episode_data

def choose_random_episode(data):
    return random.choice(data)

def play_episode(episode):
    print(episode[2])
    instance = vlc.Instance('--no-xlib')
    player = instance.media_player_new()
    media = vlc.Media(episode[2])
    player.set_media(media)
    player.play()
    print_now_playing(episode[0], episode[1])

    time.sleep(5)
    duration = player.get_length()
    time.sleep(duration/1000 + 1)
    player.stop()

if __name__ == "__main__":
#    data = get_recent_episode_urls('https://podcasts.files.bbci.co.uk/p02nq0gn.rss')
#    play_episode(choose_random_episode(data))
#    play_latest_episode('https://stickynotespodcast.libsyn.com/rss')
#    print(get_recent_episode_urls('https://stickynotespodcast.libsyn.com/rss', 20))

    feed = parse_feed('https://podcasts.files.bbci.co.uk/p02nq0gn.rss')
    print(podcast_meta_string(feed))
    print(episode_meta_string(feed['episodes'][0]))
