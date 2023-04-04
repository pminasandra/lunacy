import os.path

import gtts

import config

def generate_voice_saying(text, filename, tld=config.TTS_TLD):
    """
    Generates an mp3 file saying the contents of 'text', but takes some time.
    """

    gttsobj = gtts.tts.gTTS(text, tld=tld)
    gttsobj.save(os.path.join(filename))

if __name__ == "__main__":
    generate_voice_saying("This is a public service announcement. Baba Saitaandas is watching. Thank you.", "clip.mp3")
