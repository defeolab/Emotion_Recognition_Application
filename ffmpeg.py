"""
Using ffmpeg to capture video and audio
"""

import io
import os
import keyboard
import sys
import threading
import subprocess


def extract_audio():
    cmd = ('ffmpeg -f dshow -t 00:00:15 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" '
           '-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
           '-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #os.system('ffmpeg -f dshow -t 00:00:15 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" '
    #       '-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
    #       '-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')

if __name__ == "__main__":
    print('Recording')
    extract_audio()
    #thread = threading.Thread(target=extract_audio, )
    #thread.start()
    extract_audio()
    while True:
        if keyboard.is_pressed('q'):
            print('VIDEO ABOUT TO BE STOPPED')
    #        thread.join()
    #        if thread.is_alive():
    #            print('still recording')
    #            thread.join()
            break
    print('VIDEO RECORDING STOPPED')
    sys.exit()

#q
#ffmpeg -list_devices true -f dshow -i dummy


