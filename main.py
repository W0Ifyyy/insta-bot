from generate_quote import get_quote
from tts import generate_audio
from make_reel import make_reel
from generate_caption import generate_caption
from publish import publish_to_instagram
def main():
    quoteData = get_quote()
    print("Quote subscratted!: " + quoteData['quote'] + " - " + quoteData['author'] + ".....");
    generate_audio(quoteData['quote']);
    print("Audio generated successfully.....");
    make_reel(quoteData['quote'] + " - " + quoteData['author']);
    print("Reel generated successfully.....");
    caption = generate_caption(quoteData['quote']);
    print("Caption generated successfully: " + caption);
    publish_to_instagram("reel.mp4", caption);
    print("Reel published successfully.....");
    
main();