from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip
from pydub import AudioSegment
import os

def make_reel(quote_text):
    # Load background image or video
    if os.path.splitext("background.jpg")[1].lower() in ['.jpg', '.png', '.jpeg']:
        bg = ImageClip("background.jpg")
    else:
        bg = VideoFileClip("background.jpg").subclip(0, 10)

    # Load and mix voiceover with background music
    voice = AudioSegment.from_file("quote.mp3")
    bgm = AudioSegment.from_file("music.mp3").apply_gain(-10)
    combined = bgm.overlay(voice)

    # Match combined duration to voice duration
    voice_ms = len(voice)
    if len(combined) < voice_ms:
        combined += AudioSegment.silent(duration=voice_ms - len(combined))
    else:
        combined = combined[:voice_ms]
    combined.export("final_audio.mp3", format="mp3")

    # Load final audio into MoviePy
    final_audio = AudioFileClip("final_audio.mp3")
    print(f"Audio duration: {final_audio.duration}s")  # Debug

    # Resize and duration for background
    bg = bg.set_duration(final_audio.duration)
    bg = bg.resize((1080, 1920))

    # Create text overlay
    txt_clip = TextClip(
        quote_text,
        fontsize=70,
        font="Arial-Bold",
        color="white",
        method='caption',
        size=(1000, None)
    ).set_position('center').set_duration(final_audio.duration)

    # Composite video and text, attach audio to final clip
    final = CompositeVideoClip(
        [bg, txt_clip],
        size=(1080, 1920)
    ).set_audio(final_audio)  # Set audio only once on the final composite
    # Verify audio exists
    if final.audio is None:
        print("Warning: final clip has no audio attached.")

    # Export ensuring audio is included
    final.write_videofile(
        "reel.mp4",
        fps=30,
        codec='libx264',
        audio_codec='aac',
        audio=True,
        threads=4
    )
