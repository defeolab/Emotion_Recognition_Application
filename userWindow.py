from tkinter import *
from tkinter import ttk
import loginWindow as lw
from random import randint
import os


import patientWindow as pw

class userWindow():

    def __init__(self, name, surname, environment, id):
        self.name = name
        self.surname = surname
        self.environment = environment  # 0 = clinical, 1 = neuromarketing
        self.patientId = id
        self.window = None
        self.patient = None
        self.participants = ['Participant n 1234', 'Participant n 5678', 'Participant n 3853', 'Participant n 6734']
        self.dropdown = None

        self.createWindow()

    def logout(self):
        self.window.destroy()
        application = lw.loginWindow()

    def update_menu(self):
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for string in self.participants:
            menu.add_command(label=string)

    def add_patient(self):
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
        gender = Entry(top)
        gender.grid(row=5, column=2, columnspan=10)

        Label(top, text=' Educational Level ', font='Times 15').grid(row=5, column=1, pady=20)
        gender = Entry(top)
        gender.grid(row=6 , column=2, columnspan=10)

        Label(top, text=' Other info???? ', font='Times 15').grid(row=6, column=1, pady=20)


        def add_to_participants():
            id = randint(1000, 9999)
            self.participants.append("Participant n " +str(id))
            self.update_menu()

            try:
                path = os.getcwd()+'/data/'+str(id)
                os.mkdir(path)
            except OSError:
                print("Creation of the directory %s failed" % path)

            top.destroy()

        Button(top, text='Add Patient', command=add_to_participants).grid(row=7, column=3)

    def createWindow(self):
        self.window = Tk()
        self.window.title("User personal page")
        self.window.geometry("800x600")
        self.window.columnconfigure(10, weight=1)

        Label(self.window, text=self.name + " " + self.surname, font='Times 25').grid(row=0, column=0, pady=40, padx = 20 )

        logout_but = ttk.Button(self.window, text="Logout", command=self.logout).grid(sticky=E, row=0, column=10, padx=10)
        Label(text="", font='Times 25').grid(row=0, column=1, pady=40, padx = 20 )


        # Add a grid
        mainframe = Frame(self.window)
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)


        # Create a Tkinter variable
        tkvar = StringVar(self.window)

        # Dictionary with options
        tkvar.set(self.participants[0])  # set the default option

        self.dropdown = OptionMenu(mainframe, tkvar, *self.participants)

        Label(mainframe, text="Choose a participant", font='Times 16').grid(row=2, column=1, pady= 20)

        self.dropdown.grid(row=3, column=1, sticky=(N, W, E, S))


        add_but = ttk.Button(mainframe, text="Add new Patient", command=self.add_patient).grid(row=4, column=1,
                                                                                                 padx=10, pady=50)

        def selectPatient(str):

            if self.patient is not None:
                for w in self.patient.widgets:
                    w.destroy()

            #name_surname = str.get().split()
            patient = str.get().split()[2]
            self.patient = pw.PatientWindow(self.window, self.environment, patient)

        # on change dropdown value
        def change_dropdown(*args):
            selectPatient(tkvar)

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)




