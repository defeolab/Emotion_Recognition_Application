import tkinter as tk

import base
import videoPlayer as vp
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import eyeTracker
import webcam
import sys, os
import webBrowser
import json
import cv2
from PIL import Image, ImageTk
import time



# from PyQt5.QtWebEngineWidgets import QWebEngineView


class PatientWindow:

    def __init__(self, parent, id, name=None, surname=None, video_source=0):
        self.name = name
        self.surname = surname
        self.patientId = id

        self.parent = parent  # window
        self.widgets = self.addWidgets()
        self.settings = None #possible settings : 'lab' or 'home'

        self.frame = None
        self.camera_on = False

    def add_webcam_frame(self):
        top = Toplevel()
        top.title("Webcam output")
        top.geometry("600x600")
        Label(top, text=' Webcam ', font='Times 25').grid(row=1, column=3, pady=40)

    def browseFiles(self):
        filename = filedialog.askopenfile(initialdir=os.getcwd() + "/data/" + str(self.patientId),
                                          title="Select a File",
                                          filetypes=(("csv files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))

        if filename is not None:

            comand = "start " + filename.name
            try:
                os.system(comand)
            except:
                print(comand)




    def addWidgets(self):
        widgets = []
        style = ttk.Style()
        style.configure('Wild.TButton', background="white")
        style.map('Wild.TButton', background=[('disabled', 'yellow'),('pressed','red')])
        var = tk.IntVar()
        self.x = IntVar()
        self.x.set(0)

        self.parent.columnconfigure(1, weight=2)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight=1)

        experiments_frame.grid(row=1, column=1, rowspan=2, pady=3, padx=100, sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant " + self.patientId, font='Times 18').grid(row=0, column=1)

        angraphic = ttk.Button(self.parent, text="Show Anagraphic", command=self.show_anagraphic)
        angraphic.grid(row=1, column=2)

        #if (self.x.get() == 0):
            #start_camera_button = ttk.Checkbutton(self.parent, command=self.start_camera, text="start camera", variable = self.x)
            #start_camera_button.grid(row=2, column=2)

        lab_button = ttk.Radiobutton(self.parent, text="Switch to Lab Settings",command=self.switch_lab, variable = var, value=1)
        lab_button.grid(row=3, column=2)

        home_button = ttk.Radiobutton(self.parent, text="Switch to Home Settings",
                                 command=self.switch_home, variable=var, value=2)
        home_button.grid(row=4, column=2)

        widgets.append(experiments_frame)

        neuro_frame = ttk.LabelFrame(experiments_frame, text="Experiments", relief=tk.RIDGE)
        neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

        button1 = ttk.Button(neuro_frame, text="Image Experiment", command=self.run_expimage)
        button1.grid(row=1, column=1, pady=15)
        button2 = ttk.Button(neuro_frame, text="Video Experiment", command=self.run_expvideo)
        button2.grid(row=2, column=1, pady=15)
        button3 = ttk.Button(neuro_frame, text="Browser Experiment", command=self.openfile)
        button3.grid(row=3, column=1, pady=15)
        neuro_frame.columnconfigure(1, weight=1)

        show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=30)

        widgets.extend([neuro_frame, button1, button2, button3, show_data_but])

        return widgets


    #def openfile1(self):

    def openfile(self):
        if (self.settings == 'lab') | (self.settings == 'home'):
            self.root = Tk()
            self.root.title("Enter URL")
            self.root.geometry("600x600")

            Label(self.root, text="Search url", font='Times 16').grid(row=5, column=1, pady=20)
            self.search = Entry(self.root)
            self.search.grid(row=6, column=1, columnspan=1)
            add_search_but = Button(self.root, text="Search", command=self.run_expbrowser).grid(row=6, column=2, padx=10, pady=50)

            but1 = Button(self.root, text="web1", command=self.website1).grid(row=7, column=1, padx=10,
                                                                                            pady=20)
            but2 = Button(self.root, text="web2", command=self.website2).grid(row=8, column=1, padx=10,
                                                                                            pady=20)
            but3 = Button(self.root, text="web3", command=self.website3).grid(row=9, column=1, padx=10,
                                                                                            pady=20)
            but4 = Button(self.root, text="web4", command=self.website4).grid(row=10, column=1, padx=10,
                                                                            pady=20)
            self.parent.columnconfigure(6)
            self.parent.bind("<Return>", lambda e: self.run_expbrowser())
        else:
            print("No Mode Selected!")

    def website1(self):
        #self.frame = None
        fp = open('websites.txt', 'r')
        websites = json.load(fp)
        fp.close()

        self.web1 = websites['website1']
        if self.settings == "lab":
        #    if self.camera_on is False:
        #        print("You need to turn the camera on")
        #    else:
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpBrowser(self.web1, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            #self.frame = webcam.Faceless_app()
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' +  str(self.patientId) + '/video_output')
            webBrowser.launch_browser(self.web1, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website2(self):
        fp = open('websites.txt', 'r')
        websites = json.load(fp)
        fp.close()

        self.web2 = websites['website2']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpBrowser(self.web2, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            #self.frame = webcam.Faceless_app()
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            webBrowser.launch_browser(self.web2, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website3(self):
        fp = open('websites.txt', 'r')
        websites = json.load(fp)
        fp.close()

        self.web3 = websites['website3']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpBrowser(self.web3, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            #self.frame = webcam.Faceless_app()
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            webBrowser.launch_browser(self.web3, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website4(self):
        fp = open('websites.txt', 'r')
        websites = json.load(fp)
        fp.close()

        self.web4 = websites['website4']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:
            b#ase.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpBrowser(self.web4, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            #self.frame = webcam.Faceless_app()
            #base.VideoWriterWidget(os.getcwd() + '/data/Browser/' + str(self.patientId) + '/video_output')
            webBrowser.launch_browser(self.web4, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def run_expimage(self):
        if self.settings == "lab":
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpImage(self.patientId)
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")"""
            #base.VideoWriterWidget(os.getcwd() + '/data/Image/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpImage(self.patientId)
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        elif self.settings == "home":
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            top.geometry("300x300")
            top.configure(background='grey')

            path = filedialog.askopenfilename(initialdir=os.getcwd() + "/Image/")
            #base.VideoWriterWidget(os.getcwd() + '/data/Image/' + str(self.patientId) + '/video_output')
            #self.frame = webcam.Faceless_app() #start recording
            if path is not None:
                img = ImageTk.PhotoImage(master=top, image=Image.open(path))
                label1 = tk.Label(top, image=img)
                label1.pack(side="bottom", fill="both", expand="yes")

                def countdown(time):
                    if time == -1:
                        top.destroy()
                        self.frame.stop()
                    else:
                        top.after(1000, countdown, time - 1)

            countdown(30)
            top.mainloop()
            #self.frame.stop()
            os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        else:
            print("No mode selected!")
    def run_expvideo(self):
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":
            base.VideoWriterWidget(os.getcwd() + '/data/Video/' + str(self.patientId) + '/video_output')
            eyeTracker.runexpVideo(self.patientId)
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpVideo(self.patientId)"""

        elif self.settings == "home":
            #to be run after calibration
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            base.VideoWriterWidget(os.getcwd() + '/data/Video/' + str(self.patientId) + '/video_output')
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            player = None
            self.frame = True
            player = vp.Player(top, self.frame, title="tkinter vlc")
            def closeTop():
                player.timer.stop()
                if player.frame is not None:
                    player.frame.stop()
                top.destroy()
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")
                player.OnStop()

            top.protocol("WM_DELETE_WINDOW", closeTop)

            def pause(arg):
                player.OnPause()

            top.bind('<space>', pause)

        else:
            print("No mode selected!")

    def run_expbrowser(self):
        self.search_key_var = None
        self.frame = None
        if self.settings == "lab":
            self.search_key_var = self.search.get()
            if self.search_key_var is not None:
                eyeTracker.runexpBrowser(self.search_key_var, 1, self.patientId, self.parent, self.root)
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                self.search_key_var = self.search.get()
                if self.search_key_var is not None:
                    eyeTracker.runexpBrowser(self.search_key_var, 1, self.patientId, self.parent, self.root)"""
        elif self.settings == "home":
            self.search_key_var = self.search.get()
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            if self.search_key_var is not None:
                self.frame = webcam.Faceless_app()
                webBrowser.launch_browser(self.search_key_var, 1,self.patientId,self.parent,self.root, self.frame)
            else:
                print("no url")

    def switch_lab(self):
        if (self.settings == 'lab'):
            print('lab settings mode !')
        else:
            self.settings = 'lab'

    def start_camera(self):

        if not self.camera_on & (self.settings == 'lab'):
            self.camera_on = True
            self.frame = webcam.App(tk.Toplevel(), "Recording", self.patientId, self.parent)
        else:
            print("camera is already on !")

    def switch_home(self):
        print("home setting mode")

        if (self.settings == 'home'):
            print('already using home settings mode !')
        else:
            self.settings = 'home'
            #self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")

    def show_anagraphic(self):
        top = tk.Toplevel()
        top.title("Anagraphic data")
        top.geometry("500x500")

        fp = open('anagraphicData.txt', 'r')
        data = json.load(fp)

        participants = data['Participants']

        user = None

        for p in participants:
            if str(p['id']) == self.patientId:
                user = p
                break

        if user is not None:

            ttk.Label(top, text="Participant n " + self.patientId, font='Times 26').grid(row=0, column=1, pady=30,
                                                                                         padx=20)
            ttk.Label(top, text="Age :  " + user['age'], font='Times 18').grid(row=1, column=1, sticky=tk.W, pady=20,
                                                                               padx=5)
            ttk.Label(top, text="Gender :  " + user['gender'], font='Times 18').grid(row=2, column=1, sticky=tk.W,
                                                                                     pady=20, padx=5)
            ttk.Label(top, text="Educational Level :  " + user['edu'], font='Times 18').grid(row=3, column=1,
                                                                                             sticky=tk.W, pady=20,
                                                                                             padx=5)



        else:
            ttk.Label(top, text="Data on Participant " + self.patientId + " not found.", font='Times 18').grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
