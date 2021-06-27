import signalRecord as ls
import tkinter as tk

window = tk.Tk()


def start():
    sample_rate = 384000     #using the highest sampling frequency
    sec = 10
    myrec = ls.Record(sample_rate, sec, window)
    val = myrec.mysignal()
    myrec.playback(val)
    myrec.savefile('new1_signal_record.wav', val)
    return


btn = tk.Button(window, text='Start GSR ', command=start)
btn.pack()
window.mainloop()
