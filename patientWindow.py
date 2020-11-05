import tkinter as tk
from tkinter import ttk
import expGiulia
import sys

class PatientWindow :

    def __init__(self, parent, name, surname, environment, id=None):
        self.name = name
        self.surname = surname
        self.patientId = id
        self.environment = environment          #0 = clinical, 1 = neuromarketing
        self.parent = parent
        self.widgets = self.addWidgets()

    def addWidgets(self):
        widgets = []

        experiments_frame = ttk.Label(self.parent, text= self.name + " " + self.surname, font='Times 18')
        experiments_frame.grid(row=3, column=1, sticky=tk.W, pady=3, padx=100)

        widgets.append(experiments_frame)

        if self.environment == 0:

            neuro_frame = ttk.LabelFrame(self.parent, text="NeuroMarketing experiments", relief=tk.RIDGE)
            neuro_frame.grid(row=4, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=100, pady=40)

            button1 = ttk.Button(neuro_frame, text="Giulia's Experiment", command=self.run_expGiulia
                                 )
            button1.grid(row=1, column=1)
            button2 = ttk.Button(neuro_frame, text="Alessia's Experiment")
            button2.grid(row=2, column=1)

            widgets.extend([neuro_frame, button1, button2])

        else:

            clinical_frame = ttk.LabelFrame(self.parent, text="NeuroMarketing experiments", relief=tk.RIDGE)
            clinical_frame.grid(row=4, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=4)

            button3 = ttk.Button(clinical_frame, text="Clinical Experiment")
            button3.grid(row=1, column=1)

            widgets.extend([clinical_frame, button3])

        return widgets

    def run_expGiulia(self):
        try:
            expGiulia.expGiulia()

        except:
            print("exit with "+str(sys.exc_info()[0]))


