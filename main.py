from generate_quote import get_quote
from tts import generate_audio
from make_reel import make_reel
from generate_caption import generate_caption
from publish import publish_to_instagram
import os
import random
import tkinter as tk
from tkinter import filedialog, ttk
import threading


def main():

    def process_with_gui():
        # Create main window
        root = tk.Tk()
        root.title("Instagram Reel Generator")
        root.geometry("445x280")
        root.resizable(False, False)
        # Create frame for inputs
        frame = ttk.Frame(root, padding="10")

        # Add informational text about random selections
        info_label = ttk.Label(root, text="If background, music, quote or author are not selected, random ones will be used.", foreground="blue", padding=5)
        info_label.pack(fill=tk.X)

        # Add .env file requirement info
        env_info_label = ttk.Label(root, text="Remember to fill the .env file with your Instagram username, password, \nElevenLabs API key, and OpenRouter API key before using. \n(IG_USERNAME, IG_PASSWORD, ELEVENLABS_API_KEY, OPENROUTER_API_KEY)", foreground="red", padding=5)
        env_info_label.pack(fill=tk.X)

        # Pack the frame after the info label
        frame.pack(fill=tk.BOTH, expand=True)

        # Background selection
        bg_var = tk.StringVar()
        ttk.Label(frame, text="Background:").grid(column=0, row=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=bg_var, width=40).grid(column=1, row=0, pady=5)
        ttk.Button(frame, text="Browse...",
                command=lambda: bg_var.set(filedialog.askopenfilename(
                    initialdir="./assets/bgs/",
                    filetypes=[("Image/Video files", "*.jpg *.jpeg *.png *.mp4")]))).grid(column=2, row=0, pady=5)

        # Music selection
        music_var = tk.StringVar()
        ttk.Label(frame, text="Music:").grid(column=0, row=1, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=music_var, width=40).grid(column=1, row=1, pady=5)
        ttk.Button(frame, text="Browse...",
                command=lambda: music_var.set(filedialog.askopenfilename(
                    initialdir="./assets/music/",
                    filetypes=[("Audio files", "*.mp3 *.wav")]))).grid(column=2, row=1, pady=5)

        # Quote input
        quote_var = tk.StringVar()
        ttk.Label(frame, text="Quote:").grid(column=0, row=2, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=quote_var, width=40).grid(column=1, row=2, columnspan=2, pady=5, sticky="w")

        # Author input
        author_var = tk.StringVar()
        ttk.Label(frame, text="Author:").grid(column=0, row=3, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=author_var, width=40).grid(column=1, row=3, columnspan=2, pady=5, sticky="w")

        # Start button
        def on_start():
            bg = bg_var.get() if bg_var.get() else None
            music = music_var.get() if music_var.get() else None
            quote = quote_var.get()
            author = author_var.get()

            def process():
                if quote and author:
                    quoteData = {'quote': quote, 'author': author}
                    print(f"Using custom quote: {quote} - {author}")
                else:
                    quoteData = get_quote()
                    print(f"Quote retrieved: {quoteData['quote']} - {quoteData['author']}")

                generate_audio(quoteData['quote'])
                print("Audio generated successfully...")

                selected_bg = bg
                selected_music = music

                if not selected_bg:
                    bg_folder = "./assets/bgs/"
                    bg_files = [os.path.join(bg_folder, f) for f in os.listdir(bg_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.mp4'))]
                    selected_bg = random.choice(bg_files)

                if not selected_music:
                    music_folder = "./assets/music/"
                    music_files = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
                    selected_music = random.choice(music_files)

                make_reel(quoteData['quote'] + " - " + quoteData['author'], background=selected_bg, music=selected_music)
                print("Reel generated successfully...")

                # Generate caption and publish (from original main function)
                caption = generate_caption(quoteData['quote'])
                print("Caption generated successfully: " + caption)
                publish_to_instagram("reel.mp4", caption)
                print("Reel published successfully...")

            threading.Thread(target=process, daemon=True).start()

        ttk.Button(frame, text="Start", command=on_start).grid(column=1, row=4, pady=20)

        root.mainloop()

    # Run the GUI
    process_with_gui()

# Start the application
main()
