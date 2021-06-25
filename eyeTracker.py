#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.4),
    on novembre 01, 2020, at 11:28
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard
import threading
from screeninfo import get_monitors

###Titta imports
import pickle
import pandas as pd

import webBrowser
from titta import Titta, helpers_tobii as helpers
import os

import tkinter as tk
import videoPlayer as vp


def runexpGiulia(participantId):
    print(participantId)
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    SCREEN_RES = [tmp[0].width, tmp[0].height]
    SCREEN_WIDTH = 52.7  # cm
    VIEWING_DIST = 63  # distance from eye to center of screen (cm)
    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
    mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)
    im_name = 'beer_positioning.jpg'

    # %%  ET settings
    et_name = 'Tobii T60'
    dummy_mode = False
    bimonocular_calibration = False

    settings = Titta.get_defaults(et_name)
    settings.FILENAME = 'data/giulia/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    print(settings.FILENAME)
    settings.N_CAL_TARGETS = 3

    tracker = Titta.Connect(settings)

    if dummy_mode:
        tracker.set_dummy_mode()
    tracker.init()

    # Window set-up (this color will be used for calibration)

    win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                        screen=1, size=SCREEN_RES, units='deg')
    fixation_point = helpers.MyDot2(win)
    image = visual.ImageStim(win, image=im_name, units='norm', size=(2, 2))

    #  Calibrate
    """if bimonocular_calibration:
        tracker.calibrate(win, eye='left', calibration_number='first')
        tracker.calibrate(win, eye='right', calibration_number='second')
    else:
        tracker.calibrate(win)"""
    tracker.calibrate(win)

    tracker.start_recording(gaze_data=True, store_data=True)
    # Present fixation dot and wait for one second
    for i in range(monitor_refresh_rate):
        if i == 0:
            tracker.send_message('fix on')
        fixation_point.draw()
        win.flip()
    tracker.send_message('fix off')

    # Wait exactly 3 * fps frames (3 s)

    for i in range(30 * monitor_refresh_rate):
        if i == 0:
            tracker.send_message(''.join(['stim on: ', im_name]))
        image.draw()
        t = win.flip()
    tracker.send_message(''.join(['stim off: ', im_name]))
    win.flip()

    tracker.stop_recording(gaze_data=True)

    # Close window and save data

    win.close()
    tracker.save_data(mon)  # Also save screen geometry from the monitor object

    # %% Open pickle and write et-data and messages to tsv-files.

    f = open(settings.FILENAME[:-4] + '.pkl', 'rb')
    gaze_data = pickle.load(f)
    msg_data = pickle.load(f)
    #  Save data and messages
    df = pd.DataFrame(gaze_data, columns=tracker.header)
    df.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')
    df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
    df_msg.to_csv(settings.FILENAME[:-4] + '_msg.tsv', sep='\t')


def runexpAlessia(participantId):

    print(participantId)
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    SCREEN_RES = [tmp[0].width, tmp[0].height]
    SCREEN_WIDTH = 52.7  # cm
    VIEWING_DIST = 63  # distance from eye to center of screen (cm) #TODO : measure the actual distance
    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
    mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)

    # %%  ET settings
    et_name = 'Tobii T60'
    dummy_mode = False
    bimonocular_calibration = False

    settings = Titta.get_defaults(et_name)
    settings.FILENAME = 'data/alessia/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    #settings.FILENAME = 'testfile.tsv'
    print(settings.FILENAME)
    settings.N_CAL_TARGETS = 3

    tracker = Titta.Connect(settings)

    if dummy_mode:
        tracker.set_dummy_mode()
    tracker.init()

    # Window set-up (this color will be used for calibration)

    win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                        screen=1, size=SCREEN_RES, units='deg')
    fixation_point = helpers.MyDot2(win)
    #image = visual.ImageStim(win, image=im_name, units='norm', size=(2, 2)) #video instead?

    tracker.calibrate(win)
    win.close()
    tracker.start_recording(gaze_data=True, store_data=True)

    def createVideoFrame():
        top = tk.Toplevel()
        top.title("Experiment VLC media player")
        top.state('zoomed')
        player = None
        player = vp.Player(top, title="tkinter vlc")

        def closeTop():
            player.OnStop()
            player.quit()
            top.destroy()

            #save file
            tracker.stop_recording(gaze_data=True)
            # Close window and save data
            tracker.save_data(mon)  # Also save screen geometry from the monitor object
            # %% Open pickle and write et-data and messages to tsv-files.
            f = open(settings.FILENAME[:-4] + '.pkl', 'rb')
            gaze_data = pickle.load(f)
            msg_data = pickle.load(f)
            #  Save data and messages
            df = pd.DataFrame(gaze_data, columns=tracker.header)
            df.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')
            df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
            df_msg.to_csv(settings.FILENAME[:-4] + '_msg.tsv', sep='\t')
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")

        top.protocol("WM_DELETE_WINDOW", closeTop)

        def pause():
            player.OnPause()

        top.bind('<space>', pause)

    createVideoFrame()


def runexpBrowser(participantId, type):  # type parameter : 1 for Camilla, 2 for Chiara
    print(participantId)
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    SCREEN_RES = [tmp[0].width, tmp[0].height]
    SCREEN_WIDTH = 52.7  # cm
    VIEWING_DIST = 63  # distance from eye to center of screen (cm)
    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
    mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)

    # %%  ET settings
    et_name = 'Tobii T60'
    dummy_mode = False

    settings = Titta.get_defaults(et_name)
    if type == 1:
        settings.FILENAME = 'data/camilla/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    else:
        settings.FILENAME = 'data/chiara/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    print(settings.FILENAME)
    settings.N_CAL_TARGETS = 3

    tracker = Titta.Connect(settings)

    if dummy_mode:
        tracker.set_dummy_mode()
    tracker.init()

    # Window set-up (this color will be used for calibration)
    win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                        screen=1, size=SCREEN_RES, units='deg')
    fixation_point = helpers.MyDot2(win)

    tracker.calibrate(win)
    win.close()
    tracker.start_recording(gaze_data=True, store_data=True)

    if(type == 1):
        webBrowser.launch_browser("https://www.lavazza.it/it.html", 1)
    else:
        webBrowser.launch_browser("https://www.spain.info/it/", 2)

    tracker.stop_recording(gaze_data=True)
    tracker.save_data(mon)  # Also save screen geometry from the monitor object

    # %% Open pickle and write et-data and messages to tsv-files.

    f = open(settings.FILENAME[:-4] + '.pkl', 'rb')
    gaze_data = pickle.load(f)
    msg_data = pickle.load(f)
    #  Save data and messages
    df = pd.DataFrame(gaze_data, columns=tracker.header)
    #df.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')
    df.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')
    df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
    df_msg.to_csv(settings.FILENAME[:-4] + '_msg.tsv', sep='\t')

    print("saved")