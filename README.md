# Lunacy: a personalised radio channel (alpha)

Lunacy is a hobby-project to listen to my favourite podcasts in a different way.
Lunacy takes a list of podcast RSS feeds and transforms it into a daily radio channel, complete with
anchors and continuity announcers powered by OpenAI's Large Language Models.

## Personal project
While this is largely meant for my own sake, to learn as well as enjoy audio content better, I want to
try to make this a generally usable bit of code so that you can listen to your own podcasts in the same
way.

I also decided to try to use ChatGPT to help write the code to see how it compares to usual coding standards.
The answer: if you care about style and readability, abysmal.
If you are an experienced programmer *and* like to stick to your programming principles, using AI services for coding seems 
to actively slow down things rather than speed it up.
However, it is undeniable that the software lets you know things you didn't know before, and you get access to (often wrong, but) helpful
code skeletons that you can rely on for your own purposes?

# Dependencies
This project depends on the python modules, which can all be `pip` installed:

- requests
- gtts
- openai
- pandas
- podcastparser
- pydub

Note also that this code uses `glob`, a python in-built, which restricts its use only to linux (and maybe mac?).
Since this is meant to run on something like a raspberry pi like an alarm clock every morning, it's totally fine for this to happen.
Others are welcome to make it more OS-agnostic if they should choose.

## OpenAI registration
You need an OpenAI paid subscription for this to work, since the free quota doesn't cover the amount of text needed for a radio presenter, unfortunately.
Register with them on [their website](https://openai.com/pricing), obtain your API key, and put it in your `.bashrc` as follows:

```
export OPENAI_API_KEY="your-huge-api-key-will-go-here"
```

Also set up a price limit on their website so that you don't end up with a huge bill!

# Installation and setting up

First clone this repository as follows:

```
https://github.com/pminasandra/lunacy
```

In `config.py`, make sure the `RESOURCE_DIR`, `TEMP_DIR`, and `OWNER_NAME` variables are appropriately set.
`<RESOURCE_DIR>` is a directory containing the podcast list, music files for generating continuity announcements, etc.
In `<TEMP_DIR>`, the code will create a directory called `current/`, which will contain all the mp3 files in order that need to be played for the audio to work.
Note that the code works properly as is.

To customise, edit `<RESOURCE_DIR>/podcast.csv` so that it has all the podcasts of your choice.
`config.CATEGORY_ORDER` is the order of categories for which podcast episodes will be played.
When news podcasts are played, the most recent episode is always selected.

You might want to use `cron` or `systemmd` to make sure that `main.py` is always executed a few hours before the radio needs to be played.
Then, `<TEMP_DIR>/current` contains all the files that, when played in order, will sound like the radio show.
You can use `cvlc <TEMP_DIR>/current` to listen to your content.

# Issues

Since this is the alpha release, there are bound to be thousands of bugs.
Please feel free to write to me if you have great bugfixes or ideas.
