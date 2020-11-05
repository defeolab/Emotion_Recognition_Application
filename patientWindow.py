import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import expGiulia
import expClinical
import sys, os

class PatientWindow :

    def __init__(self, parent, environment, id, name=None, surname=None):
        self.name = name
        self.surname = surname
        self.patientId = id
        self.environment = environment          #0 = clinical, 1 = neuromarketing
        self.parent = parent
        self.widgets = self.addWidgets()

    def browseFiles(self):
        filename = filedialog.askopenfile(initialdir= os.getcwd() +"/data",
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

        experiments_frame.grid(row=3, column=1, pady=3, padx=100 , sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Patient n " + self.patientId, font='Times 18').grid(row =0, column=1)

        widgets.append(experiments_frame)

        if self.environment == 0:

            neuro_frame = ttk.LabelFrame(experiments_frame, text="NeuroMarketing experiments", relief=tk.RIDGE)
            neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=100, pady=40)

            button1 = ttk.Button(neuro_frame, text="Giulia's Experiment", command=self.run_expGiulia)
            button1.grid(row=1, column=1)
            button2 = ttk.Button(neuro_frame, text="Alessia's Experiment")
            button2.grid(row=2, column=1)

            widgets.extend([neuro_frame, button1, button2])

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
            print("exit with "+str(sys.exc_info()[0]))


    def run_expClinical(self):
        try:
            if (self.patientId == None):
                self.patientId = '';
            expClinical.runExp(self.patientId)
            #os.system('expClinical.py')

        except:
            print("exit with " + str(sys.exc_info()[0]))


