from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_caption(quote):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    )

    completion = client.chat.completions.create(
    extra_body={},
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[
        {
        "role": "user",
        "content": "Generate caption for instagram reel, respond only with one caption, the quote: " + quote,
        }
    ]
    )
    return completion.choices[0].message.content

print(generate_caption("The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt"))