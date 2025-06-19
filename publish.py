import os
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

def publish_to_instagram(video_path, caption):
    try:
        cl = Client()
        cl.login(USERNAME, PASSWORD)

        cl.clip_upload(
            path=video_path,
            caption=caption,
        )

        print("✔️ reel published successfully!")
    except Exception as e:
        print(f"❌ publish error: {e}")
