import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter


class ButterWorthFilter:

    def __init__(self):
        self.signal, self.sample_freq = sf.read(
            r"C:\Users\Neuromarketing\PycharmProjects\Emotion_Recognition_Application\new1_signal1_record_112_1.wav")


    def leftRightChannel(self):
        left_channel = []
        right_channel = []
        for i in self.signal:
            left_channel.append(i[0])
            right_channel.append(i[1])

        # compute range of the signal seconds
        time = np.linspace(0, len(self.signal) / self.sample_freq, len(self.signal))
        return time, left_channel, right_channel

    def butterLowPass(self):
        order = 4  # filter order number
        cutoff = 10000  # cutoff frequency
        time, left_channel, right_channel = self.leftRightChannel()
        b, a = butter(order, cutoff, btype='lowpass', fs=self.sample_freq)
        left_butter_filter = lfilter(b, a, left_channel)
        right_butter_filter = lfilter(b, a, right_channel)

        df = pd.DataFrame({'Time': time, 'Left_Channel': left_channel, 'Right_Channel': right_channel,
                           'LeftButterWorth': left_butter_filter, 'RightButterWorth': right_butter_filter})

        # save as csv file
        df.to_csv(r'C:\Users\Neuromarketing\PycharmProjects\Emotion_Recognition_Application\new1_signal1_record_112_1.csv')

        return time, left_butter_filter, right_butter_filter

    def canvasPlot(self):
        root = tk.Tk()
        root.title('Left and Right Channel Butterworth Filter')
        frame = tk.Frame(root)
        frame1 = tk.Frame(root)

        time, left_filter, right_filter = self.butterLowPass()

        fig = plt.Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, left_filter)
        ax.set_title('Left Channel Butterworth Filter')
        ax.set_xlabel('Time(secs)')
        ax.grid()
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar.pack(side=tk.LEFT)

        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(time, right_filter)
        ax1.set_title('Right Channel Butterworth Filter')
        ax1.set_xlabel('Time(secs)')
        ax1.grid()
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH)
        toolbar1 = NavigationToolbar2Tk(canvas1, frame1)
        toolbar1.update()
        toolbar1.pack()

        plt.rcParams['agg.path.chunksize'] = 1000

        frame.pack(side=tk.LEFT)
        frame1.pack(side=tk.LEFT)

        root.mainloop()

        return

