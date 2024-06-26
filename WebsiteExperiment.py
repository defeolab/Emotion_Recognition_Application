import json
import ctypes
import patientWindow as pw
import ScreenRecording
import ffmpeg_video_audio
import eyeTracker as ey
import GSR_rec
import platform
import sys
import GSR.GSR_RECORD_SIGNAL.recordgsr as gsr

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import threading
from cefpython3 import cefpython as cef

import logging as _logging

logger = _logging.getLogger("tkinter_.py")
# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


class launch_browser:
    def __init__(self,url, type, id, window, frame, path=None, exptype=None,cal_tracker=None):
        logger.setLevel(_logging.INFO)
        stream_handler = _logging.StreamHandler()
        formatter = _logging.Formatter("[%(filename)s] %(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.info("CEF Python {ver}".format(ver=cef.__version__))
        logger.info("Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
        logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
        assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        self.root = tk.Toplevel()
        sw, sh = 1920, 1080
        app = MainFrame(self.root, url, type, id, window, frame, cal_tracker)
        rec = None
        if exptype == "gsr":
            rec = gsr.Record()
            rec.on_rec(path)

    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
        cef.Initialize()

        t1 = threading.Thread(target=app.browser_frame.mainloop())
        t1.start()
        cef.Shutdown()


# Main Instruction Frame
class MainFrame(tk.Frame):

    def __init__(self, root, starting_url, type_exp,id, old_window,frame = None,cal_tracker=None):
        self.browser_frame = None
        self.navigation_bar = None
        self.instruction_frame = None
        self.type = type_exp
        self.id = id
        self.old_window = old_window
        self.frame = frame  #frame for lab setting enable
        self.cal_tracker=cal_tracker

        # Root
        if self.frame == True:
            fp = open('ffmpeg.txt', 'r')
            reso = json.load(fp)
            fp.close()
            self.sw, self.sh = root.winfo_screenwidth(), root.winfo_screenheight()
        # Root
            root.geometry('%sx%s+%s+%s' % (reso['tobii_width'], reso['tobii_hight'], -self.sw + reso['screen_shift'],
                                           reso['screen_shift_y']))
        else:
            root.geometry("900x640")

        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("NeuroMarketing Experiment")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        self.navigation_bar = NavigationBar(self, root,self.type, starting_url,self.id,self.old_window,
                                            self.frame,self.cal_tracker)
        self.navigation_bar.grid(row=0, column=0,
                                 sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, starting_url, self.navigation_bar)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
        self.master.destroy()
        if self.frame is not None:
            self.frame.stop()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None


# Instruction frame navigation
class NavigationBar(tk.Frame):
    def __init__(self, master, root, type_exp, starting_url, id, old_window, frame=None, cal_tracker=None):
        self.websites = None
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None
        tk.Frame.__init__(self, master)
        self.type = type_exp
        self.root = root
        self.starting_url = starting_url
        self.id = id
        self.frame = frame
        self.old_window = old_window
        self.cal_tracker = cal_tracker

        # Back button
        back = 'resources/back.png'
        self.back_image = tk.PhotoImage(file=back)
        self.back_button = tk.Button(self, image=self.back_image, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward = 'resources/forward.png'
        self.forward_image = tk.PhotoImage(file=forward)
        self.forward_button = tk.Button(self, image=self.forward_image, command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        # Reload button
        refresh = 'resources/reload.png'
        self.reload_image = tk.PhotoImage(file=refresh)
        self.reload_button = tk.Button(self, image=self.reload_image, command=self.reload)
        self.reload_button.grid(row=0, column=2)

        self.start_rec = tk.Button(self, text="Start Experiment!", command=self.start_experiment)
        self.start_rec.grid(row=0, column=3)

        # Url entry
        self.url_entry = tk.Entry(self)
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def start_experiment(self):
        tk.Frame.destroy(self.master)

        fp = open('websites.txt', 'r')
        self.websites = json.load(fp)
        fp.close()

        print(' Type in website experiment', self.type)

        if self.type == 1:
            SecondaryMainFrame(self.root, self.websites['website1'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 2:
            SecondaryMainFrame(self.root, self.websites['website2'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 3:
            SecondaryMainFrame(self.root, self.websites['website3'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 4:
            SecondaryMainFrame(self.root, self.websites['website4'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 5:
            SecondaryMainFrame(self.root, self.websites['website5'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 6:
            SecondaryMainFrame(self.root, self.websites['website6'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 7:
            SecondaryMainFrame(self.root, self.websites['website7'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 8:
            SecondaryMainFrame(self.root, self.websites['website8'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 9:
            SecondaryMainFrame(self.root, self.websites['website9'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 10:
            SecondaryMainFrame(self.root, self.websites['website10'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 11:
            SecondaryMainFrame(self.root, self.websites['website11'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 12:
            SecondaryMainFrame(self.root, self.websites['website12'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 13:
            SecondaryMainFrame(self.root, self.websites['website13'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 14:
            SecondaryMainFrame(self.root, self.websites['website14'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 15:
            SecondaryMainFrame(self.root, self.websites['website15'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 16:
            SecondaryMainFrame(self.root, self.websites['website16'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 17:
            SecondaryMainFrame(self.root, self.websites['website17'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 18:
            SecondaryMainFrame(self.root, self.websites['website18'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 19:
            SecondaryMainFrame(self.root, self.websites['website19'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        elif self.type == 20:
            SecondaryMainFrame(self.root, self.websites['website20'], self.type, self.id, self.old_window, self.frame,
                               cal_tracker=self.cal_tracker)
        else:
            print("no browser!")

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """Fix CEF focus issues (#255). See also FocusHandler.OnGotFocus."""
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)


# Main Browser Frame
class SecondaryMainFrame(tk.Frame):
    def __init__(self, root, starting_url, type_exp, id, old_window, frame=None, cal_tracker=None):
        self.browser_frame = None
        self.navigation_bar = None
        self.instruction_frame = None
        self.type = type_exp
        self.id = id
        self.old_window = old_window
        self.frame = frame
        self.cal_tracker = cal_tracker
        #self.eye_track_file = None
        self.root = root
        self.enable = 0

        if self.frame == True:
            fp = open('ffmpeg.txt', 'r')
            reso = json.load(fp)
            fp.close()
            self.sw, self.sh = root.winfo_screenwidth(), root.winfo_screenheight()
            root.geometry('%sx%s+%s+%s' % (
            reso['tobii_width'], reso['tobii_hight'], -self.sw + reso['screen_shift'], reso['screen_shift_y']))
        else:
            root.geometry("900x640")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("NeuroMarketing Experiment")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        self.navigation_bar = SecondaryNavigationBar(self, root, self.type, starting_url, self.id, self.old_window,
                                            frame=self.frame, cal_tracker=self.cal_tracker)
        self.navigation_bar.grid(row=0, column=0,
                                 sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, starting_url, self.navigation_bar)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.enable = 1
            self.browser_frame.on_root_close()


        self.master.destroy()

        if self.frame is not None:
            self.frame.stop()
        pw.PatientWindow(self.old_window, self.id)

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

# Main Navigation Frame
class SecondaryNavigationBar(tk.Frame):
    def __init__(self, master, root, type_exp, starting_url, id, old_window, frame=None, cal_tracker=None):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None
        tk.Frame.__init__(self, master)
        self.type = type_exp
        self.starting_url = starting_url
        self.id = id
        self.root = root
        self.old_window = old_window
        self.frame = frame
        #self.enable = 0
        self.cal_tracker = cal_tracker
        self.eye_track_file = None

        # Back button
        back = 'resources/back.png'
        self.back_image = tk.PhotoImage(file=back)
        self.back_button = tk.Button(self, image=self.back_image, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward = 'resources/forward.png'
        self.forward_image = tk.PhotoImage(file=forward)
        self.forward_button = tk.Button(self, image=self.forward_image, command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        #  Reload button
        refresh = 'resources/reload.png'
        self.reload_image = tk.PhotoImage(file=refresh)
        self.reload_button = tk.Button(self, image=self.reload_image, command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        self.update_state()

        self.chronometer = tk.Label(self, text=" ", width=20)
        self.chronometer.grid(row=0, column=4)
        self.remaining = 0

        fp = open('websites.txt', 'r')
        self.websites = json.load(fp)
        fp.close()

        (h, m, s) = self.websites['duration'].split(':')
        self.result = int(h) * 3600 + int(m) * 60 + int(s)

        #loading_time = threading.Thread(target=self.loading_countdown, args=(self.websites['loading_time'],))
        #loading_time.start()



        self.eye_track_file = ey.run_browser_experiment(self.starting_url, self.type, self.id,
                                                    self.old_window, self.root, True)
        self.eye_track_file.start_exp_rec(self.cal_tracker)
        cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, self.type, self.frame,
                                                                                  None))
        cam1.start()
        sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, self.type, self.frame, None))
        sc.start()
        # Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 1))
        # Gsr.start()
        if self.enable == 1:
            self.root.destroy()
            self.eye_track_file.stop_exp_rec(self.cal_tracker)
            finish = tk.Label(self.old_window, text="Experiment finished! press the close Button.", font='Times 14')
            finish.grid(row=14, column=1)

    def GSR_rec(self, pat, id, type):
        main = GSR_rec.Record(pat, id, type)  # passing the id, exp type and type
        main.create_stream()
        main.on_rec()
    """    
    def loading_countdown(self, time):
        if time == -1:
            # self.enable = 1
            print("loading time end")
            self.chrono_countdown(self.result)
            im_timer = threading.Thread(target=self.countdown, args=(self.result,))
            im_timer.start()

            self.eye_track_file = ey.run_browser_experiment(self.starting_url, self.type, self.id,
                                                            self.old_window, self.root, True)
            self.eye_track_file.start_exp_rec(self.cal_tracker)
            cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, self.type, self.frame,
                                                                                      None))
            cam1.start()
            sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, self.type, self.frame, None))
            sc.start()
            # Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 1))
            # Gsr.start()
    def countdown(self, time):
        if time == -1:
            self.enable = 1
            self.root.destroy()
            print(self.eye_track_file)
            self.eye_track_file.stop_exp_rec(self.cal_tracker)
            finish = tk.Label(self.old_window, text="Experiment finished! press the close Button.", font='Times 14')
            finish.grid(row=14, column=1)
        else:
            self.root.after(1000, self.countdown, time - 1)

    def chrono_countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.chronometer.configure(text="time's up!")
        else:
            self.chronometer.configure(text="remaining %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.chrono_countdown)
    """
    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """Fix CEF focus issues (#255). See also FocusHandler.OnGotFocus."""
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)

"""
            #if self.frame == True:
            if self.type == 1:
                    self.eye_track_file = ey.run_browser_experiment(self.websites['website1'], 1, self.id,
                                                                    self.old_window, self.root, True)
                    self.eye_track_file.start_exp_rec(self.cal_tracker)
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 1, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 1, self.frame, None))
                    sc.start()
                    #Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 1))
                    #Gsr.start()
            elif self.type == 2:
                    self.eye_track_file = ey.run_browser_experiment(self.websites['website2'], 2, self.id,
                                                                    self.old_window, self.root, True)
                    self.eye_track_file.start_exp_rec(self.cal_tracker)
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 2, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 2, self.frame, None))
                    sc.start()
                    #Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 2))
                    #Gsr.start()
            elif self.type == 3:
                    self.eye_track_file = ey.run_browser_experiment(self.websites['website3'], 3, self.id,
                                                                    self.old_window, self.root, True)
                    self.eye_track_file.start_exp_rec(self.cal_tracker)
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 3, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 3, self.frame, None))
                    sc.start()
                    #Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 3))
                    #Gsr.start()
            elif self.type == 4:
                    self.eye_track_file = ey.run_browser_experiment(self.websites['website4'], 4, self.id,
                                                                    self.old_window, self.root, True)
                    self.eye_track_file.start_exp_rec(self.cal_tracker)
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 4, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 4, self.frame, None))
                    sc.start()
                    #Gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3, 4))
                    #Gsr.start()
            else:
                    print("no experiment!")
            
            else:
                if self.type == 1:

                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 1, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 1, self.frame, None))
                    sc.start()

                elif self.type == 2:
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 2, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 2, self.frame, None))
                    sc.start()

                elif self.type == 3:
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 3, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 3, self.frame, None))
                    sc.start()

                elif self.type == 4:
                    cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3, 4, self.frame,
                                                                                              None))
                    cam1.start()
                    sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3, 4, self.frame, None))
                    sc.start()

                else:
                    print("no experiment!")

"""
 #       else:
 #           self.root.after(1000, self.loading_countdown, time - 1)#



# Common Browser Frame
class BrowserFrame(tk.Frame):

    def __init__(self, master, starting_url, navigation_bar):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        self.starting_url = starting_url
        # tk.Frame.__init__(self, master)
        self.brFrame = tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url=self.starting_url)
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("BrowserFrame.on_focus_out")
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        self.browser = None


class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())


class FocusHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        return False

    def OnGotFocus(self, **_):
        """Fix CEF focus issues (#255). Call browser frame's focus_set
           to get rid of type cursor in url entry widget."""
        logger.debug("FocusHandler.OnGotFocus")
        self.browser_frame.focus_set()
