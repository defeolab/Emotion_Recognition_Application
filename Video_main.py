
"""
         Use python to achieve: read the picture of the USB camera
"""
# Import CV2 module
import cv2
import os
import json
import datetime
import tkinter as tk
import time
#from threading import *
import threading

class VideoRecording:
    def __init__(self, id):
        self.patientId = id
        os.system("start cmd_.vbe")  # Start recording
        #time.sleep(1)
        t1 = threading.Thread(target=screen_record)

        t3 = threading.Thread(target=read_usb_capture)
        # time.sleep(1)
        t1.start()
        #time.sleep(1)
        # screen_record()
        t3.start()

        #read_usb_capture()  # Start camera
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Current time
        os.system("ffmpeg -i temp.mp4 -i temp.wav -strict -2 -f mp4 " + name + ".mp4")  # Use ffmpe to merge
        print(name)
        # os.remove('temp.mp4') # Delete the intermediate video file
        # os.remove("temp.wav") # Delete intermediate audio files

x= 0

def screen_record():
    #fld = "C:\\Users\\zeel9\\PycharmProjects\\Emotion_Recognition_Application - v3\\output\\output"
    #fld = "C:\\Users\\zeel9\\PycharmProjects\\ffmpeg - v1\\output\\output"
    filename =  "output.mp4"
    #audio = "Microphone Array (Realtek Audio)"
    video_size = "2366x1300"
    #os.system("""ffmpeg -f dshow -t 00:00:15 -i video="screen-capture-recorder" output.mp4""")

    fp = open('ffmpeg.txt', 'r')
    mic = json.load(fp)
    fp.close()

    audio = mic['gsr']

    #os.system(f"""ffmpeg -y -rtbufsize 200M -f dshow -i video="screen-capture-recorder" -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)
    os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

    #os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)


def read_usb_capture():
    # Select the number of the camera
    cap = cv2.VideoCapture(0)
    # Add this sentence is a pop-up window that can be dragged with the mouse
    cv2.namedWindow('real_img', cv2.WINDOW_NORMAL)

    # .mp4 format, 25 is FPS frame rate, (640,480) is size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp.mp4', fourcc, 25, (640, 480))

    while(cap.isOpened()):
        # Read the picture of the camera
        ret, frame = cap.read()

        # Perform write operation
        out.write(frame)
        # Real picture
        cv2.imshow('real_img', frame)
        # Press'esc' to exit
        if cv2.waitKey(1) & 0xFF == 27:
            break
    # Release screen
    cap.release()
    cv2.destroyAllWindows()

#if __name__ == '__main__':
#    os.system("start cmd_.vbe") #Start recording
#    read_usb_capture() # Start camera
#    name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Current time
#    os.system("ffmpeg -i temp.mp4 -i temp.wav -strict -2 -f mp4 " + name + ".mp4")  # Use ffmpe to merge
#    print(name)
    #os.remove('temp.mp4') # Delete the intermediate video file
    #os.remove("temp.wav") # Delete intermediate audio files

#t1= VideoRecording(1223)
#screen_record()