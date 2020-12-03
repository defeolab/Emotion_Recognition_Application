import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import expGiulia
import expClinical
import sys, os
import vlc
from time import sleep
import webBrowser

#from PyQt5.QtWebEngineWidgets import QWebEngineView


class PatientWindow :

    def __init__(self, parent, environment, id, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.patientId = id
        self.environment = environment          #0 = clinical, 1 = neuromarketing
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

        widgets.append(experiments_frame)

        if self.environment == 0:

            neuro_frame = ttk.LabelFrame(experiments_frame, text="Experiments", relief=tk.RIDGE)
            neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

            button1 = ttk.Button(neuro_frame, text="Giulia's Experiment", command=self.run_expGiulia)
            button1.grid(row=1, column=1, pady=15)
            button2 = ttk.Button(neuro_frame, text="Alessia's Experiment", command=self.run_expAlessia)
            button2.grid(row=2, column=1, pady=15)
            neuro_frame.columnconfigure(1, weight=1)

            show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
            show_data_but.grid(row=2, column=1, pady=30)

            widgets.extend([neuro_frame, button1, button2, show_data_but])

        else:

            clinical_frame = ttk.LabelFrame(experiments_frame, text="Experiment", relief=tk.RIDGE)
            clinical_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

            button3 = ttk.Button(clinical_frame, text="Clinical Experiment", command=self.run_expClinical)
            clinical_frame.columnconfigure(1, weight=1)
            button3.grid(row=1, column=1, pady = 10)

            show_data_but = ttk.Button(experiments_frame, text="Show Previous Data", command=self.browseFiles)
            show_data_but.grid(row=2, column=1, pady = 30)

            widgets.extend([clinical_frame, button3, show_data_but])

        return widgets

    def run_expGiulia(self):
        try:
            if(self.patientId == None):
                self.patientId = '';
            expGiulia.runExp(self.patientId)

        except:

            if(sys.exc_info()[1].__getattribute__('code') == 1):
                self.run_expCamilla()
            self.run_expCamilla()       #Da LEVARE POST PRESENTAZIONE

    def run_expClinical(self):
        try:
            if (self.patientId == None):
                self.patientId = '';
            #os.system('expClinical.py')

        except:
            print("exit with " + str(sys.exc_info()[0]))

    def run_expAlessia (self):
        print("Non funzionante")
        #
        #
        # # Instance = vlc.Instance('--fullscreen')
        # Instance = vlc.Instance()
        # player = Instance.media_player_new()
        # Media = Instance.media_new('videos/filmato_Alessia.mp4')
        # print(Media.get_mrl())
        #
        # root.bind("<Return>", (lambda event: print("Return")))
        # root.bind("<Escape>", (lambda event: print("escape")))
        #
        # player.set_media(Media)
        # player.set_fullscreen(True)
        # player.play()
        #
        # def close_player():
        #     player.stop()
        #
        # sleep(5)  # Or however long you expect it to take to open vlc
        # while player.is_playing():
        #     sleep(1)


    def run_expCamilla(self):
        webBrowser.launch_browser()



