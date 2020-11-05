#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.4),
    on ottobre 21, 2020, at 18:07
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""


from __future__ import absolute_import, division

from PyQt5 import QtWidgets

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

import cv2

def webcamRegistration() :

    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Store info about the experiment session
    psychopyVersion = '2020.2.4'
    expName = 'testVideo'  # from the Builder filename that created this script
    expInfo = {'participant': '', 'session': '001'}
    dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
                                     extraInfo=expInfo, runtimeInfo=None,
                                     originPath='C:\\Users\\matti\\OneDrive\\Desktop\\Tesi\\testVideo_lastrun.py',
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
        size=(1024, 768), fullscr=True, screen=0,
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

    # Initialize components for Routine "welcome"
    welcomeClock = core.Clock()
    WelcomeText = visual.TextStim(win=win, name='WelcomeText',
                                  text='This is a test to record your webcam.\n\nPress space when ready!\n',
                                  font='Arial',
                                  pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                                  color='white', colorSpace='rgb', opacity=1,
                                  languageStyle='LTR',
                                  depth=0.0);
    key_resp = keyboard.Keyboard()

    # Initialize components for Routine "WebcamRegistration"
    WebcamRegistrationClock = core.Clock()
    movie = visual.MovieStim3(
        win=win, name='movie',
        noAudio=False,
        filename='C:\\Users\\matti\\OneDrive\\Desktop\\Tesi\\video Test.mp4',
        ori=0, pos=(0, 0), opacity=1,
        loop=False,
        depth=0.0,
    )
    endVideo = keyboard.Keyboard()

    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

    # ------Prepare to start Routine "welcome"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # keep track of which components have finished
    welcomeComponents = [WelcomeText, key_resp]
    for thisComponent in welcomeComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    welcomeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "welcome"-------
    while continueRoutine:
        # get current time
        t = welcomeClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=welcomeClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *WelcomeText* updates
        if WelcomeText.status == NOT_STARTED and tThisFlip >= 1 - frameTolerance:
            # keep track of start time/frame for later
            WelcomeText.frameNStart = frameN  # exact frame index
            WelcomeText.tStart = t  # local t and not account for scr refresh
            WelcomeText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(WelcomeText, 'tStartRefresh')  # time at next scr refresh
            WelcomeText.setAutoDraw(True)

        # *key_resp* updates
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= 2 - frameTolerance:
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
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in welcomeComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "welcome"-------
    for thisComponent in welcomeComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('WelcomeText.started', WelcomeText.tStartRefresh)
    thisExp.addData('WelcomeText.stopped', WelcomeText.tStopRefresh)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys', key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
    thisExp.addData('key_resp.started', key_resp.tStartRefresh)
    thisExp.addData('key_resp.stopped', key_resp.tStopRefresh)
    thisExp.nextEntry()
    # the Routine "welcome" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ------Prepare to start Routine "WebcamRegistration"-------
    continueRoutine = True
    # update component parameters for each repeat
    endVideo.keys = []
    endVideo.rt = []
    _endVideo_allKeys = []
    # keep track of which components have finished
    WebcamRegistrationComponents = [movie, endVideo]
    for thisComponent in WebcamRegistrationComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    WebcamRegistrationClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "WebcamRegistration"-------
    while continueRoutine:
        # get current time
        t = WebcamRegistrationClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=WebcamRegistrationClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *movie* updates
        if movie.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            movie.frameNStart = frameN  # exact frame index
            movie.tStart = t  # local t and not account for scr refresh
            movie.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie, 'tStartRefresh')  # time at next scr refresh
            movie.setAutoDraw(True)

        # *endVideo* updates
        waitOnFlip = False
        if endVideo.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            endVideo.frameNStart = frameN  # exact frame index
            endVideo.tStart = t  # local t and not account for scr refresh
            endVideo.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(endVideo, 'tStartRefresh')  # time at next scr refresh
            endVideo.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(endVideo.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(endVideo.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if endVideo.status == STARTED and not waitOnFlip:
            theseKeys = endVideo.getKeys(keyList=['q'], waitRelease=False)
            _endVideo_allKeys.extend(theseKeys)
            if len(_endVideo_allKeys):
                endVideo.keys = _endVideo_allKeys[-1].name  # just the last key pressed
                endVideo.rt = _endVideo_allKeys[-1].rt
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in WebcamRegistrationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

        #####################VIDEO RECORDING#######################################################################################################

        cap = cv2.VideoCapture(0)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                #  frame = cv2.flip(frame,0)

                # write the flipped frame
                out.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    # -------Ending Routine "WebcamRegistration"-------
    for thisComponent in WebcamRegistrationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    movie.stop()
    # check responses
    if endVideo.keys in ['', [], None]:  # No response was made
        endVideo.keys = None
    thisExp.addData('endVideo.keys', endVideo.keys)
    if endVideo.keys != None:  # we had a response
        thisExp.addData('endVideo.rt', endVideo.rt)
    thisExp.addData('endVideo.started', endVideo.tStartRefresh)
    thisExp.addData('endVideo.stopped', endVideo.tStopRefresh)
    thisExp.nextEntry()
    # the Routine "WebcamRegistration" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

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
