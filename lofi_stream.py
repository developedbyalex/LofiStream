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

# Get a random audio file from the folder
def get_random_audio_file():
    audio_files = os.listdir(audio_folder)
    return os.path.join(audio_folder, random.choice(audio_files))


# Get the duration of an audio file using FFmpeg
def get_audio_duration(audio_file):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            audio_file,
        ],
        capture_output=True,
        text=True,
    )
    duration = float(result.stdout)
    return duration


# Start the streaming process
def start_streaming(audio_file):
    # Create a subprocess object for FFmpeg
    ffmpeg_process = subprocess.Popen(
        [
            "ffmpeg",
            "-re",
            "-ignore_loop",
            "0",
            "-i",
            background_image,
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
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )  # Suppress FFmpeg output

    # Get the duration of the audio track
    audio_duration = get_audio_duration(audio_file)

    # Sleep for the duration of the audio track
    time.sleep(audio_duration)

    # Terminate the FFmpeg process
    ffmpeg_process.terminate()
    ffmpeg_process.wait()  # Wait for the process to finish


# Select audio files and start streaming
def audio_track_selection():
    while True:
        current_audio_file = get_random_audio_file()

        # Start the streaming process in a separate thread
        streaming_thread = threading.Thread(
            target=start_streaming, args=(current_audio_file,)
        )
        streaming_thread.start()

        # Sleep for a short time before starting the next track
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
