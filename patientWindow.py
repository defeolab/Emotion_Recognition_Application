import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import expGiulia
import sys, os
import vlc
from time import sleep
import webBrowser
import json

import videoPlayer as vp

#from PyQt5.QtWebEngineWidgets import QWebEngineView


class PatientWindow :

    def __init__(self, parent, id, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.patientId = id

        self.parent = parent
        self.widgets = self.addWidgets()

    def browseFiles(self):
        filename = filedialog.askopenfile(initialdir= os.getcwd() +"/data/"+ str(self.patientId),
                                              title="Select a File",
                                              filetypes=(("csv files",
                                                          "*.csv"),
                                                         ("all files",
                                                          "*.*")))

        if filename is not None :

            comand = "start " + filename.name
            try :
                os.system(comand)
            except:
                print(comand)


    def addWidgets(self):
        widgets = []

        self.parent.columnconfigure(1, weight = 2)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight =1)

        experiments_frame.grid(row=1, column=1, rowspan = 2, pady=3, padx=100 , sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant n " + self.patientId, font='Times 18').grid(row =0, column=1)

        angraphic = ttk.Button(self.parent, text="Show Anagraphic", command= self.show_anagraphic)
        angraphic.grid(row=1, column= 2)

        widgets.append(experiments_frame)


        neuro_frame = ttk.LabelFrame(experiments_frame, text="Experiments", relief=tk.RIDGE)
        neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

        button1 = ttk.Button(neuro_frame, text="Giulia's Experiment", command=self.run_expGiulia)
        button1.grid(row=1, column=1, pady=15)
        button2 = ttk.Button(neuro_frame, text="Alessia's Experiment", command=self.run_expAlessia)
        button2.grid(row=2, column=1, pady=15)
        button3 = ttk.Button(neuro_frame, text="Camilla's Experiment", command=self.run_expCamilla)
        button3.grid(row=3, column=1, pady=15)
        button4 = ttk.Button(neuro_frame, text="Chiara's Experiment", command=self.run_expChiara)
        button4.grid(row=4, column=1, pady=15)
        neuro_frame.columnconfigure(1, weight=1)

        show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=30)

        widgets.extend([neuro_frame, button1, button2, button3, button4, show_data_but])

        return widgets

    def run_expGiulia(self):
        try:
            if(self.patientId == None):
                self.patientId = '';
            expGiulia.runExp(self.patientId)

        except:

            # if(sys.exc_info()[1].__getattribute__('code') == 1):
            #     self.run_expCamilla()
            # self.run_expCamilla()       #Da LEVARE POST PRESENTAZIONE
            print("Manual escape")

        os.startfile("https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

    def run_expAlessia (self):
        #print("Non funzionante")

        top = tk.Toplevel()
        top.title("Experiment VLC media player")

        top.state('zoomed')

        player = None

        player = vp.Player(top, title="tkinter vlc")

        def closeTop():
            player.OnStop()
            top.destroy()

            os.startfile("https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")

        top.protocol("WM_DELETE_WINDOW", closeTop)

        def pause(arg):
            #print(str(arg))
            player.OnPause()
        top.bind('<space>', pause)



    def run_expCamilla(self):
        webBrowser.launch_browser("https://www.lavazza.it/it.html", 1)

    def run_expChiara(self):
        webBrowser.launch_browser("https://www.spain.info/it/", 2)
        # https: // www.spain.info / it /
        # https: // www.visitnorway.it /

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

            ttk.Label(top, text="Participant n " + self.patientId, font='Times 26').grid(row=0, column=1, pady =30, padx = 20)
            ttk.Label(top, text="Age :  " + user['age'], font='Times 18').grid(row=1, column=1, sticky=tk.W, pady =20, padx = 5)
            ttk.Label(top, text="Gender :  " + user['gender'], font='Times 18').grid(row=2, column=1, sticky=tk.W, pady =20, padx = 5)
            ttk.Label(top, text="Educational Level :  " + user['edu'], font='Times 18').grid(row=3, column=1, sticky=tk.W, pady =20, padx = 5)



        else:
            ttk.Label(top, text="Data on Participant n " + self.patientId+ " not found.", font='Times 18').grid(row=0, column=1, padx = 5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
