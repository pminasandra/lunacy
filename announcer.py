
import os

import openai

import podcasts

api_key = os.getenv("OPENAI_API_KEY")
feed = podcasts.parse_feed("https://podcasts.files.bbci.co.uk/b006qykl.rss")
episode = feed['episodes'][0]

PROMPT_STRING = """
I have set up a personalised radio system where randomly selected podcast episodes will be played in sequence.
Your task is to act as a continuity announcer, and briefly and concisely introduce upcoming episodes with some information about the podcast and its host.
You don't need to include ALL the details, just choose what you think is most important.
I definitely need you to mention the date and year the episode we are playing was aired in.
Here are the details:

%pod_det%
%ep_det%

CONTINUITY ANNOUNCEMENT:
"""

INTRO_STRING = """
You are a radio announcer named Luna for a morning radio show named "Lunacy, the personal radio broadcast for Pranav Minasandra".
You will be given today's schedule, which will consist of 1 news episode, 1 music piece, and 1 episode focussing on either science or history.
These episodes might occur in a different order to that listed above, and the order will be specified in the details.
You might or might not be given additional information.
Mentioning today's date as the date given in the details, and incorporating all details given, present a cheerful introduction to today's show.

DETAILS:
%details%
%extra_details%

INTRODUCTION TO RADIO SHOW:
"""

def generate_announcement(feed, episode):
    openai.api_key = os.environ["OPENAI_API_KEY"] # replace with your OpenAI API key
    prompt = PROMPT_STRING
    prompt = prompt.replace("%pod_det%", podcasts.podcast_meta_string(feed))
    prompt = prompt.replace("%ep_det%", podcasts.episode_meta_string(episode))

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=1024,
      n=1,
      stop=None,
      timeout=60,
      )

    return response.choices[0].text.strip()

def generate_intro(date="default", extra_details=None):
    if date == "default":
        import datetime as dt
        date = dt.datetime.today()

        days = ["Modayn", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = days[date.weekday()]

    openai.api_key = os.environ["OPENAI_API_KEY"] # replace with your OpenAI API key
    prompt = INTRO_STRING
    prompt = prompt.replace("%details%", f"Date: {date}\nDay: {day}")
    if extra_details is not None:
        prompt = prompt.replace("%extra_details%", extra_details)

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      temperature=0.5,
      max_tokens=1024,
      n=1,
      stop=None,
      timeout=60,
      )

    return response.choices[0].text.strip()

#print(generate_announcement(feed, episode))
if __name__ == "__main__":
    print(generate_intro())
    while True:
        url = input("Give podcast URL: ")
        feed = podcasts.parse_feed(url)
        num = int(input("Give episode number: "))
        episode = feed['episodes'][num]

        print(generate_announcement(feed, episode), '\n')
