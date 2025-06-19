import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

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

  with open("quote.mp3", "wb") as f:
    f.write(b"".join(audio))
