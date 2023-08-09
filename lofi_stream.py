import os
import random
import subprocess
import threading

# Replace with the path to your audio folder and background image
audio_folder = r"AUDIO_FOLDER_HERE"
background_image = r"BACKGROUND_IMG_HERE" #Supports .gif

# Replace with your own YouTube Live stream URL and stream key
stream_url = 'rtmp://a.rtmp.youtube.com/live2'
stream_key = 'STREAM_KEY_HERE'

# Get a random audio file from the folder
def get_random_audio_file():
    audio_files = os.listdir(audio_folder)
    return os.path.join(audio_folder, random.choice(audio_files))

# Start the streaming process
def start_streaming(audio_file):
    # Run FFmpeg subprocess to handle the video streaming with the provided audio file
    subprocess.call([
        'ffmpeg',
        '-re',
        '-ignore_loop', '0',  # Add this option to respect the GIF loop count
        '-i', background_image,
        '-i', audio_file,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-pix_fmt', 'yuv420p',
        '-f', 'flv',
        stream_url + '/' + stream_key
    ])

# Select audio files and start streaming
def audio_track_selection():
    while True:
        current_audio_file = get_random_audio_file()

        # Start the streaming process in a separate thread
        streaming_thread = threading.Thread(target=start_streaming, args=(current_audio_file,))
        streaming_thread.start()

        # Wait for the streaming thread to finish
        streaming_thread.join()

# Main program loop
def main():
    # Start audio track selection in a separate thread
    audio_track_thread = threading.Thread(target=audio_track_selection)
    audio_track_thread.start()

    # Keep the program running until interrupted
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    # Stop the audio track selection thread
    audio_track_thread.join()

# Run the main program
if __name__ == '__main__':
    main()
