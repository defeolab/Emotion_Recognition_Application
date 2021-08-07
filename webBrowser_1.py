from cefpython3 import cefpython as cef
import ctypes
import GSR.GSR_RECORD_SIGNAL.recordgsr as gsr

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


def launch_browser(url, type, id, window, old_root, frame, path=None, exptype=None):
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
    print('browser')
    #app = MainFrame(root, url, type, id, window, old_root, frame)
    rec = None
    if exptype == "gsr":
        rec = gsr.Record()
        rec.on_rec(path)

    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()
    #app.browser_frame.mainloop()
    cef.Shutdown()
