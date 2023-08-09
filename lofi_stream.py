import os
import random
import subprocess
import threading
import time
import art
import json
from colorama import Fore, Style

# Display ASCII art title
print(Fore.CYAN + art.text2art("LofiStream") + Style.RESET_ALL)

# Check if the config file exists and load stream information if available
config_file = "lofi_config.json"
stream_info = {}

if os.path.exists(config_file):
    with open(config_file, "r") as f:
        stream_info = json.load(f)

# Ask for user input or use stored information
audio_folder = input(
    Fore.YELLOW + "Enter the path to your audio folder: " + Style.RESET_ALL
)
background_image = input(
    Fore.YELLOW
    + "Enter the path to your background image (jpg, png, or gif): "
    + Style.RESET_ALL
)

stream_url = stream_info.get(
    "stream_url",
    input(Fore.YELLOW + "Enter your YouTube Live stream URL: " + Style.RESET_ALL),
)
stream_key = stream_info.get(
    "stream_key", input(Fore.YELLOW + "Enter your stream key: " + Style.RESET_ALL)
)

# Save the stream information to the config file
stream_info["stream_url"] = stream_url
stream_info["stream_key"] = stream_key

with open(config_file, "w") as f:
    json.dump(stream_info, f)

# Get a list of audio files from the folder
audio_files = [os.path.join(audio_folder, file) for file in os.listdir(audio_folder) if file.endswith(".mp3")]

# Start the streaming process
def start_streaming(audio_file):
    while True:
        # Create a subprocess object for FFmpeg
        ffmpeg_process = subprocess.Popen(
            [
                "ffmpeg",
                "-re",
                "-i",
                background_image,
                "-stream_loop",
                "-1",  # Loop indefinitely
                "-i",
                audio_file,
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-pix_fmt",
                "yuv420p",
                "-g",
                "60",
                "-f",
                "flv",
                stream_url + "/" + stream_key,
            ],
            stdin=subprocess.PIPE,  # Close stdin
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )  # Suppress FFmpeg output

        # Wait for the FFmpeg process to complete
        ffmpeg_process.wait()

# Select audio files and start streaming in a loop
def audio_track_selection():
    while True:
        for audio_file in audio_files:
            start_streaming(audio_file)
            time.sleep(5)  # Adjust as needed

# Main program loop
def main():
    start_time = time.time()

    # Start audio track selection in a separate thread
    audio_track_thread = threading.Thread(target=audio_track_selection)
    audio_track_thread.start()

    try:
        while True:
            elapsed_time = int(time.time() - start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            print(
                Fore.GREEN
                + f"Stream is online - Elapsed Time: {hours:02d}:{minutes:02d}:{seconds:02d}"
                + Style.RESET_ALL,
                end="\r",
            )
            time.sleep(1)  # Update every second
    except KeyboardInterrupt:
        pass

    # Stop the audio track selection thread
    audio_track_thread.join()

# Run the main program
if __name__ == "__main__":
    main()
