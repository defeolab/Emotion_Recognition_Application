from tkinter import *
from tkinter import ttk, _setit
import tkinter as tk

import pandas as pd

import loginWindow as lw
from random import randint
import os
import json
from tkinter import messagebox


import patientWindow as pw
#global temp
class userWindow():

    def __init__(self, name, surname, id):
        self.name = name
        self.surname = surname
        self.patientId = id
        self.window = None
        self.patient = None
        fp = open('anagraphicData.txt', 'r')
        data = json.load(fp)
        self.ids = data['IDs']
        fp.close()
        self.participants = []
        for id in self.ids :
            self.participants.append('Participant n '+ str(id))
        self.dropdown = None

        self.createWindow()

    def logout(self):
        self.window.destroy()
        application = lw.loginWindow()

    def update_menu(self):

        self.dropdown["menu"].delete(0, "end")
        for string in self.participants:
            self.dropdown["menu"].add_command(label=string, command=_setit(self.tkvar, string))




        #print("patient")

    def add_patient(self):
        temp = 0
        top = Toplevel()
        top.title("Add a new Patient")
        top.geometry("600x600")


        Label(top, text=' Patient anagraphic data  ', font='Times 25').grid(row=1, column=3, pady=40)

        Label(top, text=' Name ', font='Times 15').grid(row=2, column=1, pady=20)
        name = Entry(top)
        name.grid(row=2, column=2, columnspan=10)

        Label(top, text=' Surname ', font='Times 15').grid(row=3, column=1, pady=10)
        surname = Entry(top)
        surname.grid(row=3, column=2, columnspan=10)

        Label(top, text=' Age ', font='Times 15').grid(row=4, column=1, pady=20)
        age = Entry(top)
        age.grid(row=4, column=2, columnspan=10)

        Label(top, text=' Gender ', font='Times 15').grid(row=5, column=1, pady=20)
        genderValues = ['Male', 'Female', 'Prefer not to say']
        varGend = StringVar(top)
        varGend.set(genderValues[0])
        genderMenu = OptionMenu(top, varGend, *genderValues)
        genderMenu.grid(row=5, column=2, columnspan=10)


        Label(top, text=' Educational Level ', font='Times 15').grid(row=6, column=1, pady=20)
        eduValues = ['Primary School', 'Middle School', 'High School', 'Bachelor/Master Degree']
        varEdu = StringVar(top)
        varEdu.set(eduValues[0])
        eduMenu = OptionMenu(top, varEdu, *eduValues)
        eduMenu.grid(row=6, column=2, columnspan=10)

        Label(top, text=' Trauma ', font='Times 15').grid(row=7, column=1, pady=20)
        trumaValues = ['Cancer injury', 'Head injury', 'vascular injury']
        varTruma = StringVar(top)
        varTruma.set(trumaValues[0])
        trumaMenu = OptionMenu(top, varTruma, *trumaValues)
        trumaMenu.grid(row=7, column=2, columnspan=10)

        Label(top, text=' Nationality ', font='Times 15').grid(row=8, column=1, pady=20)
        nationality = Entry(top)
        nationality.grid(row=8, column=2, columnspan=10)




        def add_to_participants():
            while True:
                id = randint(1000, 9999)
                if id not in self.ids:
                    break

            #self.participants.append("Participant n " +str(id))
            self.participants.append(str(id))
            self.update_menu()

            fp = open('anagraphicData.txt', 'r')
            data = json.load(fp)

            data['IDs'].append(id)

            try:
                path = os.getcwd()+'/data/'+str(id)
                os.mkdir(path)
                temp = str(id)
            except OSError:
                print("Creation of the directory %s failed" % path)

            elem = {'id': id, 'name': name.get(), 'surname': surname.get(), 'age': age.get(),
                    'gender': varGend.get(), 'edu': varEdu.get()}

            elem1 = {id,name.get(),surname.get(),age.get(),varGend.get(),varEdu.get()}

            data['Participants'].append(elem)


            df = pd.DataFrame.from_dict(data, orient='index')
            df.to_csv('website3.csv', index=False, header=True, encoding='utf-8')

            #fp = open('anagraphicData.txt', 'w')
            #json.dump(data, fp)
            #fp.close()

            #js = open('anagraphicData.json', 'w')
            #json.dump(data, js)
            #js.close()


            #df = pd.read_json(r'anagraphicData.json')
            #df.to_csv(r'patientdata.csv',index = None)



            top.destroy()

            messagebox.showinfo("Sucessfully added", "You added a new Participant, the Participant is associated with the number "+ str(id)+".")


        Button(top, text='Add Participant', command=add_to_participants).grid(row=9, column=3, pady=20)


    def createWindow(self):
        self.window = Tk()
        self.window.title("User personal page")
        self.window.geometry("1000x600")
        self.window.columnconfigure(1, weight=1)
        #root = Tk()

        Label(self.window, text=self.name + " " + self.surname, font='Times 25').grid(row=0, column=0, pady=40, padx = 20 )

        logout_but = ttk.Button(self.window, text="Logout", command=self.logout).grid(sticky=E, row=0, column=10, padx=10)
        Label(text="", font='Times 25').grid(row=0, column=1, pady=40, padx = 20 )


        mainframe = Frame(self.window)
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        #scrollbar = Scrollbar(mainframe)
        #scrollbar.pack(side=RIGHT, fill=Y)

        # Create a Tkinter variable
        self.tkvar = StringVar(self.window)

        # Dictionary with options
        self.tkvar.set(self.participants[0])  # set the default option

        self.dropdown = OptionMenu(mainframe, self.tkvar, *self.participants)

        #self.dropdown = Listbox(mainframe, yscrollcommand=scrollbar.set)
        #self.dropdown.insert(END, self.tkvar, *self.participants)

        Label(mainframe, text="Choose a participant", font='Times 16').grid(row=2, column=1, pady= 20)

        self.dropdown.grid(row=3, column=1, sticky=(N, W, E, S))
        #self.dropdown.pack(side=LEFT, fill=BOTH)

        #self.dropdown.config(yscrollcommand=scrollbar.set)

        #scrollbar.config(command=self.dropdown.yview)

        add_but = ttk.Button(mainframe, text="Add new Participant", command=self.add_patient).grid(row=4, column=1,
                                                                                                 padx=10, pady=50)

        Label(mainframe, text="Search patient", font='Times 16').grid(row=5, column=1, pady=20)
        self.search = Entry(mainframe)
        self.search.grid(row=6, column=1, columnspan=1)
        add_search_but = ttk.Button(mainframe, text="Search", command=self.search_patient).grid(row=7, column=1,
                                                                                                padx=10, pady=50)
        self.window.columnconfigure(6)
        #weight = 19
        self.window.bind("<Return>", lambda e: self.search_patient())

        no_participant = ttk.Label(self.window, text="No Participant Selected", font='Times 26').grid(row=1, column=1, padx= 30, pady= 20)

        def selectPatient(str):
            print("hi")
            if self.patient is not None:
                #no_participant.destroy()
                for w in self.patient.widgets:
                    w.destroy()


            #name_surname = str.get().split()
            pat = str.get().split()[2]
            self.patient = pw.PatientWindow(self.window, pat)

        # on change dropdown value
        def change_dropdown(*args):
            selectPatient(self.tkvar)

        # link function to change dropdown
        self.tkvar.trace('w', change_dropdown)

    def searchPatient(self, str):
        print("hi")
        if self.patient is not None:
            # no_participant.destroy()
            for w in self.patient.widgets:
                w.destroy()

        # name_surname = str.get().split()
        pat = str.split()[2]
        self.patient = pw.PatientWindow(self.window, pat)

    def search_patient(self):
        self.search_key_var = self.search.get()
        if self.search_key_var is not None:
            self.searchPatient(self.search_key_var)
        else:
            print("No participant exist")







