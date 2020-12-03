#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2020.2.4),
    on novembre 12, 2020, at 18:16
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

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

def runExp(participantId):

    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    # Store info about the experiment session
    psychopyVersion = '2020.2.4'
    expName = 'ExpClinical'  # from the Builder filename that created this script
    expInfo = {'participant': participantId, 'session': '001'}
    #dlg = gui.DlgFromDict(dictionary=expInfo, sort_keys=False, title=expName)
    #if dlg.OK == False:
    #    core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName
    expInfo['psychopyVersion'] = psychopyVersion

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s/%s_%s_%s' % (expInfo['participant'],expInfo['participant'], expName, expInfo['date'])

    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
                                     extraInfo=expInfo, runtimeInfo=None,
                                     originPath='C:\\Users\\matti\\OneDrive\\Desktop\\Tesi\\ExpClinical_lastrun.py',
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

    # Initialize components for Routine "Introduction"
    IntroductionClock = core.Clock()
    text = visual.TextStim(win=win, name='text',
                           text='The experiment is starting.\n\nPress the spacebar when you are ready!',
                           font='Arial',
                           pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1,
                           languageStyle='LTR',
                           depth=0.0);
    key_resp_2 = keyboard.Keyboard()

    # Initialize components for Routine "ShowImage"
    ShowImageClock = core.Clock()
    image = visual.ImageStim(
        win=win,
        name='image',
        image='sin', mask=None,
        ori=0, pos=(0, 0), size=None,
        color=[1, 1, 1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)
    key_resp = keyboard.Keyboard()
    mouse_2 = event.Mouse(win=win)
    x, y = [None, None]
    mouse_2.mouseClock = core.Clock()

    # Initialize components for Routine "Gert"
    GertClock = core.Clock()
    happiness = visual.Polygon(
        win=win, name='happiness',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(0.23, 0.32),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)
    neutral = visual.Polygon(
        win=win, name='neutral',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(0.43, 0.02),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-1.0, interpolate=True)
    surprise = visual.Polygon(
        win=win, name='surprise',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(0.31, -0.30),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-2.0, interpolate=True)
    fear = visual.Polygon(
        win=win, name='fear',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(-0.05, -0.35),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-3.0, interpolate=True)
    sadness = visual.Polygon(
        win=win, name='sadness',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(-0.37, -0.20),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-4.0, interpolate=True)
    disgust = visual.Polygon(
        win=win, name='disgust',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(-0.4, 0.12),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-5.0, interpolate=True)
    anger = visual.Polygon(
        win=win, name='anger',
        edges=1000, size=(0.25, 0.25),
        ori=0, pos=(-0.15, 0.35),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-6.0, interpolate=True)
    text_happiness = visual.TextStim(win=win, name='text_happiness',
                                     text='Happiness',
                                     font='Arial',
                                     pos=(0.23, 0.32), height=0.05, wrapWidth=None, ori=0,
                                     color='black', colorSpace='rgb', opacity=1,
                                     languageStyle='LTR',
                                     depth=-7.0);
    text_neutral = visual.TextStim(win=win, name='text_neutral',
                                   text='Neutral',
                                   font='Arial',
                                   pos=(0.43, 0.02), height=0.05, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-8.0);
    text_surprise = visual.TextStim(win=win, name='text_surprise',
                                    text='Surprise',
                                    font='Arial',
                                    pos=(0.31, -0.30), height=0.05, wrapWidth=None, ori=0,
                                    color='black', colorSpace='rgb', opacity=1,
                                    languageStyle='LTR',
                                    depth=-9.0);
    text_fear = visual.TextStim(win=win, name='text_fear',
                                text='Fear',
                                font='Arial',
                                pos=(-0.05, -0.35), height=0.05, wrapWidth=None, ori=0,
                                color='black', colorSpace='rgb', opacity=1,
                                languageStyle='LTR',
                                depth=-10.0);
    text_sadness = visual.TextStim(win=win, name='text_sadness',
                                   text='Sadness',
                                   font='Arial',
                                   pos=(-0.37, -0.20), height=0.05, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-11.0);
    text_disgust = visual.TextStim(win=win, name='text_disgust',
                                   text='Disgust',
                                   font='Arial',
                                   pos=(-0.4, 0.12), height=0.05, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-12.0);
    text_anger = visual.TextStim(win=win, name='text_anger',
                                 text='Anger',
                                 font='Arial',
                                 pos=(-0.15, 0.35), height=0.05, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-13.0);
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()

    # Initialize components for Routine "End"
    EndClock = core.Clock()
    text_2 = visual.TextStim(win=win, name='text_2',
                             text='End',
                             font='Arial',
                             pos=(0, 0), height=0.4, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             languageStyle='LTR',
                             depth=0.0);
    text_3 = visual.TextStim(win=win, name='text_3',
                             text='Press spacebar to exit',
                             font='Arial',
                             pos=(0, -0.3), height=0.05, wrapWidth=None, ori=0,
                             color='white', colorSpace='rgb', opacity=1,
                             languageStyle='LTR',
                             depth=0.0);
    key_resp_3 = keyboard.Keyboard()

    # Create some handy timers
    globalClock = core.Clock()  # to track the time since experiment started
    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

    # ------Prepare to start Routine "Introduction"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # keep track of which components have finished
    IntroductionComponents = [text, key_resp_2]
    for thisComponent in IntroductionComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    IntroductionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "Introduction"-------
    while continueRoutine:
        # get current time
        t = IntroductionClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=IntroductionClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *text* updates
        if text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            text.setAutoDraw(True)

        # *key_resp_2* updates
        waitOnFlip = False
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
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
        for thisComponent in IntroductionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "Introduction"-------
    for thisComponent in IntroductionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('text.started', text.tStartRefresh)
    thisExp.addData('text.stopped', text.tStopRefresh)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    thisExp.addData('key_resp_2.keys', key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
    thisExp.addData('key_resp_2.started', key_resp_2.tStartRefresh)
    thisExp.addData('key_resp_2.stopped', key_resp_2.tStopRefresh)
    thisExp.nextEntry()
    # the Routine "Introduction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=1, method='random',
                               extraInfo=expInfo, originPath=-1,
                               trialList=data.importConditions('ClinicalImages.csv'),
                               seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)

    RelativePath = ''

    if thisTrial != None:
        #for paramName in thisTrial:
        #    exec('{} = thisTrial[paramName]'.format(paramName))
        RelativePath = thisTrial['RelativePath']


    nImageShowed = 0

    for thisTrial in trials:

        if(nImageShowed == 5):
            break;

        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            #for paramName in thisTrial:
            #    exec('{} = thisTrial[paramName]'.format(paramName))
            RelativePath = thisTrial['RelativePath']

        # ------Prepare to start Routine "ShowImage"-------
        continueRoutine = True
        # update component parameters for each repeat
        image.setImage(RelativePath)
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # setup some python lists for storing info about the mouse_2
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        ShowImageComponents = [image, key_resp, mouse_2]
        for thisComponent in ShowImageComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        ShowImageClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1

        # -------Run Routine "ShowImage"-------
        while continueRoutine:
            # get current time
            t = ShowImageClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=ShowImageClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *image* updates
            if image.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                image.setAutoDraw(True)

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
            # *mouse_2* updates
            if mouse_2.status == NOT_STARTED and t >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                mouse_2.frameNStart = frameN  # exact frame index
                mouse_2.tStart = t  # local t and not account for scr refresh
                mouse_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse_2, 'tStartRefresh')  # time at next scr refresh
                mouse_2.status = STARTED
                mouse_2.mouseClock.reset()
                prevButtonState = mouse_2.getPressed()  # if button is down already this ISN'T a new click
            if mouse_2.status == STARTED:  # only update if started and not finished!
                buttons = mouse_2.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        continueRoutine = False
                        # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                win.close()
                core.quit()

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ShowImageComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "ShowImage"-------
        for thisComponent in ShowImageComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('image.started', image.tStartRefresh)
        trials.addData('image.stopped', image.tStopRefresh)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        trials.addData('key_resp.keys', key_resp.keys)
        if key_resp.keys != None:  # we had a response
            trials.addData('key_resp.rt', key_resp.rt)
        trials.addData('key_resp.started', key_resp.tStartRefresh)
        trials.addData('key_resp.stopped', key_resp.tStopRefresh)
        # store data for trials (TrialHandler)
        trials.addData('mouse_2.started', mouse_2.tStart)
        trials.addData('mouse_2.stopped', mouse_2.tStop)
        # the Routine "ShowImage" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # ------Prepare to start Routine "Gert"-------
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the mouse
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        # keep track of which components have finished
        GertComponents = [happiness, neutral, surprise, fear, sadness, disgust, anger, text_happiness, text_neutral,
                          text_surprise, text_fear, text_sadness, text_disgust, text_anger, mouse]
        for thisComponent in GertComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        GertClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1

        # -------Run Routine "Gert"-------
        while continueRoutine:
            # get current time
            t = GertClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=GertClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *happiness* updates
            if happiness.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                happiness.frameNStart = frameN  # exact frame index
                happiness.tStart = t  # local t and not account for scr refresh
                happiness.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(happiness, 'tStartRefresh')  # time at next scr refresh
                happiness.setAutoDraw(True)

            # *neutral* updates
            if neutral.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                neutral.frameNStart = frameN  # exact frame index
                neutral.tStart = t  # local t and not account for scr refresh
                neutral.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(neutral, 'tStartRefresh')  # time at next scr refresh
                neutral.setAutoDraw(True)

            # *surprise* updates
            if surprise.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                surprise.frameNStart = frameN  # exact frame index
                surprise.tStart = t  # local t and not account for scr refresh
                surprise.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(surprise, 'tStartRefresh')  # time at next scr refresh
                surprise.setAutoDraw(True)

            # *fear* updates
            if fear.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                fear.frameNStart = frameN  # exact frame index
                fear.tStart = t  # local t and not account for scr refresh
                fear.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fear, 'tStartRefresh')  # time at next scr refresh
                fear.setAutoDraw(True)

            # *sadness* updates
            if sadness.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                sadness.frameNStart = frameN  # exact frame index
                sadness.tStart = t  # local t and not account for scr refresh
                sadness.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(sadness, 'tStartRefresh')  # time at next scr refresh
                sadness.setAutoDraw(True)

            # *disgust* updates
            if disgust.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                disgust.frameNStart = frameN  # exact frame index
                disgust.tStart = t  # local t and not account for scr refresh
                disgust.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(disgust, 'tStartRefresh')  # time at next scr refresh
                disgust.setAutoDraw(True)

            # *anger* updates
            if anger.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                anger.frameNStart = frameN  # exact frame index
                anger.tStart = t  # local t and not account for scr refresh
                anger.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(anger, 'tStartRefresh')  # time at next scr refresh
                anger.setAutoDraw(True)

            # *text_happiness* updates
            if text_happiness.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_happiness.frameNStart = frameN  # exact frame index
                text_happiness.tStart = t  # local t and not account for scr refresh
                text_happiness.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_happiness, 'tStartRefresh')  # time at next scr refresh
                text_happiness.setAutoDraw(True)

            # *text_neutral* updates
            if text_neutral.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_neutral.frameNStart = frameN  # exact frame index
                text_neutral.tStart = t  # local t and not account for scr refresh
                text_neutral.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_neutral, 'tStartRefresh')  # time at next scr refresh
                text_neutral.setAutoDraw(True)

            # *text_surprise* updates
            if text_surprise.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_surprise.frameNStart = frameN  # exact frame index
                text_surprise.tStart = t  # local t and not account for scr refresh
                text_surprise.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_surprise, 'tStartRefresh')  # time at next scr refresh
                text_surprise.setAutoDraw(True)

            # *text_fear* updates
            if text_fear.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_fear.frameNStart = frameN  # exact frame index
                text_fear.tStart = t  # local t and not account for scr refresh
                text_fear.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_fear, 'tStartRefresh')  # time at next scr refresh
                text_fear.setAutoDraw(True)

            # *text_sadness* updates
            if text_sadness.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_sadness.frameNStart = frameN  # exact frame index
                text_sadness.tStart = t  # local t and not account for scr refresh
                text_sadness.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_sadness, 'tStartRefresh')  # time at next scr refresh
                text_sadness.setAutoDraw(True)

            # *text_disgust* updates
            if text_disgust.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_disgust.frameNStart = frameN  # exact frame index
                text_disgust.tStart = t  # local t and not account for scr refresh
                text_disgust.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_disgust, 'tStartRefresh')  # time at next scr refresh
                text_disgust.setAutoDraw(True)

            # *text_anger* updates
            if text_anger.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_anger.frameNStart = frameN  # exact frame index
                text_anger.tStart = t  # local t and not account for scr refresh
                text_anger.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_anger, 'tStartRefresh')  # time at next scr refresh
                text_anger.setAutoDraw(True)
            # *mouse* updates
            if mouse.status == NOT_STARTED and t >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                mouse.status = STARTED
                mouse.mouseClock.reset()
                prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
            if mouse.status == STARTED:  # only update if started and not finished!
                buttons = mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        for obj in [happiness, neutral, surprise, fear, sadness, disgust, anger]:
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                        if gotValidClick:  # abort routine on response
                            continueRoutine = False

            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                win.close()
                core.quit()

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in GertComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "Gert"-------
        for thisComponent in GertComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('happiness.started', happiness.tStartRefresh)
        trials.addData('happiness.stopped', happiness.tStopRefresh)
        trials.addData('neutral.started', neutral.tStartRefresh)
        trials.addData('neutral.stopped', neutral.tStopRefresh)
        trials.addData('surprise.started', surprise.tStartRefresh)
        trials.addData('surprise.stopped', surprise.tStopRefresh)
        trials.addData('fear.started', fear.tStartRefresh)
        trials.addData('fear.stopped', fear.tStopRefresh)
        trials.addData('sadness.started', sadness.tStartRefresh)
        trials.addData('sadness.stopped', sadness.tStopRefresh)
        trials.addData('disgust.started', disgust.tStartRefresh)
        trials.addData('disgust.stopped', disgust.tStopRefresh)
        trials.addData('anger.started', anger.tStartRefresh)
        trials.addData('anger.stopped', anger.tStopRefresh)
        trials.addData('text_happiness.started', text_happiness.tStartRefresh)
        trials.addData('text_happiness.stopped', text_happiness.tStopRefresh)
        trials.addData('text_neutral.started', text_neutral.tStartRefresh)
        trials.addData('text_neutral.stopped', text_neutral.tStopRefresh)
        trials.addData('text_surprise.started', text_surprise.tStartRefresh)
        trials.addData('text_surprise.stopped', text_surprise.tStopRefresh)
        trials.addData('text_fear.started', text_fear.tStartRefresh)
        trials.addData('text_fear.stopped', text_fear.tStopRefresh)
        trials.addData('text_sadness.started', text_sadness.tStartRefresh)
        trials.addData('text_sadness.stopped', text_sadness.tStopRefresh)
        trials.addData('text_disgust.started', text_disgust.tStartRefresh)
        trials.addData('text_disgust.stopped', text_disgust.tStopRefresh)
        trials.addData('text_anger.started', text_anger.tStartRefresh)
        trials.addData('text_anger.stopped', text_anger.tStopRefresh)
        # store data for trials (TrialHandler)
        x, y = mouse.getPos()
        buttons = mouse.getPressed()
        if sum(buttons):
            # check if the mouse was inside our 'clickable' objects
            gotValidClick = False
            for obj in [happiness, neutral, surprise, fear, sadness, disgust, anger]:
                if obj.contains(mouse):
                    gotValidClick = True
                    mouse.clicked_name.append(obj.name)
        trials.addData('mouse.x', x)
        trials.addData('mouse.y', y)
        trials.addData('mouse.leftButton', buttons[0])
        trials.addData('mouse.midButton', buttons[1])
        trials.addData('mouse.rightButton', buttons[2])
        if len(mouse.clicked_name):
            trials.addData('mouse.clicked_name', mouse.clicked_name[0])
        trials.addData('mouse.started', mouse.tStart)
        trials.addData('mouse.stopped', mouse.tStop)
        # the Routine "Gert" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()

        nImageShowed += 1

    # completed 1 repeats of 'trials'


    # ------Prepare to start Routine "End"-------
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # keep track of which components have finished
    EndComponents = [text_2, text_3, key_resp_3]
    for thisComponent in EndComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    EndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "End"-------
    while continueRoutine:
        # get current time
        t = EndClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=EndClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *text_2* updates
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            text_2.setAutoDraw(True)

        # *text_3* updates
        if text_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            text_3.frameNStart = frameN  # exact frame index
            text_3.tStart = t  # local t and not account for scr refresh
            text_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_3, 'tStartRefresh')  # time at next scr refresh
            text_3.setAutoDraw(True)

        # *key_resp_3* updates
        waitOnFlip = False
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['space'], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
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
        for thisComponent in EndComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "End"-------
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('text_2.started', text_2.tStartRefresh)
    thisExp.addData('text_2.stopped', text_2.tStopRefresh)

    thisExp.addData('text_3.started', text_3.tStartRefresh)
    thisExp.addData('text_3.stopped', text_3.tStopRefresh)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys = None
    thisExp.addData('key_resp_3.keys', key_resp_3.keys)
    if key_resp_3.keys != None:  # we had a response
        thisExp.addData('key_resp_3.rt', key_resp_3.rt)
    thisExp.addData('key_resp_3.started', key_resp_3.tStartRefresh)
    thisExp.addData('key_resp_3.stopped', key_resp_3.tStopRefresh)
    thisExp.nextEntry()
    # the Routine "End" was not non-slip safe, so reset the non-slip timer
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
