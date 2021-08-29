import json
import threading
import datetime

from cefpython3 import cefpython as cef
import ctypes
import GSR.GSR_RECORD_SIGNAL.recordgsr as gsr
import ScreenRecording
import GSR_rec
import ffmpeg_video_audio
import patientWindow
import webBrowser

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import platform
import logging as _logging
import patientWindow as pw

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")


class MainFrame(tk.Frame):

    def __init__(self, root, starting_url, type_exp,id, old_window,old_root,frame = None):
        self.browser_frame = None
        self.navigation_bar = None
        self.instruction_frame = None
        self.type = type_exp
        self.id = id
        self.old_window = old_window
        self.old_root = old_root

        fp = open('ffmpeg.txt', 'r')
        reso = json.load(fp)
        fp.close()


        self.sw,self.sh = root.winfo_screenwidth(),root.winfo_screenheight()
        # Root
        root.geometry('%sx%s+%s+%s' % (reso['tobii_width'], reso['tobii_hight'], -self.sw+reso['screen_shift'], 0))
        #root.geometry("900x640")
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        self.frame = frame

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("NeuroMarketing Experiment")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        self.navigation_bar = NavigationBar(self, root,self.type, starting_url,self.id,self.old_window, self.old_root,self.frame)
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
        self.old_root.destroy()
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




class BrowserFrame(tk.Frame):

    def __init__(self, master, starting_url, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        self.starting_url = starting_url
        tk.Frame.__init__(self, master)
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

class launch_browser:
    def __init__(self,url, type, id, window, old_root, frame, path=None, exptype=None):
#def launch_browser(url, type, id, window, old_root, frame, path=None, exptype=None):
    #browser_frame = None

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
        app = MainFrame(self.root, url, type, id, window, old_root, frame)
        rec = None
        if exptype == "gsr":
            rec = gsr.Record()
            rec.on_rec(path)


    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
        cef.Initialize()


        #im_timer = threading.Thread(target=self.countdown, args=(self.dur,))
        #im_timer.start()

        t1 = threading.Thread(target=app.browser_frame.mainloop())
        t1.start()
        cef.Shutdown()




class NavigationBar(tk.Frame):
    def __init__(self, master, root,type_exp, starting_url, id, old_window,old_root,frame = None):
        #self.countdown = None
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
        self.old_root = old_root
        self.frame = frame
        self.enable = 0

        fp = open('ffmpeg.txt', 'r')
        dur = json.load(fp)
        fp.close()

        #self.duration = int(dur['dur'])

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

        #        Reload button
        refresh = 'resources/reload.png'
        self.reload_image = tk.PhotoImage(file=refresh)
        self.reload_button = tk.Button(self, image=self.reload_image, command=self.reload)
        self.reload_button.grid(row=0, column=2)

        #start_rec = tk.Button(self, text="Start Experiment!",command =self.start_recording)
        #start_rec.grid(row=0, column=3)


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
        file = open('ffmpeg.txt', 'r')
        self.duration = json.load(file)
        file.close()
        (h, m, s) = self.duration['duration'].split(':')
        self.result = int(h) * 3600 + int(m) * 60 + int(s)
        #self.loading_countdown(self.websites['loading_time'])
        loading_time = threading.Thread(target=self.loading_countdown, args=(self.websites['loading_time'],))
        loading_time.start()

    def GSR_rec(self, pat, id,type):
        main = GSR_rec.Record(pat, id,type)
        main.create_stream()
        main.on_rec()

    def countdown(self, time):
        if time == -1:
            self.enable = 1
            self.root.destroy()
            finish = tk.Label(self.old_root, text ="Experiment finished! press the close Button.",font='Times 14')
            finish.grid(row=14,column=1)
        else:
            self.root.after(1000, self.countdown, time - 1)
    def loading_countdown(self, time):
        if time == -1:
            #self.enable = 1
            print("loading time end")
            self.chrono_countdown(self.result)
            if self.type == 1:

                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3,1))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3,1))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3,1))
                gsr.start()
            elif self.type == 2:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3,2))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3,2))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3,2))
                gsr.start()
            elif self.type == 3:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3,3))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3,3))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3,3))
                gsr.start()
            elif self.type == 4:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.id, 3,4))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.id, 3,4))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.id, 3,4))
                gsr.start()
            else:
                print("no experiment!")
            im_timer = threading.Thread(target=self.countdown, args=(self.result,))
            im_timer.start()

            #self.root.destroy()
            #self.master.destroy()
        else:
            self.root.after(1000, self.loading_countdown, time - 1)

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()


    def chrono_countdown(self, remaining=None):
        #self.chronometer['text'] = self.convert_seconds_left_to_time()
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.chronometer.configure(text="time's up!")
        else:
            self.chronometer.configure(text="remaining %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.after(1000, self.chrono_countdown)

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


