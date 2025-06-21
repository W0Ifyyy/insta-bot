from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ImageClip
from pydub import AudioSegment
import os

def make_reel(quote_text, background="./assets/bgs/bg.mp4", music="./assets/music/music.mp3"):

    # Load and mix voiceover with background music
    voice = AudioSegment.from_file("quote.mp3")
    bgm = AudioSegment.from_file(music).apply_gain(-10)
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

    if not os.path.exists(background):
        raise FileNotFoundError(f"Background file not found: {background}")


    if os.path.splitext(background)[1].lower() in ['.jpg', '.png', '.jpeg']:
        bg = ImageClip(background)
    else:
        bg = VideoFileClip(background).subclip(0, final_audio.duration)

    # Set duration for background
    bg = bg.set_duration(final_audio.duration)

    # Resize and crop background to 1080x1920 (portrait orientation)
    target_width = 1080
    target_height = 1920

    # Calculate which dimension to resize to ensure complete filling
    width_ratio = target_width / bg.size[0]
    height_ratio = target_height / bg.size[1]
    resize_ratio = max(width_ratio, height_ratio)

    # Resize while maintaining aspect ratio
    new_width = int(bg.size[0] * resize_ratio)
    new_height = int(bg.size[1] * resize_ratio)
    bg = bg.resize((new_width, new_height))

    # Now crop to exact dimensions (centered)
    x_center = new_width / 2
    y_center = new_height / 2
    bg = bg.crop(
        x_center=x_center,
        y_center=y_center,
        width=target_width,
        height=target_height
    )

    # Create shadow text (slightly offset and darker)
    shadow_clip = TextClip(
        quote_text,
        fontsize=70,
        font="Arial-Bold",
        color="black",
        method='caption',
        size=(1000, None)
    ).set_position(('center', 'center')).set_duration(final_audio.duration).margin(left=3, top=3, opacity=0)

    # Create text overlay
    txt_clip = TextClip(
        quote_text,
        fontsize=70,
        font="Arial-Bold",
        color="white",
        method='caption',
        size=(1000, None)
    ).set_position(('center', 'center')).set_duration(final_audio.duration)

    # Combine shadow and text into one clip, then center the whole thing
    text_with_shadow = CompositeVideoClip([shadow_clip, txt_clip], size=(1080, 1920)).set_duration(final_audio.duration)

    # Center text within the full canvas
    text_with_shadow = text_with_shadow.set_position('center')


    # Composite video and text, attach audio to final clip
    final = CompositeVideoClip(
        [bg, text_with_shadow],
        size=(1080, 1920)
    ).set_audio(final_audio)  # Set audio only once on the final composite
    # Verify audio exists
    if final.audio is None:
        print("Warning: final clip has no audio attached.")

    # Export ensuring audio is included
    final.write_videofile(
        "reel.mp4",
        fps=60,
        codec='libx264',
        audio_codec='aac',
        audio=True,
        threads=4
    )
