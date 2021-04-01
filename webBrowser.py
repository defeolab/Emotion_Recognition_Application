from cefpython3 import cefpython as cef
import ctypes

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import sys
import platform
import logging as _logging

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")

# Globals
logger = _logging.getLogger("tkinter_.py")


class MainFrame(tk.Frame):

    def __init__(self, root, starting_url, type_exp):
        self.browser_frame = None
        self.navigation_bar = None
        self.instruction_frame = None
        self.type = type_exp  # 1= Camilla, 2=Chiara
        # Root
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
        self.navigation_bar = NavigationBar(self, self.type)
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

        # InstructionFrame
        self.instruction_frame = InstructionFrame(self, self.type)
        self.instruction_frame.grid(row=1, column=1, sticky=(tk.N + tk.S + tk.E + tk.W))
        # tk.Grid.rowconfigure(self, 0, weight=1)
        # tk.Grid.columnconfigure(self, 1, weight=1)

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

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None


class BrowserFrame(tk.Frame):

    def __init__(self, master, starting_url="", navigation_bar=None):
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
        # elif MAC:
        #     from AppKit import NSApp
        #     import objc
        #     return objc.pyobjc_id(NSApp.windows()[-1].contentView())
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


class NavigationBar(tk.Frame):
    def __init__(self, master, type_exp):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None
        tk.Frame.__init__(self, master)
        self.type = type_exp

        # Back button
        back = 'resources/back.png'
        self.back_image = tk.PhotoImage(file=back)
        # self.back_image = self.back_image.zoom(25).subsample(100)
        self.back_button = tk.Button(self, image=self.back_image, command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward = 'resources/forward.png'
        self.forward_image = tk.PhotoImage(file=forward)
        # self.forward_image = self.forward_image.zoom(25).subsample(100)
        self.forward_button = tk.Button(self, image=self.forward_image, command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        #        Reload button
        refresh = 'resources/reload.png'
        self.reload_image = tk.PhotoImage(file=refresh)
        # self.reload_image = self.reload_image.zoom(25).subsample(100)
        self.reload_button = tk.Button(self, image=self.reload_image, command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        if self.type == 1:
            self.nespresso_button = tk.Button(self, text="Nespresso", command=self.go_toNespresso)
            self.nespresso_button.grid(row=0, column=5, padx=20)

            self.lavazza_button = tk.Button(self, text="Lavazza", command=self.go_toLavazza)
            self.lavazza_button.grid(row=0, column=4, padx=20)

        elif self.type == 2:
            self.spain_button = tk.Button(self, text="Spagna", command=self.go_toSpagna)
            self.spain_button.grid(row=0, column=5, padx=20)

            self.norway_button = tk.Button(self, text="Norvegia", command=self.go_toNorvegia)
            self.norway_button.grid(row=0, column=4, padx=20)

        # Update state of buttons
        self.update_state()

    def go_toNespresso(self):
        self.master.get_browser().StopLoad()
        self.master.get_browser().LoadUrl(
            "https://www.nespresso.com/it/it/our-choices/esperienza-caffe/lean-in-and-listen-stories-behind-nespresso-fairtrade-coffee")

    def go_toLavazza(self):
        self.master.get_browser().StopLoad()
        self.master.get_browser().LoadUrl("https://www.lavazza.it/it.html")

    def go_toSpagna(self):
        self.master.get_browser().StopLoad()
        self.master.get_browser().LoadUrl("https://www.spain.info/it/")

    def go_toNorvegia(self):
        self.master.get_browser().StopLoad()
        self.master.get_browser().LoadUrl("https://www.visitnorway.it/")

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


class InstructionFrame(tk.Frame):
    def __init__(self, master, type_exp):
        self.instruction = None
        tk.Frame.__init__(self, master)
        self.type = type_exp
        # self.instruction = tk.Listbox(self)
        self.instruction = tk.Text(self, width=50, font=("Helvetica", 14))
        self.instruction.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, minsize=200, weight=1)

        if self.type == 1:
            self.instruction.insert(tk.INSERT, "GRUPPO A\nIstruzioni per sito Lavazza:\n     • Andare sul sito lavazza.it \n"
                                           "     • Cliccare tasto “Menu”\n     • Cliccare tasto “Sostenibilità”\n"
                                           "     • Cliccare tasto “Fondazione”\n     • Leggere la pagina “Fondazione Lavazza”\n"
                                           "     • Leggere l’articolo “Innovazione contro il cambiamento                     climatico” cliccando il tasto “Scopri di più”\n"
                                           "     • Leggere l’articolo “L’impresa di diventare impresa”\n"
                                           "     • Leggere l’articolo “Il caffè per rinascere” \n\nGRUPPO B\nIstruzioni per sito Nespresso:\n"
                                           "     • Andare sul sito nespresso.com\n     • Passare il mouse sul tasto “Sostenibilità e riciclo”\n"
                                           "     • Cliccare tasto “Il caffè secondo Nespresso”\n     • Leggere l’articolo “Avvicinati e ascolta”\n"
                                           "     • Tornare alla pagina precedente\n     • Leggere l’articolo “Pace e speranza in Colombia”\n"
                                           "     • Tornare alla pagina precedente\n     • Leggere l’articolo “Piantare radici per salvaguardare il futuro           del caffè e del nostro pianeta”")
        elif self.type == 2:
            self.instruction.insert(tk.INSERT, "Istruzioni per il partecipante:\n\n 1.  Osservate la home page.\n\n 2.  Cercare nel menù di navigazione la voce “Cosa fare”\n\n"
                                               " 3.  Scegliete l’opzione “Natura” (per il sito della Spagna) / \n      “Attrazioni naturali imperdibili” ( per il sito della Norvegia).\n\n"
                                               " 4.  Scorrete fra i contenuti dell’intera pagina e cercate il \n       pulsante per prenotare un’esperienza a contatto con la \n      natura.")

        self.instruction.config(state='disabled')


def launch_browser(url, type, camera):
    #todo : handle different camera types for browser
    if camera == 'eye_tracker':
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
        root = tk.Toplevel()
        root.state("zoomed")
        app = MainFrame(root, url, type)
        # Tk must be initialized before CEF otherwise fatal error (Issue #306)
        cef.Initialize()
        app.mainloop()
        cef.Shutdown()
    else:
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
        root = tk.Toplevel()
        root.state("zoomed")
        app = MainFrame(root, url, type)
        # Tk must be initialized before CEF otherwise fatal error (Issue #306)
        cef.Initialize()
        app.mainloop()
        cef.Shutdown()

