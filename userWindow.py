from tkinter import *
from tkinter import ttk, _setit
import pandas as pd

import loginWindow as lw
from random import randint
import os
import json
from tkinter import messagebox


import patientWindow as pw
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
            self.participants.append('Participant '+ str(id))
        self.dropdown = None

        self.createWindow()

    def logout(self):
        self.window.destroy()
        application = lw.loginWindow()

    def update_menu(self):

        self.dropdown["menu"].delete(0, "end")
        for string in self.participants:
            self.dropdown["menu"].add_command(label=string, command=_setit(self.tkvar, string))

    def add_patient(self):
        top = Toplevel()
        top.title("Add a new Patient")
        top.geometry("600x1000")


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

            self.participants.append('Participant '+ str(id))
            self.update_menu()

            fp = open('anagraphicData.txt', 'r')
            data = json.load(fp)

            data['IDs'].append(id)

            try:
                id_path = os.getcwd()+'/data/'+str(id)
                os.mkdir(id_path)
                Image_path = os.getcwd()+'/data/Image/'+str(id)
                os.mkdir(Image_path)
                GSRPath1 = os.getcwd()+'/data/Image/'+str(id) + '/GSR_data/'
                os.mkdir(GSRPath1)
                Video_path = os.getcwd() + '/data/Video/' + str(id)
                os.mkdir(Video_path)
                GSRPath2 = os.getcwd() + '/data/Video/' + str(id) + '/GSR_data/'
                os.mkdir(GSRPath2)
                Browser_path = os.getcwd() + '/data/Browser/' + str(id)
                os.mkdir(Browser_path)
                GSRPath3 = os.getcwd() + '/data/Browser/' + str(id) + '/GSR_data/'
                os.mkdir(GSRPath3)
                temp = str(id)
            except OSError:
                print("Creation of the directory %s failed")

            elem = {'id': id, 'name': name.get(), 'surname': surname.get(), 'age': age.get(),
                    'gender': varGend.get(), 'edu': varEdu.get()}


            data['Participants'].append(elem)

            fp = open('anagraphicData.txt', 'w')
            json.dump(data, fp)
            fp.close()

            top.destroy()

            messagebox.showinfo("Sucessfully added", "You added a new Participant, the Participant is associated with the number "+ str(id)+".")


        Button(top, text='Add Participant', command=add_to_participants).grid(row=9, column=3, pady=20)

    def my_remove_sel(self):
        self.win = Tk()
        self.win.geometry("600x300")
        Label(self.win, text="Are you sure to delete participant?", font='Times 16').grid(row=2, column=2, pady=20)
        yes = ttk.Button(self.win, text="Yes", command=self.delete_participant)
        yes.grid(row=4, column=2, padx=10, pady=20)
        no = ttk.Button(self.win, text="No", command=self.no_action)
        no.grid(row=4, column=3, padx=10, pady=20)

    def delete_participant(self):
        part = self.tkvar.get().split()[1]
        fp = open('anagraphicData.txt', 'r')
        data = json.load(fp)
        data['IDs'].remove(int(part))

        fp = open('anagraphicData.txt', 'w')
        json.dump(data, fp)
        fp.close()

        r_index = self.dropdown["menu"].index(self.tkvar.get())  # index of selected option.
        self.dropdown["menu"].delete(r_index)  # deleted the option
        self.tkvar.set(self.dropdown["menu"].entrycget(0, "label"))  # select the first one
        self.win.destroy()

    def no_action(self):
        print('Not deleted')
        self.win.destroy()


    def createWindow(self):
        self.window = Tk()
        self.window.title("User personal page")
        #self.window.geometry("1200x1000")
        self.sw, self.sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        # Root
        self.window.geometry('%sx%s' % (self.sw,self.sh))
        self.window.columnconfigure(1, weight=1)

        Label(self.window, text=self.name + " " + self.surname, font='Times 25').grid(row=0, column=0, pady=40, padx = 20 )

        logout_but = ttk.Button(self.window, text="Logout", command=self.logout).grid(sticky=E, row=0, column=10, padx=10)
        Label(text="", font='Times 25').grid(row=0, column=1, pady=40, padx = 20 )


        mainframe = Frame(self.window)
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # Create a Tkinter variable
        self.tkvar = StringVar(self.window)

        # Dictionary with options
        self.tkvar.set(self.participants[0])  # set the default option

        self.dropdown = OptionMenu(mainframe, self.tkvar, *self.participants)

        Label(mainframe, text="Choose a participant", font='Times 16').grid(row=2, column=1, pady= 20)

        self.dropdown.grid(row=3, column=1, sticky=(N, W, E, S))

        add_but = ttk.Button(mainframe, text="Add new Participant", command=self.add_patient).grid(row=4, column=1,
                                                                                                 padx=10, pady=20)

        del_but = ttk.Button(mainframe, text="Delete Participant", command=lambda: self.my_remove_sel())
        del_but.grid(row=5, column=1, padx=10, pady=20)

        Label(mainframe, text="Search participant", font='Times 16').grid(row=6, column=1, pady=20)
        self.search = Entry(mainframe)
        self.search.grid(row=7, column=1, columnspan=1)
        add_search_but = ttk.Button(mainframe, text="Search", command=self.search_participant).grid(row=8, column=1,
                                                                                                padx=10, pady=20)
        self.window.columnconfigure(6)
        self.window.bind("<Return>", lambda e: self.search_participant())

        no_participant = ttk.Label(self.window, text="No Participant Selected", font='Times 26')
        no_participant.grid(row=1, column=1, padx= 30, pady= 20)


        def selectPatient(str):
            if self.patient is not None:
                no_participant.destroy()
                for w in self.patient.widgets:
                    w.destroy()


            pat = str.get().split()[1]
            self.patient = pw.PatientWindow(self.window, pat)

        # on change dropdown value
        def change_dropdown(*args):
            selectPatient(self.tkvar)

        # link function to change dropdown
        self.tkvar.trace('w', change_dropdown)

    def searchPatient(self, str):
        if self.patient is not None:
            for w in self.patient.widgets:
                w.destroy()

        pat = str.split()[1]
        self.patient = pw.PatientWindow(self.window, pat)

    def search_participant(self):
        self.search_key_var = self.search.get()
        if self.search_key_var is not None:
            self.searchPatient(self.search_key_var)
        else:
            print("No participant exist")

