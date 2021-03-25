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

###Titta imports
import pickle
import pandas as pd
from titta import Titta, helpers_tobii as helpers
import os

def runExp(participantId):
    # Ensure that relative paths start from the same directory as this scripta
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    im_name = 'Capture.PNG'

    # Store info about the experiment session
    psychopyVersion = '2020.2.4'
    expName = 'ExpGiulia'  # from the Builder filename that created this script
    expInfo = {'participant': participantId, 'session': '001'}

    #dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title=expName)
    #if dlg.OK == False:
    #    core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
    FULLSCREEN = True
    SCREEN_RES = [1920, 1080]
    SCREEN_WIDTH = 52.7  # cm
    VIEWING_DIST = 63  # distance from eye to center of screen (cm)

    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
    mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)

    et_name = 'Tobii T60'
    # et_name = 'IS4_Large_Peripheral'
    # et_name = 'Tobii Pro Nano'

    bimonocular_calibration = False
    dummy_mode = True

    # Change any of the default settings
    settings = Titta.get_defaults(et_name)
    settings.FILENAME = 'testfile.tsv'
    settings.N_CAL_TARGETS = 5

    tracker = Titta.Connect(settings)
    if dummy_mode:
        tracker.set_dummy_mode()
    tracker.init()

    win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                        screen=1, size=SCREEN_RES, units='deg')
    expInfo['frameRate'] = win.getActualFrameRate()

    #get fixation point
    fixation_point = helpers.MyDot2(win)
    image = visual.ImageStim(win, image=im_name, units='norm', size=(2, 2))

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s/%s_%s_%s' % (expInfo['participant'],expInfo['participant'], expName, expInfo['date'])
    print(filename)
    # An ExperimentHandler isn't essential but helps with data saving

    #  Calibrate
    if bimonocular_calibration:
        tracker.calibrate(win, eye='left', calibration_number='first')
        tracker.calibrate(win, eye='right', calibration_number='second')
    else:
        tracker.calibrate(win)

    # Record some data
    tracker.start_recording(gaze_data=True, store_data=True)
    """
    for i in range(expInfo['frameRate']):
        if i == 0:
            tracker.send_message('fix on')
        fixation_point.draw()
        t = win.flip()
    tracker.send_message('fix off')
    """
    # Wait exactly 3 * fps frames (3 s)
    for i in range(3 * monitor_refresh_rate):
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

    # Open pickle and write et-data and messages to tsv-files.
    f = open(settings.FILENAME[:-4] + '.pkl', 'rb')
    gaze_data = pickle.load(f)
    msg_data = pickle.load(f)

    #  Save data and messages
    df = pd.DataFrame(gaze_data, columns=tracker.header)
    df.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')
    df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
    df_msg.to_csv(settings.FILENAME[:-4] + '_msg.tsv', sep='\t')


