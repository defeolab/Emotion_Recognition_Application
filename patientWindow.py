import tkinter as tk
import videoPlayer as vp
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import eyeTracker
import webcam
import sys, os
import vlc
import urllib
from time import sleep
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
        self.settings = 'lab' #possible settings : 'lab' or 'home'

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
        #style2 = ttk.Style()
        #style2.configure("BW.TLabel", background="red")

        #root = tk.Tk()
        var = tk.IntVar()
        #style = ttk.Style()
        #style.map('TRadiobutton', indicatorcolor=[('selected', '#00FF00')])
        self.x = IntVar()
        self.x.set(0)

        self.parent.columnconfigure(1, weight=2)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight=1)

        experiments_frame.grid(row=1, column=1, rowspan=2, pady=3, padx=100, sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant n " + self.patientId, font='Times 18').grid(row=0, column=1)

        angraphic = ttk.Button(self.parent, text="Show Anagraphic", command=self.show_anagraphic)
        angraphic.grid(row=1, column=2)

        if (self.x.get() == 0):
            start_camera_button = ttk.Checkbutton(self.parent, command=self.start_camera, text="start camera", variable = self.x)
        #start_camera_button.var = self.x
        #print(self.x)
            start_camera_button.grid(row=2, column=2)
        #stop_camera_button = ttk.Checkbutton(self.parent, command=self.stop_camera, text="stop camera", variable = self.x)
        #else:
        #    print("Camera is on!")

        #start_camera_button = ttk.Scale(self.parent,command=self.start_camera, from_=0, to=1, orient=HORIZONTAL)
        #start_camera_button.set(0)
        #start_camera_button.grid(row=2, column=2)


        lab_button = ttk.Radiobutton(self.parent, text="Switch to Lab Settings",command=self.switch_lab, variable = var, value=1)
        lab_button.grid(row=3, column=2)

        home_button = ttk.Radiobutton(self.parent, text="Switch to Home Settings",
                                 command=self.switch_home, variable = var, value=2)
        home_button.grid(row=4, column=2)

        widgets.append(experiments_frame)

        neuro_frame = ttk.LabelFrame(experiments_frame, text="Experiments", relief=tk.RIDGE)
        neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

        button1 = ttk.Button(neuro_frame, text="Image Experiment", command=self.run_expGiulia)
        button1.grid(row=1, column=1, pady=15)
        button2 = ttk.Button(neuro_frame, text="Video Experiment", command=self.run_expAlessia)
        button2.grid(row=2, column=1, pady=15)
        #button3 = ttk.Button(neuro_frame, text="Camilla's Experiment", command=self.run_expCamilla)
        #button3.grid(row=3, column=1, pady=15)
        #button4 = ttk.Button(neuro_frame, text="Chiara's Experiment", command=self.run_expChiara)
        #button4.grid(row=4, column=1, pady=15)
        button5 = ttk.Button(neuro_frame, text="Browser Experiment", command=self.openfile)
        button5.grid(row=3, column=1, pady=15)
        neuro_frame.columnconfigure(1, weight=1)

        show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=30)

        widgets.extend([neuro_frame, button1, button2, button5, show_data_but])

        return widgets


    def openfile(self):
        self.root = Tk()
        self.root.title("Enter URL")
        self.root.geometry("600x600")

        Label(self.root, text="Search url", font='Times 16').grid(row=5, column=1, pady=20)
        self.search = Entry(self.root)
        self.search.grid(row=6, column=1, columnspan=1)
        add_search_but = Button(self.root, text="Search", command=self.run_expCamilla).grid(row=6, column=2, padx=10, pady=50)

        self.parent.columnconfigure(6)
        self.parent.bind("<Return>", lambda e: self.run_expCamilla())


    def run_expGiulia(self):
        if self.settings == "lab":
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpGiulia(self.patientId)
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")
        else:
            self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            top.geometry("300x300")
            top.configure(background='grey')

            path = filedialog.askopenfilename(initialdir=os.getcwd() + "/Image/")

            if path is not None:
                #file = os.startfile(path)
                img = ImageTk.PhotoImage(master=top, image=Image.open(path))
                label1 = tk.Label(top, image=img)
                label1.pack(side="bottom", fill="both", expand="yes")

            #img = ImageTk.PhotoImage(master = top, image = Image.open('Capture.PNG'))
            #label1 = tk.Label(top, image=img)
            #label1.pack(side="bottom", fill="both", expand="yes")


                def countdown(time):
                    if time == -1:
                        top.destroy()
                        self.frame.stop()
                    else:
                        top.after(1000, countdown, time - 1)

            countdown(30)
            top.mainloop()
            os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")


    def run_expAlessia(self):
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpAlessia(self.patientId)

        else:
            #to be run after calibration
            self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            player = None
            player = vp.Player(top, title="tkinter vlc")

            def closeTop():

                top.destroy()
                self.frame.stop()

                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")
                player.OnStop()


            top.protocol("WM_DELETE_WINDOW", closeTop)

            def pause(arg):
                # print(str(arg))
                player.OnPause()

            top.bind('<space>', pause)



    def run_expCamilla(self):
        self.search_key_var = None
        if self.settings == "lab":
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                self.search_key_var = self.search.get()
                if self.search_key_var is not None:
                    #eyeTracker.runexpBrowser(self.patientId, 1)
                    eyeTracker.runexpBrowser(self.search_key_var, 1, self.patientId, self.parent, self.root)
        else:
            self.search_key_var = self.search.get()
            self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
            if self.search_key_var is not None:
                #print(self.search_key_var)
                #f = urllib.request.urlopen(self.search_key_var)
                #myfile = f.read()

                #print(myfile)
                webBrowser.launch_browser(self.search_key_var, 1,self.patientId,self.parent,self.root)
                #self.parent.protocol("WM_DELETE_WINDOW", self.root.destroy())
                #webBrowser.MainFrame(tk.Toplevel(),self.search_key_var, 1)
            else:
                print("no url")
        #def close():
        #    self.root.destroy()

            #webBrowser.launch_browser("https://www.lavazza.it/it.html", 1)
        #self.parent.protocol("WM_DELETE_WINDOW", self.root.destroy())

    def run_expChiara(self):
        self.search_key_var = None
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                #eyeTracker.runexpBrowser(self.patientId, 2)
                self.search_key_var = self.search.get()
                if self.search_key_var is not None:
                    eyeTracker.runexpBrowser(self.search_key_var, 2,self.patientId,self.parent,self.root)
        else:
            self.search_key_var = self.search.get()
            if self.search_key_var is not None:
                self.frame = webcam.Faceless_app(tk.Toplevel(), "Recording")
                webBrowser.launch_browser(self.search_key_var, 2,self.patientId,self.parent,self.root)
            # https: // www.spain.info / it /
            # https: // www.visitnorway.it /

    #def change_color(self):
    #    if (self.settings == 'lab'):
    #        lab_button = ttk.Button(self.parent, text="Switch to Lab Settings", style="BW.TLabel",command=self.switch_lab)
    #        lab_button.grid(row=3, column=2)
    #    else:
    #        home_button = ttk.Button(self.parent, text="Switch to Home Settings", style="BW.TLabel",
    #                             command=self.switch_home)
    #        home_button.grid(row=4, column=2)

    def switch_lab(self):
        if (self.settings == 'lab'):
            print('already using lab settings mode !')
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
            ttk.Label(top, text="Data on Participant n " + self.patientId + " not found.", font='Times 18').grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
