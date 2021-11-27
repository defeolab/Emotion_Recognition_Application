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

import json

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
from PIL import Image, ImageTk
from tkinter import filedialog
###Titta imports
import pickle
import pandas as pd
import time

import GSR_rec
import ScreenRecording
import ffmpeg_video_audio
import webBrowser
import webInstruction
from titta import Titta, helpers_tobii as helpers
import os

import tkinter as tk
import videoPlayer as vp
import GSR.GSR_RECORD_SIGNAL.recordgsr as gsr
#import postprocessing


def runexpImage(participantId):
    print(participantId)
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    #print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    #SCREEN_RES = [tmp[1].width, tmp[1].height]
    #SCREEN_WIDTH = tmp[1].width  # cm
    SCREEN_RES = [1280, 1024]
    SCREEN_WIDTH = 33.8  # cm
    VIEWING_DIST = 63  # distance from eye to center of screen (cm)
    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
    mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)
    im_name = os.getcwd() + "/Image/beer_positioning.jpg"

    #im_name = filedialog.askopenfilename(initialdir=os.getcwd() + "/Image/")

    # %%  ET settings
    et_name = 'Tobii T60'
    dummy_mode = False
    bimonocular_calibration = False

    settings = Titta.get_defaults(et_name)
    settings.FILENAME = 'data/Image/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    GSRpath = 'data/Image/' + str(participantId) + '/GSR_data/'
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
    #rec = gsr.Record()
    #rec.on_rec(GSRpath)

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

    #rec.on_stop()
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

class run_video_experiment:
    def __init__(self,search_key_var, type, participantId, parent, root, frame):
        self.website = search_key_var
        self.type = type
        self.id = participantId
        self.parent = parent
        self.root = root
        self.frame = frame
        #self.cal = cal
        self.MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
        self.FULLSCREEN = True
        # SCREEN_RES = [tmp[0].width, tmp[0].height]
        # SCREEN_WIDTH = 52.7  # cm
        self.SCREEN_RES = [1280, 1024]
        self.SCREEN_WIDTH = 33.8  # cm
        self.VIEWING_DIST = 63  # distance from eye to center of screen (cm) #TODO : measure the actual distance
        self.monitor_refresh_rate = 60  # frames per second (fps)
        self.mon = monitors.Monitor(self.MY_MONITOR)  # Defined in defaults file
        self.mon.setWidth(self.SCREEN_WIDTH)  # Width of screen (cm)
        self.mon.setDistance(self.VIEWING_DIST)  # Distance eye / monitor (cm)
        self.mon.setSizePix(self.SCREEN_RES)

        # %%  ET settings
        self.et_name = 'Tobii T60'
        self.dummy_mode = False
        bimonocular_calibration = False

        self.settings = Titta.get_defaults(self.et_name)
        self.settings.FILENAME = 'data/Browser/' + str(self.id) + '/' + data.getDateStr() + '_web' + str(self.type) + '.tsv'
        print(self.settings.FILENAME)
        self.settings.N_CAL_TARGETS = 3

        self.tracker = Titta.Connect(self.settings)

    def runexpweb(self):
        #self.tmp = get_monitors()
        #self.new_width = self.tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
        #self.new_height = self.tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
        #print("Schermo rilevato: " + str(self.new_width) + " x " + str(self.new_height))

        if self.dummy_mode:
            self.tracker.set_dummy_mode()
        self.tracker.init()

        # Window set-up (this color will be used for calibration)

        win = visual.Window(monitor=self.mon, fullscr=self.FULLSCREEN,
                            screen=1, size=self.SCREEN_RES, units='deg')
        fixation_point = helpers.MyDot2(win)

        self.tracker.calibrate(win)
        win.close()
        cal_tracker = self.tracker
        #return cal_tracker

        fp = open('websites.txt', 'r')
        self.websites = json.load(fp)
        fp.close()
        if self.type == 1:
            webInstruction.launch_browser(self.websites['website5'], 1, self.id, self.parent, self.root, True, cal_tracker = cal_tracker)
        elif self.type == 2:
            webInstruction.launch_browser(self.websites['website5'], 2, self.id, self.parent, self.root, True, cal_tracker=cal_tracker)
        elif self.type == 3:
            webInstruction.launch_browser(self.websites['website5'], 3, self.id, self.parent, self.root, True, cal_tracker=cal_tracker)
        elif self.type == 4:
            webInstruction.launch_browser(self.websites['website5'], 4, self.id, self.parent, self.root, True, cal_tracker=cal_tracker)

    def start_exp_rec(self, cal_tracker):
        self.tracker = cal_tracker
        self.tracker.start_recording(gaze_data=True, store_data=True)


    def stop_exp_rec(self, cal_tracker):
        self.tracker = cal_tracker
        self.tracker.stop_recording(gaze_data=True)
        self.tracker.save_data(self.mon)  # Also save screen geometry from the monitor object

        # %% Open pickle and write et-data and messages to tsv-files.
        file_path = "data/Browser/" + str(self.id) + "/"
        for file in os.listdir(file_path):
            if file.endswith(".pkl"):
                print(file)
                f = open(file_path + file, "rb")

        #f = open(self.settings.FILENAME[:-4] + '.pkl', 'rb')
        #data = pickle.load(open(file_path, "rb"))
        # loads : get the data from var
        #data = pickle.load(var)
        #f = open(self.settings.FILENAME[:-4] + '.pkl', 'rb')
        gaze_data = pickle.load(f)
        msg_data = pickle.load(f)
        #  Save data and messages
        df = pd.DataFrame(gaze_data, columns=self.tracker.header)
        df.to_csv(self.settings.FILENAME[:-4] + '.tsv', sep='\t')
        df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
        df_msg.to_csv(self.settings.FILENAME[:-4] + '_msg.tsv', sep='\t')

        print("saved")


