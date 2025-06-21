import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import io

load_dotenv()

def generate_audio(quote):
  elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
  )

  audio = elevenlabs.text_to_speech.convert(
      text=quote,
      voice_id="kqVT88a5QfII1HNAEPTJ",
      model_id="eleven_multilingual_v2",
      output_format="mp3_44100_128",
  )

  # Join audio chunks into a single binary
  audio_binary = b"".join(audio)
  
  # Convert audio bytes to AudioSegment
  audio_segment = AudioSegment.from_file(io.BytesIO(audio_binary), format="mp3")
  
  # Create 0.5 second silence
  silence = AudioSegment.silent(duration=850)  # 500 milliseconds = 0.5 seconds
  
  # Add silence to beginning and end
  audio_with_silence = silence + audio_segment + silence
  
  # Export to file
  audio_with_silence.export("quote.mp3", format="mp3")
