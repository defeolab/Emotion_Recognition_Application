import tkinter as tk
import threading
import GSR_rec
import ScreenRecording
import ffmpeg_video_audio
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

        start_camera_button = ttk.Button(self.parent, command=self.start_camera, text="Start Recording")
        start_camera_button.grid(row=1, column=2)

        angraphic = ttk.Button(self.parent, text="Show Anagraphic", command=self.show_anagraphic)
        angraphic.grid(row=2, column=2,sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

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
        no_participant1 = ttk.Label(neuro_frame, text="Please select one mode of settings!", font='Times 18').grid(
            row=4, column=1,
            padx=30, pady=20)

        show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=30)

        widgets.extend([neuro_frame, button1, button2, button3, show_data_but])

        return widgets


    def openfile(self):
        if (self.settings == 'lab') | (self.settings == 'home'):
            self.root = Tk()
            self.root.title("Enter URL")
            self.root.geometry("800x800")
            fp = open('websites.txt', 'r')
            self.websites = json.load(fp)
            fp.close()

            Label(self.root, text="Select Experiment", font='Times 16').grid(row=5, column=1, pady=20)

            but1 = Button(self.root, text="web1", command=self.website1).grid(row=7, column=1, padx=10,
                                                                                            pady=20)
            but2 = Button(self.root, text="web2", command=self.website2).grid(row=8, column=1, padx=10,
                                                                                            pady=20)
            but3 = Button(self.root, text="web3", command=self.website3).grid(row=9, column=1, padx=10,
                                                                                            pady=20)
            but4 = Button(self.root, text="web4", command=self.website4).grid(row=10, column=1, padx=10,
                                                                            pady=20)
            Label(self.root, text=self.websites['website1'], font='Times 14').grid(row=7, column=2, pady=20)
            Label(self.root, text=self.websites['website2'], font='Times 14').grid(row=8, column=2, pady=20)
            Label(self.root, text=self.websites['website3'], font='Times 14').grid(row=9, column=2, pady=20)
            Label(self.root, text=self.websites['website4'], font='Times 14').grid(row=10, column=2, pady=20)
            Label(self.root, text="To change website configuration please edit 'websites.txt' file", font='Times 16').grid(row=12, column=2, pady=20)

            self.parent.columnconfigure(6)
            self.parent.bind("<Return>", lambda e: self.web1())

        else:
            print("No Mode Selected!")

    def website1(self):

        self.web1 = self.websites['website1']
        if self.settings == "lab":
        #    if self.camera_on is False:
        #        print("You need to turn the camera on")
        #    else:
            eyeTracker.runexpBrowser(self.web1, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            webBrowser.launch_browser(self.web1, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website2(self):

        self.web2 = self.websites['website2']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:
            eyeTracker.runexpBrowser(self.web2, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            webBrowser.launch_browser(self.web2, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website3(self):
        self.web3 = self.websites['website3']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:

            eyeTracker.runexpBrowser(self.web3, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
            webBrowser.launch_browser(self.web3, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            print("No mode selected!")

    def website4(self):

        self.web4 = self.websites['website4']
        if self.settings == "lab":
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:

            eyeTracker.runexpBrowser(self.web4, 1, self.patientId, self.parent, self.root)
        elif self.settings == "home":
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

            eyeTracker.runexpImage(self.patientId)
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        elif self.settings == "home":
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            top.geometry("300x300")
            top.configure(background='grey')

            path = filedialog.askopenfilename(initialdir=os.getcwd() + "/Image/")

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

            im_timer = threading.Thread(target=countdown,args=(30,))
            im_timer.start()
            top.mainloop()
            os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        else:
            print("No mode selected!")
    def run_expvideo(self):
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":

            eyeTracker.runexpVideo(self.patientId)
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpVideo(self.patientId)"""

        elif self.settings == "home":
            #to be run after calibration
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

    def switch_lab(self):
        if (self.settings == 'lab'):
            print('lab settings mode !')
        else:
            self.settings = 'lab'

    def start_camera(self):

        if not self.camera_on & (self.settings == 'lab'):
            self.camera_on = True
            cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording,args=(self.patientId,))
            cam1.start()
            sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.patientId,))
            sc.start()
            gsr = threading.Thread(target=GSR_rec.GSR_recording, args=(self.patientId,))
            gsr.start()

        else:
            print("camera is already on !")

    def switch_home(self):
        print("home setting mode")

        if (self.settings == 'home'):
            print('already using home settings mode !')
        else:
            self.settings = 'home'

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
