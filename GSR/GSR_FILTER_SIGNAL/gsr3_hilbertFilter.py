import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import *
from scipy.signal import butter, lfilter, hilbert


class HilbertTransformClass:
    def __init__(self, root1, root2, root3, root4, sample_freq, left_butter, right_butter, time):
        self.root1 = root1
        self.root2 = root2
        self.root3 = root3
        self.root4 = root4
        self.sample_freq = sample_freq
        self.left_butterworth = left_butter
        self.right_butterworth = right_butter
        self.time = time

    # perform the hilbertTransform on the butterworth filter signal from the channel
    def hilbert_transform(self, signal, sample_freq):
        analytic_signal = hilbert(signal)  # analytic signal by hilbert tranform function
        envelop = np.abs(analytic_signal)  # hilbert Amplitude envelope
        instant_phase = np.unwrap(np.angle(analytic_signal))  # instantaneous phase
        instant_freq = (np.diff(instant_phase) / (2.0 * np.pi) * sample_freq)  # instantaneous frequency
        return analytic_signal, envelop, instant_phase, instant_freq

    def left_hilbert_transform(self):
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.hilbert_transform(
            self.left_butterworth, self.sample_freq)
        return left_analytic_signal, left_envelop, left_phase, left_instant_freq

    def right_hilbert_transform(self):
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.hilbert_transform(
                self.right_butterworth, self.sample_freq)
        return right_analytic_signal, right_envelop, right_phase, right_instant_freq

    # method to perform a butterworth filter on the left hilbertTransform envelop with 1000Hz
    def left_envelop_butterworth(self, order=4, cutoff=1000):
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        b, a = butter(order, cutoff, btype='low', fs=self.sample_freq)
        left_envelop_filter = lfilter(b, a, left_envelop)
        return left_envelop_filter

    # method to perform a butterworth filter on the right hilbertTransform envelop with 1000Hz
    def right_envelop_butterworth(self, order=4, cutoff=1000):
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()
        b, a = butter(order, cutoff, btype='low', fs=self.sample_freq)
        right_envelop_filter = lfilter(b, a, right_envelop)
        return right_envelop_filter

    # method to perform a butterworth filter on the left instantaneous frequency with 1000Hz
    def left_frequency_butterworth(self, order=4, cutoff=1000):
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        b, a = butter(order, cutoff, btype='low', fs=self.sample_freq)
        left_freq_filter = lfilter(b, a, left_instant_freq)
        return left_freq_filter

    # method to perform a butterworth filter on the right instantaneous frequency with 1000Hz
    def right_frequency_butterworth(self, order=4, cutoff=1000):
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()
        b, a = butter(order, cutoff, btype='low', fs=self.sample_freq)
        right_freq_filter = lfilter(b, a, right_instant_freq)
        return right_freq_filter

    # plot the left and right Instantaneous Frequency
    def plot_instant_frequency(self):

        # get the left and right instantaneous frequency from hilbert_transform()
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()

        self.root1.title('Instantaneous Frequency')
        frame1 = Frame(self.root1)
        frame2 = Frame(self.root1)

        left_instant_freq = left_instant_freq/200000
        right_instant_freq = right_instant_freq/200000

        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.time[1:], left_instant_freq)
        ax1.set_xlabel('Times(sec)')
        ax1.set_ylabel('Frequency(Hz)')
        ax1.set_title('Left Channel Instantaneous Frequency')
        ax1.grid()
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)
        tool1 = NavigationToolbar2Tk(canvas1, frame1)
        tool1.update()
        tool1.pack()
        plt.tight_layout()

        # plot the left instantaneous frequency
        fig2 = plt.Figure(dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.time[1:], right_instant_freq)  # right instantaneous frequency
        ax2.set_xlabel('Times(sec)')
        ax2.set_ylabel('Frequency(Hz)')
        ax2.grid()
        ax2.set_title('Right Channel Instantaneous Frequency')
        canvas2 = FigureCanvasTkAgg(fig2, frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)
        tool2 = NavigationToolbar2Tk(canvas2, frame2)
        tool2.update()
        tool2.pack()

        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)

    # plot left right analytic signal and the envelop
    def plot_analytic_envelop(self):

        # get the left and right Analytic signal and envelop from hilbert_transform()
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()

        self.root2.title('Analytic Signal and Extracted Envelop')
        frame1 = Frame(self.root2)
        frame2 = Frame(self.root2)

        # plot the left analytic signal and right envelop
        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.time, left_analytic_signal, label='signal')  # left analytic signal
        ax1.plot(self.time, left_envelop, label='envelop')  # left envelop
        ax1.set_xlabel('Times(sec)')
        ax1.set_ylabel('Amplitude(V)')
        ax1.grid()
        ax1.set_title('Left Analytic Signal And Extracted Envelope')
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)
        tool1 = NavigationToolbar2Tk(canvas1, frame1)
        tool1.update()
        tool1.pack()
        fig1.legend()
        plt.tight_layout()

        # plot the right analytic signal and right envelop
        fig2 = plt.Figure(dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.time, right_analytic_signal, label='signal')  # right analytic signal
        ax2.plot(self.time, right_envelop, label='envelop')  # right envelop
        ax2.set_xlabel('Times(sec)')
        ax2.set_ylabel('Amplitude(V)')
        ax2.set_title('Right Channel Analytic Signal And Extracted Envelope')
        ax2.grid()
        canvas2 = FigureCanvasTkAgg(fig2, frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)
        tool2 = NavigationToolbar2Tk(canvas2, frame2)
        tool2.update()
        tool2.pack()
        fig2.legend()
        plt.tight_layout()

        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)

    # plot analytic signal, envelop and envelop butterworth filter
    def plot_filter_envelop(self):

        # get the left and right instantaneous frequency
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()

        # get the envelop filter from left_envelop_butterworth() and right_envelop_butterworth()
        left_envelop_filter = self.left_envelop_butterworth()
        right_envelop_filter = self.right_envelop_butterworth()

        self.root3.title('Analytic Signal, Envelop and Envelop Butterworth Filter')
        frame1 = Frame(self.root3)
        frame2 = Frame(self.root3)

        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.time, left_analytic_signal, label='signal')  # left analytic signal
        ax1.plot(self.time, left_envelop, label='envelop')  # left envelop
        ax1.plot(self.time, left_envelop_filter, label='envelop filter')  # left butterworth envelop
        ax1.set_xlabel('Times(sec)')
        ax1.set_ylabel('Amplitude(V)')
        ax1.grid()
        ax1.set_title("Left Signal, Envelop and Filter Envelop")
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)
        tool1 = NavigationToolbar2Tk(canvas1, frame1)
        tool1.update()
        tool1.pack()
        fig1.legend()
        plt.tight_layout()

        # plot the right channel
        fig2 = plt.Figure(dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.time, right_analytic_signal, label='signal')  # right analytic signal
        ax2.plot(self.time, right_envelop, label='envelop')  # right envelop
        ax2.plot(self.time, right_envelop_filter, label='envelop filter')  # right butterworth envelop
        ax2.set_xlabel('Times(sec)')
        ax2.set_ylabel('Amplitude(V)')
        ax2.grid()
        ax2.set_title("Right Signal, Envelop and Filter Envelop")
        canvas2 = FigureCanvasTkAgg(fig2, frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)
        tool2 = NavigationToolbar2Tk(canvas2, frame2)
        tool2.update()
        tool2.pack()
        fig2.legend()

        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)

    # plot the left right analytic signal, envelop and Instantaneous Frequency
    # envelop filter  and instantaneous frequency filter
    def plot_analytic_envelop_frequency(self):

        # get the left and right Analytic signal and envelop from hilbert_transform()
        left_analytic_signal, left_envelop, left_phase, left_instant_freq = self.left_hilbert_transform()
        right_analytic_signal, right_envelop, right_phase, right_instant_freq = self.right_hilbert_transform()

        # get the envelop filter from left_envelop_butterworth() and right_envelop_butterworth()
        left_envelop_filter = self.left_envelop_butterworth()
        right_envelop_filter = self.right_envelop_butterworth()

        left_instant_freq = left_instant_freq / 200000
        right_instant_freq = right_instant_freq / 200000

        left_freq_filter = self.left_frequency_butterworth()
        left_freq_filter = left_freq_filter / 200000  # divide the instant freq by 200kH
        right_freq_filter = self.right_frequency_butterworth()
        right_freq_filter = right_freq_filter / 200000

        self.root4.title('Analytic Signal, Envelop, Instantaneous Frequency, Envelop Filter and Instant Frequency Filter')
        frame1 = Frame(self.root4)
        frame2 = Frame(self.root4)

        fig1 = plt.Figure(dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.time, left_analytic_signal, label='signal')  # left analytic signal
        ax1.plot(self.time, left_envelop, label='envelop')  # left envelop
        ax1.plot(self.time[1:], left_instant_freq, label='Instantaneous frequency')
        ax1.plot(self.time, left_envelop_filter, label='envelop filter')
        ax1.plot(self.time[1:], left_freq_filter, label='frequency filter')
        ax1.set_xlabel('Times(sec)')
        ax1.set_ylabel('Amplitude(V)')
        ax1.grid()
        ax1.set_title('Left Signal,Envelop,Instantaneous freq,envelop and instant freq filter')
        canvas1 = FigureCanvasTkAgg(fig1, frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=BOTH, expand=True)
        tool1 = NavigationToolbar2Tk(canvas1, frame1)
        tool1.update()
        tool1.pack()
        fig1.legend()
        plt.tight_layout()

        fig2 = plt.Figure(dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(self.time, right_analytic_signal, label='signal')  # right analytic signal
        ax2.plot(self.time, right_envelop, label='envelop')  # right envelop
        ax2.plot(self.time[1:], right_instant_freq, label='Instantaneous frequency')
        ax2.plot(self.time, right_envelop_filter, label='envelop filter ')
        ax2.plot(self.time[1:], right_freq_filter, label='frequency filter ')
        ax2.set_xlabel('Times(sec)')
        ax2.set_ylabel('Amplitude(V)')
        ax2.grid()
        ax2.set_title('Right Signal,Envelop,Instantaneous freq,envelop and instant freq filter')
        canvas2 = FigureCanvasTkAgg(fig2, frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=BOTH, expand=True)
        tool2 = NavigationToolbar2Tk(canvas2, frame2)
        tool2.update()
        tool2.pack()
        fig2.legend()
        plt.tight_layout()

        frame1.pack(side=LEFT)
        frame2.pack(side=RIGHT)