def runExpp(participantId):
    # Ensure that relative paths start from the same directory as this scripta
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Store info about the experiment session
    psychopyVersion = '2020.2.4'
    expName = 'ExpGiulia'  # from the Builder filename that created this script
    expInfo = {'participant': participantId, 'session': '001'}

    #dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title=expName)
    #if dlg.OK == False:
    #    core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    # %%titta setup
    monitor_refresh_rate = 60  # frames per second (fps)
    mon = monitors.Monitor('testMonitor')  # Defined in defaults file
    """mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
    mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
    mon.setSizePix(SCREEN_RES)"""
    et_name = 'Tobii T60'
    dummy_mode = True
    bimonocular_calibration = False
    settings = Titta.get_defaults(et_name)
    settings.FILENAME = 'testfile.tsv'
    settings.N_CAL_TARGETS = 5  # change the duration of the calibration -- default : 0, 1, 3, 5, 9, 13

    #Connect to eye tracker and calibrate
    tracker = Titta.Connect(settings)
    if dummy_mode:
        tracker.set_dummy_mode()
    tracker.init()

    endExpNow = False  # flag for 'escape' or other condition => quit the exp

    win = visual.Window(
        size=(1280, 1024), fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')
    expInfo['frameRate'] = win.getActualFrameRate()

    """"# create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard()
    # Initialize components for Routine "trial"
    trialClock = core.Clock()"""

    # %%

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s/%s_%s_%s' % (expInfo['participant'],expInfo['participant'], expName, expInfo['date'])
    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
                                     extraInfo=expInfo, runtimeInfo=None,
                                     savePickle=True, saveWideText=True,
                                     dataFileName=filename)

    # save a log file for detail verbose info
    logFile = logging.LogFile(filename + '.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001  # how close to onset before 'same' frame

    # Start Code - component code to be run before the window creation

    # Setup the Window
    win = visual.Window(
        size=(1280, 1024), fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')
    # store frame rate of monitor if we can measure it
    expInfo['frameRate'] = win.getActualFrameRate()

    if expInfo['frameRate'] != None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    # create a default keyboard (e.g. to check for escape)
    defaultKeyboard = keyboard.Keyboard()

    # Initialize components for Routine "trial"
    trialClock = core.Clock()

    welcomeText = visual.TextStim(win=win, name='welcomeText',
                                  text='Welcome to this experiment.\n\nPress the spacebar when you are ready and the video will start!',
                                  font='Arial',
                                  pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                  color='white', colorSpace='rgb', opacity=1,
                                  languageStyle='LTR',
                                  depth=0.0)

    key_resp = keyboard.Keyboard()



    # Initialize components for Routine "Video"
    VideoClock = core.Clock()
    video = visual.MovieStim3(
        win=win, name='video',
        noAudio=False,
        filename='videos/filmato_Alessia.mp4',
        ori=0, pos=(0, 0), opacity=1,
        loop=False,
        depth=0.0,
    )

    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    trialComponents = [welcomeText, key_resp]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *welcomeText* updates
        if welcomeText.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            welcomeText.frameNStart = frameN  # exact frame index
            welcomeText.tStart = t  # local t and not account for scr refresh
            welcomeText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcomeText, 'tStartRefresh')  # time at next scr refresh
            welcomeText.setAutoDraw(True)

        # *key_resp* updates
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            win.close()
            core.quit()


        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('welcomeText.started', welcomeText.tStartRefresh)
    thisExp.addData('welcomeText.stopped', welcomeText.tStopRefresh)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys', key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
    thisExp.addData('key_resp.started', key_resp.tStartRefresh)
    thisExp.addData('key_resp.stopped', key_resp.tStopRefresh)
    thisExp.nextEntry()
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "Video"-------
    continueRoutine = True
    # update component parameters for each repeat
    # keep track of which components have finished
    """VideoComponents = [video]
    for thisComponent in VideoComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    VideoClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1"""

    ##titta part
    fixation_point = helpers.MyDot2(win)

    if bimonocular_calibration:
        tracker.calibrate(win, eye='left', calibration_number='first')
        tracker.calibrate(win, eye='right', calibration_number='second')
    else:
        tracker.calibrate(win)

    # %% Record some data
    tracker.start_recording(gaze_data=True, store_data=True)

    # Present fixation dot and wait for one second
    for i in range(monitor_refresh_rate):
        if i == 0:
            tracker.send_message('fix on')
        fixation_point.draw()
        t = win.flip()
    tracker.send_message('fix off')


    """
    # -------Run Routine "Video"-------
    while continueRoutine:
        # get current time
        t = VideoClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=VideoClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *video* updates
        if video.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            video.frameNStart = frameN  # exact frame index
            video.tStart = t  # local t and not account for scr refresh
            video.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(video, 'tStartRefresh')  # time at next scr refresh
            video.setAutoDraw(True)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            win.close()
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in VideoComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Video"-------
    for thisComponent in VideoComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    video.stop()"""

    tracker.stop_recording(gaze_data=True)
    tracker.save_data(mon)

    bs = r"\""
    # %% Open pickle and write et-data and messages to tsv-files.
    print(os.path.dirname(os.path.realpath(__file__)) + bs + settings.FILENAME[:-4] + '.pkl')
    # os.makedirs(os.path.dirname(os.path.realpath(__file__))+ bs + settings.FILENAME[:-4] + '.pkl', exist_ok=True)
    f = open(os.path.dirname(os.path.realpath(__file__)) + '/' + settings.FILENAME[:-4] + '.pkl', 'rb')
    gaze_data = pickle.load(f)
    msg_data = pickle.load(f)

    #  Save data and messages
    df = pd.DataFrame(gaze_data, columns=tracker.header)
    df.to_csv(os.path.dirname(os.path.realpath(__file__)) + bs + settings.FILENAME[:-4] + '.tsv', sep='\t')
    df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
    df_msg.to_csv(os.path.dirname(os.path.realpath(__file__)) + bs + settings.FILENAME[:-4] + '_msg.tsv', sep='\t')

    # Flip one final time so any remaining win.callOnFlip()
    # and win.timeOnFlip() tasks get executed before quitting
    win.flip()

    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    win.close()
    core.quit()
    logging.flush()

    for thisThread in threading.enumerate():
        if hasattr(thisThread, 'stop') and hasattr(thisThread, 'running'):
            # this is one of our event threads - kill it and wait for success
            thisThread.stop()
            while thisThread.running == 0:
                pass  # wait until it has properly finished polling

    sys.exit(1)  # quits the python session entirely


