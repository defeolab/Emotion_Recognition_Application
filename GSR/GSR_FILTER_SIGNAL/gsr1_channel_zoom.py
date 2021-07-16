import matplotlib.pyplot as plt
import soundfile as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
import pandas as pd

class appSignal:
    def __init__(self, signal, root, root1):
        self.signal = signal
        self.root = root
        self.root1 = root1
        self.fig = None
        self.canvas = None

    #plot the original signal
    def myCanvas(self):
        self.fig = plt.Figure(dpi=100)
        ax = self.fig.add_subplot(111)
        ax.plot(self.signal)
        ax.set_title('ORIGINAL SIGNAL')

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()

    #plot the left and right channel signal
    def leftRightChannel(self):
        left = []
        right = []
        for i in self.signal:
            left.append(i[0])
            right.append(i[1])

        time = np.linspace(0, len(data) / sample, len(data))

        # create a frame for each contain each canvas
        frame = tk.Frame(master=self.root1)
        frame1 = tk.Frame(master=self.root1)

        # plot the signal in a canvas
        fig = plt.Figure(dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, left)
        ax.set_title('Left Channel')
        ax.set_xlabel('Time(secs)')
        ax.set_ylabel('Amplitude(V)')
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar.pack(side=tk.LEFT)

        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(time, right)
        ax1.set_title('Right Channel')
        ax1.set_xlabel('Time(secs)')
        ax1.set_ylabel('Amplitude(V)')
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH)
        toolbar1 = NavigationToolbar2Tk(canvas1, frame1)
        toolbar1.update()
        toolbar1.pack()

        frame.pack(side=tk.LEFT)
        frame1.pack(side=tk.LEFT)

        return time, left, right

"""
root = tk.Tk()
root.title('Original Signal')
root1 = tk.Tk()
root1.title('Left and Right Channel Signal')
plt.rcParams['agg.path.chunksize'] = 384000
main = appSignal(data, root, root1)
main.myCanvas()
time, left_channel, right_channel = main.leftRightChannel()

root.mainloop()
root1.mainloop()
"""