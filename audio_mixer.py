import glob
import os.path

from pydub import AudioSegment as AS

import config

target_dir = os.path.join(config.TEMP_DIR, "current")

def overlay_audios(aud1, aud2, interval, aud_out=None, gain_during_overlay=3):
    audio1 = AS.from_mp3(aud1)
    audio2 = AS.from_mp3(aud2)

    available_overlay_time = len(audio1) - interval
    if available_overlay_time < len(audio2):
        silence = AS.silent(len(audio2) - available_overlay_time)
        print(f"Available overlay time was {available_overlay_time}, Silence of {len(silence)}")
        audio1 = audio1.append(silence, crossfade=0)
    audio1 = audio1.overlay(audio2, position=interval, gain_during_overlay=gain_during_overlay)
    if aud_out is None:
        aud_out = aud1
    audio1.export(aud_out, format="mp3")

def musicify_intro():
    intro = os.path.join(config.TEMP_DIR, "current", "000.mp3")
    music = os.path.join(config.RESOURCE_DIR, "lead-in_29.mp3")
    assert os.path.exists(intro)
    assert os.path.exists(music)
    
    overlay_audios(music, intro, config.AUDIO_LEAD_IN_INTERVAL, aud_out=intro)

def musicify_continuity(filename):
    music = os.path.join(config.RESOURCE_DIR, "continuity_12.mp3")
    assert os.path.exists(filename)
    assert os.path.exists(music)
    
    overlay_audios(music, filename, config.AUDIO_CONTINUITY_INTERVAL, aud_out=filename)

def musicify_all_continuity():
    files = glob.glob(os.path.join(config.TEMP_DIR, "current", "*a.mp3"))
    for file_ in files:
        musicify_continuity(file_)

if __name__ == "__main__":
    musicify_intro()
    musicify_all_continuity()
