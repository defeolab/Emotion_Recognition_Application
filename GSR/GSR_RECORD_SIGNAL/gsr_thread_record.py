import queue
import tempfile
import threading
import tkinter as tk
from psychopy import data
import numpy as np
import sounddevice as sd
import soundfile as sf
import os


def file_writing_thread(*, q, **soundfile_args):
    """Write data from queue to file until *None* is received."""
    with sf.SoundFile(**soundfile_args) as f:
        while True:
            cdata = q.get()
            print(cdata)
            if cdata is None:
                break
            f.write(cdata)


class Record(tk.Tk):

    stream = None

    def __init__(self):
        self.input_overflows = 0
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.thread = None
        self.thread1 = None
        self.peak = 0
        self.metering_q = queue.Queue(maxsize=1)
        self.filename = None
        self.name = None


    def create_stream(self,):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(samplerate=300000, device=sd.default.device['input'], channels=2, callback=self.audio_callback)
        self.stream.start()

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

        self.peak = max(self.peak, np.max(np.abs(indata)))
        try:
            self.metering_q.put_nowait(self.peak)
        except queue.Full:
            pass
        else:
            self.peak = 0

    def on_rec(self, path):
        self.recording = True

        cpath = os.path.join(path, 'gsr_file')
        if os.path.exists(cpath):
            name = cpath
        else:
            os.makedirs(cpath)
            name = cpath

        self.filename = tempfile.mktemp(prefix=data.getDateStr(), suffix='.wav', dir=name)

        self.thread1 = threading.Thread(target=self.create_stream, args=(), daemon=True)
        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=file_writing_thread,
            kwargs=dict(
                file=self.filename,
                mode='x',
                samplerate=300000,
                channels=2,
                q=self.audio_q,
            ), daemon=True,
        )
        self.thread1.start()
        self.thread.start()

    def on_stop(self, *args):
        self.recording = False
        self.stream.close()
        self.name = self.filename
        if self.thread.is_alive():
            return self.name
        self.thread.join()
        self.thread1.join()

path = os.getcwd()
print(path)
main = Record()


def quit():
    root.destroy()


def start():
    main.create_stream()
    main.on_rec(path)
    btn1.config(state=tk.DISABLED)
    btn2.configure(state=tk.NORMAL)


filename = None


def stop():
    global filename
    filename = main.on_stop()
    print('Closing streaming')
    btn2.config(state=tk.DISABLED)
    btn1.configure(state=tk.NORMAL)
    print(filename)
    printAfterStop()
    return filename


def printAfterStop():
    print("Filename after stop: " + str(filename))
    return filename


root = tk.Tk()
frame = tk.Frame(root)
btn1 = tk.Button(frame, text='Start Record', command=start)
btn2 = tk.Button(frame, text="Stop Record", command=stop, state=tk.DISABLED)
btn3 = tk.Button(frame, text="Exit", command=quit)
btn1.pack()
btn2.pack()
btn3.pack()
frame.pack()
root.mainloop()


