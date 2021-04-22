import sounddevice as sd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fft2
from psychopy import visual, core, event

win = visual.Window(size=[800, 600], fullscr=False, units='pix', monitor='TestMonitor')

class Record:
    def __init__(self, sample_rate, sec, win):
        self.sample_rate = sample_rate
        self.sec = sec
        self.win = win
        self.filename = ''

    # returned recorded sound
    def mysignal(self):
        print(f'Start Recording for {self.sec} seconds')
        signal = sd.rec(frames=int(self.sec * self.sample_rate), samplerate=self.sample_rate, channels=1, blocking = 'True')
        core.wait(1)
        print("Recording Ended !!!")
       # print(signal)
        return signal

    # playback recorded data
    def playback(self, signal):
        fig, ax = plt.subplots(1, 2)

        #sd.play(signal, self.sample_rate)
        ax[0].plot(signal)
        ax[0].set_title('RECORDED SIGNAL')
        ax[0].set_xlabel('Time(s)')
        ax[0].set_ylabel('Amplitude(Hz)')

        xf = fft2(signal)
        n = len(signal)
        fr = (sample_rate/2) * np.linspace(0, 1, round(n/2))
        xm = (2/n) * abs(xf[0:len(fr)])

        ax[1].plot(fr, xm)
        ax[1].set_xlabel('Frequency(Hz)')
        ax[1].set_ylabel('Magnitude')
        ax[1].set_title('SOUND SPECTRUM')
        ax[1].grid()
        plt.tight_layout()
        plt.savefig('image_file1.jpg')

        image = visual.ImageStim(win, image='image_file1.jpg', units='pix')
        image.draw()
        win.flip()
        event.waitKeys()
        win.close()

    # save the recorded data
    def savefile(self, filename, signal):
        sf.write(filename, signal, self.sample_rate)
        return


sample_rate = 48000
sec = 30
myrec = Record(sample_rate, sec, win)
val = myrec.mysignal()
myrec.playback(val)
myrec.savefile('new_signal_record.wav', val)
