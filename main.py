
import announcer
import audio_mixer
import config
import podcasts
import scheduler


schedule = scheduler.fill_schedule()
scheduler.download_schedule_materials(schedule)
scheduler.save_announcer_voices(schedule)

if not config.SUPPRESS_AUDIO_MIXING:
    audio_mixer.musicify_intro()
    audio_mixer.musicify_all_continuity()
