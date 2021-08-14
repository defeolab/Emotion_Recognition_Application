
"""
         Use python to achieve: read the picture of the USB camera
"""
# Import CV2 module
import threading

import cv2
import os
import json
import datetime
import tkinter as tk
from tkinter import *
import time
#from threading import *

class Recording:
    def __init__(self, id):
        self.PatientId = id
        self.root = tk.Tk()
        #self.root.title("Recording")
        self.root.geometry("300x300")
        start_recording = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        start_recording.grid(row=1, column=1)

    def start_recording(self):
        cam_start = threading.Thread(target=self.Cam_Aud_Recording)
        cam_start.start()

        sc_start = threading.Thread(target=self.screen_record)
        sc_start.start()

    def Cam_Aud_Recording(self):
        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()

        audio = mic['mic']
        video = mic['video']
    #cmd = ('ffmpeg -f dshow -t 00:00:15 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" '
           #'-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
           #'-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')
    #process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        os.system(f'ffmpeg -f dshow -t 00:00:15 -i video="{video}":audio="{audio}" '
           '-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
           '-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')

    def screen_record(self):
    #fld = "C:\\Users\\zeel9\\PycharmProjects\\Emotion_Recognition_Application - v3\\output\\output"
        filename =  "output.mp4"
        video_size = "2560x1440"
    #os.system("""ffmpeg -f dshow -t 00:00:15 -i video="screen-capture-recorder" -video_size {video_size} output.mp4""")
    #os.system("""ffmpeg -f gdigrab -t 00:00:15 -i desktop -video_size 2560x1440 -offset_x 2560 -offset_y 0 output.mp4""")

    #os.system(f"""ffmpeg -f dshow -t 00:00:15 -i video="screen-capture-recorder" -offset_x 1440 -offset_y 0 -video_size 2560x1440 -framerate 25 out.mp4""")
        os.system("""ffmpeg -f gdigrab -t 00:00:15 -framerate 6 -offset_x 10 -offset_y 20 -video_size vga -i desktop out.mp4""")
        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()

        audio = mic['gsr']

    #os.system(f"""ffmpeg -y -rtbufsize 200M -f dshow -i video="screen-capture-recorder" -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)
    #os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

    #os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

#screen_record()