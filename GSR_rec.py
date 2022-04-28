import queue
import tempfile
import threading
import tkinter as tk
from psychopy import data
import numpy as np
import sounddevice as sd
import soundfile as sf
import os
import time
import json


def file_writing_thread(*, q, **soundfile_args):
    """Write data from queue to file until *None* is received."""
    with sf.SoundFile(**soundfile_args) as f:
        while True:
            cdata = q.get()
            if cdata is None:
                break
            f.write(cdata)


class Record:

    stream = None

    def __init__(self, id, exp_type, type):
        self.input_overflows = 0
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.thread = None
        self.thread1 = None
        self.thread2 = None
        self.device = 'Microsoft Sound Mapper - Input'
        self.filename = None
        self.name = None
        self.flag = True
        self.type = type

        fp = open('ffmpeg.txt', 'r')
        data_file = json.load(fp)
        fp.close()
        fp1 = open('websites.txt', 'r')
        data_file1 = json.load(fp1)
        fp1.close()

        self.input_device = data_file['gsr']
        self.sample_rate = data_file['samplingrate']
        self.seconds = data_file1['duration']
        self.channels = data_file['channels']
        (h, m, s) = self.seconds.split(':')
        self.result = int(h) * 3600 + int(m) * 60 + int(s)
        #print(result)

        self.ParticipantID = id
        self.exp_type = exp_type
    def create_stream(self,):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(samplerate=self.sample_rate, device=self.input_device, channels=self.channels,
                                     callback=self.audio_callback)
        self.stream.start()

    def handler(self, seconds):
        for i in range(seconds+1):
            time.sleep(1)
        self.flag = False
        self.stream.close()

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status.input_overflow:
            self.input_overflows += 1.
        if self.recording:
            self.audio_q.put(indata.copy())
            self.previously_recording = True
        else:
            if self.previously_recording:
                self.audio_q.put(None)
                self.previously_recording = False

    def on_rec(self):
        self.recording = True
        if self.exp_type == 1:
            self.filename = "data/Image/" + str(self.ParticipantID) + "/" + str(self.ParticipantID) + "_GSR1_rec.wav"
            file_path = "data/Image/" + str(self.ParticipantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(self.filename):
                    print("file removed")
                    os.remove(self.filename)
                else:
                    print("No file exist")
        elif self.exp_type == 2:
            self.filename = "data/Video/" + str(self.ParticipantID) + "/" + str(self.ParticipantID) + "_GSR1_rec.wav"
            file_path = "data/Video/" + str(self.ParticipantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(self.filename):
                    print("file removed")
                    os.remove(self.filename)
                else:
                    print("No file exist")

        elif self.exp_type == 3:
            if self.type == 1:
                self.filename = "data/Browser/" + str(self.ParticipantID) + "/" + str(self.ParticipantID) + "_GSR1_web1_rec.wav"
                file_path = "data/Browser/" + str(self.ParticipantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(self.filename):
                        print("file removed")
                        os.remove(self.filename)
                    else:
                        print("No file exist")
            elif self.type == 2:
                self.filename = "data/Browser/" + str(self.ParticipantID) + "/" + str(
                    self.ParticipantID) + "_GSR1_web2_rec.wav"
                file_path = "data/Browser/" + str(self.ParticipantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(self.filename):
                        print("file removed")
                        os.remove(self.filename)
                    else:
                        print("No file exist")
            elif self.type == 3:
                self.filename = "data/Browser/" + str(self.ParticipantID) + "/" + str(
                    self.ParticipantID) + "_GSR1_web3_rec.wav"
                file_path = "data/Browser/" + str(self.ParticipantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(self.filename):
                        print("file removed")
                        os.remove(self.filename)
                    else:
                        print("No file exist")
            elif self.type == 4:
                self.filename = "data/Browser/" + str(self.ParticipantID) + "/" + str(
                    self.ParticipantID) + "_GSR1_web4_rec.wav"
                file_path = "data/Browser/" + str(self.ParticipantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(self.filename):
                        print("file removed")
                        os.remove(self.filename)
                    else:
                        print("No file exist")
            else:
                print("no experiment")
        else:
            print("ID is undefined!")
        self.thread1 = threading.Thread(target=self.create_stream, args=(), daemon=True)
        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=file_writing_thread,
            kwargs=dict(
                file=self.filename,
                mode='x',
                samplerate=self.sample_rate,
                channels=self.channels,
                q=self.audio_q,
            ), daemon=True,
        )
        self.thread2 = threading.Thread(target=self.handler, args=(self.result,), )
        self.thread.start()
        self.thread1.start()
        self.thread2.start()

    def on_stop(self, *args):
        self.recording = False
        self.stream.close()
        self.name = self.filename
        if self.thread.is_alive():
            return self.name
        self.thread.join()
        self.thread1.join()
        self.thread2.join()

