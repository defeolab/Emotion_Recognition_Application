import sounddevice as sd
import soundfile as sf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as ttk

class Record:
    def __init__(self, sample_rate, sec, win):
        self.sample_rate = sample_rate
        self.sec = sec
        self.win = win
        self.filename = ''

    # returned recorded sound
    def mysignal(self):
        print(f'Start Recording for {self.sec} seconds')
        signal = sd.rec(frames=int(self.sec * self.sample_rate), samplerate=self.sample_rate, channels=2, blocking = 'True')
        print(f"Recording Ended in {self.sec} seconds !!!")
        return signal

    # playback recorded data
    def playback(self, signal):
        win1 = ttk.Tk()
        win1.title("GSR Data")

        fig1 = Figure(figsize=(5, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(signal)
        ax1.set_title('RECORDED SIGNAL')
        ax1.set_xlabel('Time(s)')
        ax1.set_ylabel('Amplitude(Hz)')

        canvas1 = FigureCanvasTkAgg(fig1, win1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=ttk.LEFT)

    # save the recorded data
    def savefile(self, filename, signal):
        sf.write(filename, signal, self.sample_rate)
        return
