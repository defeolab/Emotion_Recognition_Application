from tkinter import *
import matplotlib.pyplot as plt
#import gsr2_butterFilter
import gsr3_hilbertFilter as hlb
import pandas as pd
import soundfile as sf

# read the original signal to extract the sampling frequency
_, sample_freq = sf.read(r"C:\Users\chuks\OneDrive\Desktop\THESIS\signals\signal_384000\signal_wet_hands_with_alcohol.wav")

# read from the csv file to extract the time, left and right channel butterworth filter
df = pd.read_csv(r'C:\Users\chuks\OneDrive\Desktop\ANACONDA\JUPYTER_NOTEBOOK\sample_wet_hands1.csv')

left_butter = df['LeftButterWorth']
right_butter = df['RightButterWorth']
time = df['Time']

root1 = Tk()
root2 = Tk()
root3 = Tk()
root4 = Tk()

plt.rcParams['agg.path.chunksize'] = 2000

app = hlb.HilbertTransformClass(root1, root2, root3, root4, sample_freq, left_butter, right_butter, time)

app.hilbert_transform(left_butter, sample_freq)  # hilbert transform of the left channel signal
app.hilbert_transform(right_butter, sample_freq)  # hilbert transform of the left channel signal

# perform right butterworth filter on the right envelop
app.left_envelop_butterworth()
app.right_envelop_butterworth()

# perform butterworth filter on the left instantaneous frequency
app.left_frequency_butterworth()
app.right_frequency_butterworth()

# plot the right hilbert transform and the envelop
app.plot_analytic_envelop()

# plot the left and right Instantaneous Frequency
app.plot_instant_frequency()

# plot left and right butterworth filter envelop, analytic signal and envelop
app.plot_filter_envelop()

# plot the left and right Analytic Signal,Envelop,instant freq, butterworth filter of envelop and Instantaneous Frequency
app.plot_analytic_envelop_frequency()

root1.mainloop()
root2.mainloop()
root3.mainloop()
root4.mainloop()