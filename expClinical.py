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
                                     originPath=os.getcwd(),
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
    excited = visual.Polygon(
        win=win, name='excited',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.10, 0.38),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=0.0, interpolate=True)
    delighted = visual.Polygon(
        win=win, name='delighted',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.30, 0.25),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-1.0, interpolate=True)
    happy = visual.Polygon(
        win=win, name='happy',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.47, 0.1),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-2.0, interpolate=True)
    content = visual.Polygon(
        win=win, name='content',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.47, -0.1),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-3.0, interpolate=True)
    relaxed = visual.Polygon(
        win=win, name='relaxed',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.30, -0.25),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-4.0, interpolate=True)
    calm = visual.Polygon(
        win=win, name='calm',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(0.10, -0.38),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-5.0, interpolate=True)
    tired = visual.Polygon(
        win=win, name='tired',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.10, -0.38),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-6.0, interpolate=True)
    bored = visual.Polygon(
        win=win, name='bored',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.30, -0.25),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-7.0, interpolate=True)
    depressed = visual.Polygon(
        win=win, name='depressed',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.47, -0.1),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-8.0, interpolate=True)
    frustrated = visual.Polygon(
        win=win, name='frustrated',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.47, 0.1),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-9.0, interpolate=True)
    angry = visual.Polygon(
        win=win, name='angry',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.30, 0.25),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-10.0, interpolate=True)
    tense = visual.Polygon(
        win=win, name='tense',
        edges=1000, size=(0.18, 0.18),
        ori=0, pos=(-0.10, 0.38),
        lineWidth=1, lineColor=[1, 1, 1], lineColorSpace='rgb',
        fillColor=[1, 1, 1], fillColorSpace='rgb',
        opacity=1, depth=-11.0, interpolate=True)
    text_excited = visual.TextStim(win=win, name='text_excited',
                                   text='Excited',
                                   font='Arial',
                                   pos=(0.10, 0.38), height=0.04, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-12.0);
    text_delighted = visual.TextStim(win=win, name='text_delighted',
                                     text='Delighted',
                                     font='Arial',
                                     pos=(0.30, 0.25), height=0.035, wrapWidth=None, ori=0,
                                     color='black', colorSpace='rgb', opacity=1,
                                     languageStyle='LTR',
                                     depth=-13.0);
    text_happy = visual.TextStim(win=win, name='text_happy',
                                 text='Happy',
                                 font='Arial',
                                 pos=(0.47, 0.1), height=0.04, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-14.0);
    text_content = visual.TextStim(win=win, name='text_content',
                                   text='Content',
                                   font='Arial',
                                   pos=(0.47, -0.1), height=0.04, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-15.0);
    text_relaxed = visual.TextStim(win=win, name='text_relaxed',
                                   text='Relaxed',
                                   font='Arial',
                                   pos=(0.30, -0.25), height=0.04, wrapWidth=None, ori=0,
                                   color='black', colorSpace='rgb', opacity=1,
                                   languageStyle='LTR',
                                   depth=-16.0);
    text_calm = visual.TextStim(win=win, name='text_calm',
                                text='Calm',
                                font='Arial',
                                pos=(0.10, -0.38), height=0.04, wrapWidth=None, ori=0,
                                color='black', colorSpace='rgb', opacity=1,
                                languageStyle='LTR',
                                depth=-17.0);
    text_tired = visual.TextStim(win=win, name='text_tired',
                                 text='Tired',
                                 font='Arial',
                                 pos=(-0.10, -0.38), height=0.04, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-18.0);
    text_bored = visual.TextStim(win=win, name='text_bored',
                                 text='Bored',
                                 font='Arial',
                                 pos=(-0.30, -0.25), height=0.04, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-19.0);
    text_depressed = visual.TextStim(win=win, name='text_depressed',
                                     text='Depressed',
                                     font='Arial',
                                     pos=(-0.47, -0.1), height=0.035, wrapWidth=None, ori=0,
                                     color='black', colorSpace='rgb', opacity=1,
                                     languageStyle='LTR',
                                     depth=-20.0);
    text_frustrated = visual.TextStim(win=win, name='text_frustrated',
                                      text='Frustrated',
                                      font='Arial',
                                      pos=(-0.47, 0.1), height=0.035, wrapWidth=None, ori=0,
                                      color='black', colorSpace='rgb', opacity=1,
                                      languageStyle='LTR',
                                      depth=-21.0);
    text_angry = visual.TextStim(win=win, name='text_angry',
                                 text='Angry',
                                 font='Arial',
                                 pos=(-0.30, 0.25), height=0.04, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-22.0);
    text_tense = visual.TextStim(win=win, name='text_tense',
                                 text='Tense',
                                 font='Arial',
                                 pos=(-0.10, 0.38), height=0.04, wrapWidth=None, ori=0,
                                 color='black', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=-23.0);
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
        GertComponents = [excited, delighted, happy, content, relaxed, calm, tired, bored, depressed, frustrated, angry,
                          tense, text_excited, text_delighted, text_happy, text_content, text_relaxed, text_calm,
                          text_tired, text_bored, text_depressed, text_frustrated, text_angry, text_tense, mouse]
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

            # *excited* updates
            if excited.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                excited.frameNStart = frameN  # exact frame index
                excited.tStart = t  # local t and not account for scr refresh
                excited.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(excited, 'tStartRefresh')  # time at next scr refresh
                excited.setAutoDraw(True)

            # *delighted* updates
            if delighted.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                delighted.frameNStart = frameN  # exact frame index
                delighted.tStart = t  # local t and not account for scr refresh
                delighted.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(delighted, 'tStartRefresh')  # time at next scr refresh
                delighted.setAutoDraw(True)

            # *happy* updates
            if happy.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                happy.frameNStart = frameN  # exact frame index
                happy.tStart = t  # local t and not account for scr refresh
                happy.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(happy, 'tStartRefresh')  # time at next scr refresh
                happy.setAutoDraw(True)

            # *content* updates
            if content.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                content.frameNStart = frameN  # exact frame index
                content.tStart = t  # local t and not account for scr refresh
                content.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(content, 'tStartRefresh')  # time at next scr refresh
                content.setAutoDraw(True)

            # *relaxed* updates
            if relaxed.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                relaxed.frameNStart = frameN  # exact frame index
                relaxed.tStart = t  # local t and not account for scr refresh
                relaxed.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(relaxed, 'tStartRefresh')  # time at next scr refresh
                relaxed.setAutoDraw(True)

            # *calm* updates
            if calm.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                calm.frameNStart = frameN  # exact frame index
                calm.tStart = t  # local t and not account for scr refresh
                calm.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(calm, 'tStartRefresh')  # time at next scr refresh
                calm.setAutoDraw(True)

            # *tired* updates
            if tired.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                tired.frameNStart = frameN  # exact frame index
                tired.tStart = t  # local t and not account for scr refresh
                tired.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(tired, 'tStartRefresh')  # time at next scr refresh
                tired.setAutoDraw(True)

            # *bored* updates
            if bored.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                bored.frameNStart = frameN  # exact frame index
                bored.tStart = t  # local t and not account for scr refresh
                bored.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(bored, 'tStartRefresh')  # time at next scr refresh
                bored.setAutoDraw(True)

            # *depressed* updates
            if depressed.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                depressed.frameNStart = frameN  # exact frame index
                depressed.tStart = t  # local t and not account for scr refresh
                depressed.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(depressed, 'tStartRefresh')  # time at next scr refresh
                depressed.setAutoDraw(True)

            # *frustrated* updates
            if frustrated.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                frustrated.frameNStart = frameN  # exact frame index
                frustrated.tStart = t  # local t and not account for scr refresh
                frustrated.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(frustrated, 'tStartRefresh')  # time at next scr refresh
                frustrated.setAutoDraw(True)

            # *angry* updates
            if angry.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                angry.frameNStart = frameN  # exact frame index
                angry.tStart = t  # local t and not account for scr refresh
                angry.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(angry, 'tStartRefresh')  # time at next scr refresh
                angry.setAutoDraw(True)

            # *tense* updates
            if tense.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                tense.frameNStart = frameN  # exact frame index
                tense.tStart = t  # local t and not account for scr refresh
                tense.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(tense, 'tStartRefresh')  # time at next scr refresh
                tense.setAutoDraw(True)

            # *text_excited* updates
            if text_excited.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_excited.frameNStart = frameN  # exact frame index
                text_excited.tStart = t  # local t and not account for scr refresh
                text_excited.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_excited, 'tStartRefresh')  # time at next scr refresh
                text_excited.setAutoDraw(True)

            # *text_delighted* updates
            if text_delighted.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_delighted.frameNStart = frameN  # exact frame index
                text_delighted.tStart = t  # local t and not account for scr refresh
                text_delighted.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_delighted, 'tStartRefresh')  # time at next scr refresh
                text_delighted.setAutoDraw(True)

            # *text_happy* updates
            if text_happy.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_happy.frameNStart = frameN  # exact frame index
                text_happy.tStart = t  # local t and not account for scr refresh
                text_happy.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_happy, 'tStartRefresh')  # time at next scr refresh
                text_happy.setAutoDraw(True)

            # *text_content* updates
            if text_content.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_content.frameNStart = frameN  # exact frame index
                text_content.tStart = t  # local t and not account for scr refresh
                text_content.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_content, 'tStartRefresh')  # time at next scr refresh
                text_content.setAutoDraw(True)

            # *text_relaxed* updates
            if text_relaxed.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_relaxed.frameNStart = frameN  # exact frame index
                text_relaxed.tStart = t  # local t and not account for scr refresh
                text_relaxed.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_relaxed, 'tStartRefresh')  # time at next scr refresh
                text_relaxed.setAutoDraw(True)

            # *text_calm* updates
            if text_calm.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_calm.frameNStart = frameN  # exact frame index
                text_calm.tStart = t  # local t and not account for scr refresh
                text_calm.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_calm, 'tStartRefresh')  # time at next scr refresh
                text_calm.setAutoDraw(True)

            # *text_tired* updates
            if text_tired.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_tired.frameNStart = frameN  # exact frame index
                text_tired.tStart = t  # local t and not account for scr refresh
                text_tired.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_tired, 'tStartRefresh')  # time at next scr refresh
                text_tired.setAutoDraw(True)

            # *text_bored* updates
            if text_bored.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_bored.frameNStart = frameN  # exact frame index
                text_bored.tStart = t  # local t and not account for scr refresh
                text_bored.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_bored, 'tStartRefresh')  # time at next scr refresh
                text_bored.setAutoDraw(True)

            # *text_depressed* updates
            if text_depressed.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_depressed.frameNStart = frameN  # exact frame index
                text_depressed.tStart = t  # local t and not account for scr refresh
                text_depressed.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_depressed, 'tStartRefresh')  # time at next scr refresh
                text_depressed.setAutoDraw(True)

            # *text_frustrated* updates
            if text_frustrated.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_frustrated.frameNStart = frameN  # exact frame index
                text_frustrated.tStart = t  # local t and not account for scr refresh
                text_frustrated.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_frustrated, 'tStartRefresh')  # time at next scr refresh
                text_frustrated.setAutoDraw(True)

            # *text_angry* updates
            if text_angry.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_angry.frameNStart = frameN  # exact frame index
                text_angry.tStart = t  # local t and not account for scr refresh
                text_angry.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_angry, 'tStartRefresh')  # time at next scr refresh
                text_angry.setAutoDraw(True)

            # *text_tense* updates
            if text_tense.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                text_tense.frameNStart = frameN  # exact frame index
                text_tense.tStart = t  # local t and not account for scr refresh
                text_tense.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text_tense, 'tStartRefresh')  # time at next scr refresh
                text_tense.setAutoDraw(True)
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
                        for obj in [excited, delighted, happy, content, relaxed, calm, tired, bored, depressed,
                                    frustrated, angry, tense]:
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
        trials.addData('excited.started', excited.tStartRefresh)
        trials.addData('excited.stopped', excited.tStopRefresh)
        trials.addData('delighted.started', delighted.tStartRefresh)
        trials.addData('delighted.stopped', delighted.tStopRefresh)
        trials.addData('happy.started', happy.tStartRefresh)
        trials.addData('happy.stopped', happy.tStopRefresh)
        trials.addData('content.started', content.tStartRefresh)
        trials.addData('content.stopped', content.tStopRefresh)
        trials.addData('relaxed.started', relaxed.tStartRefresh)
        trials.addData('relaxed.stopped', relaxed.tStopRefresh)
        trials.addData('calm.started', calm.tStartRefresh)
        trials.addData('calm.stopped', calm.tStopRefresh)
        trials.addData('tired.started', tired.tStartRefresh)
        trials.addData('tired.stopped', tired.tStopRefresh)
        trials.addData('bored.started', bored.tStartRefresh)
        trials.addData('bored.stopped', bored.tStopRefresh)
        trials.addData('depressed.started', depressed.tStartRefresh)
        trials.addData('depressed.stopped', depressed.tStopRefresh)
        trials.addData('frustrated.started', frustrated.tStartRefresh)
        trials.addData('frustrated.stopped', frustrated.tStopRefresh)
        trials.addData('angry.started', angry.tStartRefresh)
        trials.addData('angry.stopped', angry.tStopRefresh)
        trials.addData('tense.started', tense.tStartRefresh)
        trials.addData('tense.stopped', tense.tStopRefresh)
        trials.addData('text_excited.started', text_excited.tStartRefresh)
        trials.addData('text_excited.stopped', text_excited.tStopRefresh)
        trials.addData('text_delighted.started', text_delighted.tStartRefresh)
        trials.addData('text_delighted.stopped', text_delighted.tStopRefresh)
        trials.addData('text_happy.started', text_happy.tStartRefresh)
        trials.addData('text_happy.stopped', text_happy.tStopRefresh)
        trials.addData('text_content.started', text_content.tStartRefresh)
        trials.addData('text_content.stopped', text_content.tStopRefresh)
        trials.addData('text_relaxed.started', text_relaxed.tStartRefresh)
        trials.addData('text_relaxed.stopped', text_relaxed.tStopRefresh)
        trials.addData('text_calm.started', text_calm.tStartRefresh)
        trials.addData('text_calm.stopped', text_calm.tStopRefresh)
        trials.addData('text_tired.started', text_tired.tStartRefresh)
        trials.addData('text_tired.stopped', text_tired.tStopRefresh)
        trials.addData('text_bored.started', text_bored.tStartRefresh)
        trials.addData('text_bored.stopped', text_bored.tStopRefresh)
        trials.addData('text_depressed.started', text_depressed.tStartRefresh)
        trials.addData('text_depressed.stopped', text_depressed.tStopRefresh)
        trials.addData('text_frustrated.started', text_frustrated.tStartRefresh)
        trials.addData('text_frustrated.stopped', text_frustrated.tStopRefresh)
        trials.addData('text_angry.started', text_angry.tStartRefresh)
        trials.addData('text_angry.stopped', text_angry.tStopRefresh)
        trials.addData('text_tense.started', text_tense.tStartRefresh)
        trials.addData('text_tense.stopped', text_tense.tStopRefresh)
        # store data for trials (TrialHandler)
        x, y = mouse.getPos()
        buttons = mouse.getPressed()
        if sum(buttons):
            # check if the mouse was inside our 'clickable' objects
            gotValidClick = False
            for obj in [excited, delighted, happy, content, relaxed, calm, tired, bored, depressed, frustrated, angry,
                        tense]:
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
