import vlc


import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# import standard libraries
import os
from threading import Timer, Thread, Event
import time
from tkinter import filedialog

import GSR.GSR_RECORD_SIGNAL.recordgsr as gsr

class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this"""

    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Player(Tk.Frame):

    def __init__(self, parent, frame=None, title=None, type=None, path=None, sec=None):
        Tk.Frame.__init__(self, parent)
        self.videoPath = None
        self.parent = parent
        self.type = type
        self.path = path
        self.forward_music_image = None
        self.player = None
        self.rec = gsr.Record()
        self.frame = frame

        self.parent.title("tk_vlc")
        self.parent.protocol("WM_DELETE_WINDOW", self.closeTop)
        self.parent.bind('<space>', self.OnPause)

        # Menu Bar
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        # Upload
        # upload = 'resources/upload.png'
        # self.upload_image = Tk.PhotoImage(file=upload)
        ttk.Button(self.parent, text="Upload", command=self.load_video).pack()

        # Panel 2: Video Frame
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # Panel 3: Play/pause, Volume
        ctrlpanel = ttk.Frame(self.parent)

        # Play
        play = 'resources/play.png'
        self.play_image = Tk.PhotoImage(file=play)
        self.play_button = ttk.Button(ctrlpanel, image=self.play_image, command=self.OnPlay)
        self.play_button.grid(row=0, column=0)

        pause = 'resources/pause.png'
        self.pause_image = Tk.PhotoImage(file=pause)
        self.pause_button = ttk.Button(ctrlpanel, image=self.pause_image, command=self.OnPause)
        self.pause_button.grid(row=0, column=1)

        # Rewind
        rewind = 'resources/rewind_music.png'
        self.rewind_image = Tk.PhotoImage(file=rewind)
        self.rewind_button = ttk.Button(ctrlpanel, image=self.rewind_image, command=self.OnPlay)
        self.rewind_button.grid(row=0, column=2)

        # Forward
        forward = 'resources/forward_music.png'
        self.forward_image = Tk.PhotoImage(file=forward)
        self.forward_button = Tk.Button(ctrlpanel, image=self.forward_image, command=self.OnPlay)
        self.forward_button.grid(row=0, column=3)

        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel,
                                  from_=0, to=100, orient=Tk.HORIZONTAL, length=100)
        self.volslider.set(100)
        self.volslider.grid(row=0, column=5)

        ctrlpanel.pack(side=Tk.BOTTOM)

        # Panel 4:
        TimeSliderpanel = ttk.Frame(self.parent)

        self.scale_var = Tk.DoubleVar()
        self.timeslider_last_val = ""
        self.timeslider = Tk.Scale(TimeSliderpanel, variable=self.scale_var, command=self.scale_sel,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeslider_last_update = time.time()

        TimeSliderpanel.pack(side=Tk.BOTTOM, fill=Tk.X)

        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.timer = ttkTimer(self.OnTimer, 1.0)
        self.timer.start()
        self.parent.update()

        # if a file is already running, then stop it.
        self.OnStop()

        if not hasattr(self, "events"):
            self.events = self.player.event_manager()
            self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.EventManager)

    def EventManager(self, event):
        if event.type == vlc.EventType.MediaPlayerEndReached:
            self.closeTop()

    def closeTop(self):
        self.timer.stop()
        self.parent.destroy()
        os.startfile(
            "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")
        self.OnStop()

    # loads the video
    def load_video(self):
        self.videoPath = filedialog.askopenfilename(initialdir=os.getcwd() + "/videos/", parent=self.parent)

        if self.videoPath:
            self.Media = self.Instance.media_new(self.videoPath)
            self.player.set_media(self.Media)
            self.player.set_hwnd(self.GetHandle())

            self.OnPlay()
        else:
            self.errorDialog("File Error.")

    def OnPlay(self):

        ############################################################
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        ############################################################

        if self.type == "gsr":
            self.rec.on_rec(self.path)

        if not self.player.get_media():
            self.OnOpen()
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    def OnPause(self):
        # Pause the player.
        self.player.pause()
        self.rec.on_stop()

    def OnStop(self):

        # Stop the player
        self.player.stop()
        # reset the time slider
        self.timeslider.set(0)

    def OnTimer(self):
        """Update the time slider according to the current movie time."""

        if self.player == None:
            return

        #################################################################
        # since the self.player.get_length can change while playing,
        # re-set the timeslider to the correct range.
        #################################################################

        length = self.player.get_length()
        dbl = length * 0.001
        self.timeslider.config(to=dbl)

        # update the time on the slider
        tyme = self.player.get_time()
        if tyme == -1:
            tyme = 0
        dbl = tyme * 0.001
        self.timeslider_last_val = ("%.0f" % dbl) + ".0"

        ############################################################################
        # don't want to programatically change slider while user is messing with it.
        # wait 2 seconds after user lets go of slider
        ############################################################################

        if time.time() > (self.timeslider_last_update + 2.0):
            self.timeslider.set(dbl)

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            ######################################################################################################

            # this is a hack. The timer updates the time slider.
            # This change causes this rtn (the 'slider has changed' rtn) to be invoked.
            # I can't tell the difference between when the user has manually moved the slider and when
            # the timer changed the slider. But when the user moves the slider tkinter only notifies
            # this rtn about once per second and when the slider has quit moving.
            # Also, the tkinter notification value has no fractional seconds.
            # The timer update rtn saves off the last update value (rounded to integer seconds) in timeslider_last_val
            # if the notification time (sval) is the same as the last saved time timeslider_last_val then
            # we know that this notification is due to the timer changing the slider.
            # otherwise the notification is due to the user changing the slider.
            # if the user is changing the slider then I have the timer routine wait for at least
            # 2 seconds before it starts updating the slider again (so the timer doesn't start fighting with the
            # user)
            # selection = "Value, last = " + sval + " " + str(self.timeslider_last_val)
            # print("selection= ", selection)

            ####################################################################################################

            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval))  # expects milliseconds

    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100

        self.player.audio_set_volume(volume)

    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button."""
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)

        ####################################################################
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        ####################################################################

        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):

        """Set the volume according to the volume sider."""

        volume = self.volume_var.get()
        print("volume= ", volume)
        if volume > 100:
            volume = 100

        self.player.audio_set_volume(volume)
