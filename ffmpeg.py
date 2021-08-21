"""
Using ffmpeg to capture video and audio
"""

import io
import os
import tkinter
from tkinter import *
import keyboard
import sys
import threading
import subprocess

import win32process


#def extract_audio():
#    cmd = ('ffmpeg -f dshow -t 00:00:15 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" '
#           '-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
#           '-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')
#    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #os.system('ffmpeg -f dshow -t 00:00:15 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" '
    #       '-vcodec libx264 -r 10 -vb 512k -s 640x360 video_output.mp4 '
    #       '-acodec libmp3lame -ab 128k -ac 2 -ar 44100 audio_output.wav')
    #if keyboard.is_pressed('q'):
    #    print('VIDEO ABOUT TO BE STOPPED')
    #    subprocess.Popen.kill(process)


#if __name__ == "__main__":
#    print('Recording')
#    extract_audio()
    #thread = threading.Thread(target=extract_audio, )
    #thread.start()
#    extract_audio()
    #
#    while True:
#        if keyboard.is_pressed('q'):
#            print('VIDEO ABOUT TO BE STOPPED')
    #    subprocess.Popen.kill(process)

    #        thread.join()
    #        if thread.is_alive():
    #            print('still recording')
    #            thread.join()
#            break
#    print('VIDEO RECORDING STOPPED')
#    sys.exit()

#q
#ffmpeg -list_devices true -f dshow -i dummy

import subprocess
import time
global proc
import signal

#class recording:
#    def rec(self):

def start():
    cmd = ('ffmpeg -f dshow -t 00:00:10 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" out.MP4 ')
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)

        #self.cmd = ('ffmpeg -f dshow -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" out.MP4 ')
        #self.proc = subprocess.Popen(self.cmd, shell=True, stderr=subprocess.STDOUT)
#time.sleep(5) # <-- sleep for 12''

def stop():
    os.system('TaskKill /im ffmpeg.exe /F')
        #os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        #self.proc.kill() # <-- terminate the process



#if __name__ == "__main__":
   #a = recording.rec
#   top = Tk()
   #top.title("Anagraphic data")
   #top.geometry("500x500")

   #start = Button(top, text="start", command=start)
   #start.grid(row=1, column=1, padx=10, pady=20)

   #stop = Button(top, text="stop", command=stop)
   #stop.grid(row=2, column=1, padx=10, pady=20)

   #top.mainloop()

   #cmd = ('ffmpeg -y -f dshow -t 00:00:10 -i video="Integrated Webcam":audio="Microphone Array (Realtek Audio)" out.MP4 ')
   #proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)
   #time.sleep(4)
   #os.system('TaskKill /im ffmpeg.exe /F')
   #os.kill(proc.pid, signal.SIGTERM)
   #sys.exit()

