import signalRecord as ls
import tkinter as tk

window = tk.Tk()


def start():
    sample_rate = 48000
    sec = 10
    myrec = ls.Record(sample_rate, sec, window)
    val = myrec.mysignal()
    myrec.playback(val)
    myrec.savefile('new_signal_record.wav', val)

    return


btn = tk.Button(window, text='Start GSR ', command=start)
btn.pack()
window.mainloop()