'''class start_browser_recording:
    def __init__(self, cal_tracker, settings, mom):

    def start_exp_rec(self, cal_tracker):
        self.tracker = cal_tracker
        self.tracker.start_recording(gaze_data=True, store_data=True)

        def createVideoFrame():
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            player = None
            player = vp.Player(top, title="tkinter vlc")  # no gsr recorded this way

            def closeTop():
                player.OnStop()
                player.quit()
                top.destroy()

                # save file
                self.tracker.stop_recording(gaze_data=True)
                # Close window and save data
                self.tracker.save_data(self.mon)  # Also save screen geometry from the monitor object

                # %% Open pickle and write et-data and messages to tsv-files.
                f = open(self.settings.FILENAME[:-4] + '.pkl', 'rb')
                gaze_data = pickle.load(f)
                msg_data = pickle.load(f)

                #  Save data and messages
                df = pd.DataFrame(gaze_data, columns=self.tracker.header)
                df.to_csv(self.settings.FILENAME[:-4] + '.tsv', sep='\t')
                df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
                df_msg.to_csv(self.settings.FILENAME[:-4] + '_msg.tsv', sep='\t')
                # postprocessing.process(settings.FILENAME)
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")

            top.protocol("WM_DELETE_WINDOW", closeTop)

            def pause():
                player.OnPause()

            top.bind('<space>', pause)

        createVideoFrame()

'''

def runexpVideo(participantId):
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    #SCREEN_RES = [tmp[0].width, tmp[0].height]
    #SCREEN_WIDTH = 52.7  # cm
    SCREEN_RES = [1280, 1024]
    SCREEN_WIDTH = 33.8  # cm
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
    settings.FILENAME = 'data/Video/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
    GSRpath = 'data/Video/' + str(participantId) + '/GSR_data/'
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

    def createVideoFrame():
        top = tk.Toplevel()
        top.title("Experiment VLC media player")
        top.state('zoomed')
        player = None
        player = vp.Player(top, title="tkinter vlc") #no gsr recorded this way

        def closeTop():
            player.OnStop()
            player.quit()
            top.destroy()

            # save file
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
            #postprocessing.process(settings.FILENAME)
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")

        top.protocol("WM_DELETE_WINDOW", closeTop)

        def pause():
            player.OnPause()

        top.bind('<space>', pause)

    createVideoFrame()

'''def runexpBrowser(search_key_var, type, participantId, parent, root, frame):
    tmp = get_monitors()
    new_width = tmp[0].width  # 0 for resolution of main screen, 1 for resolution of the second screen
    new_height = tmp[0].height  # 0 for resolution of main screen, 1 for resolution of the second screen
    print("Schermo rilevato: " + str(new_width) + " x " + str(new_height))

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    #SCREEN_RES = [tmp[0].width, tmp[0].height]
    #SCREEN_WIDTH = 52.7  # cm
    SCREEN_RES = [1280, 1024]
    SCREEN_WIDTH = 33.8  # cm
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
        settings.FILENAME = 'data/Browser/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
        GSRpath = 'data/Browser/' + str(participantId) + '/GSR_data/'
    else:
        settings.FILENAME = 'data/Browser/' + str(participantId) + '/' + data.getDateStr() + '.tsv'
        GSRpath = 'data/Browser/' + str(participantId) + '/GSR_data/'
    sec = 30
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
    webInstruction.launch_browser(search_key_var, type, participantId, parent, root, frame = frame)

    tracker.stop_recording(gaze_data=True)
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

    print("saved")'''
