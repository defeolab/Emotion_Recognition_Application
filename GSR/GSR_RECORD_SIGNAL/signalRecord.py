import sounddevice as sd
import soundfile as sf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as ttk

class Record:
    def __init__(self, sample_rate, sec):
        self.sample_rate = sample_rate
        self.sec = sec
        self.filename = ''
        self.win = None

    # returned recorded sound
    def mysignal(self):
        print(f'Start Recording for {self.sec} seconds')
        signal = sd.rec(frames=int(self.sec * self.sample_rate), samplerate=self.sample_rate, channels=2, blocking = 'False')
        print(f"Recording Ended in {self.sec} seconds !!!")
        return signal

    # save the recorded data
    def savefile(self, filename, signal):
        sf.write(filename, signal, self.sample_rate)
