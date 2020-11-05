from tkinter import *
from tkinter import ttk
import loginWindow as lw



import patientWindow as pw

class userWindow():

    def __init__(self, name, surname, environment, id):
        self.name = name
        self.surname = surname
        self.environment = environment  # 0 = clinical, 1 = neuromarketing
        self.patientId = id
        self.window = None
        self.createWindow()
        self.patient = None

    def logout(self):
        self.window.destroy()
        application = lw.loginWindow()


    def createWindow(self):
        self.window = Tk()
        self.window.title("User personal page")
        self.window.geometry("800x600")

        Label(text=self.name + " " + self.surname, font='Times 25').grid(row=0, column=0, pady=40 )

        logout_but = Button(self.window, text="Logout", command=self.logout).grid(row=0, column=3, pady=10, padx=200)

        # Add a grid
        mainframe = Frame(self.window)
        mainframe.grid(column=0, row=1, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)


        # Create a Tkinter variable
        tkvar = StringVar(self.window)

        # Dictionary with options
        choices = ['Mario Bianchi', 'Alex Reid', 'James Bond', 'Donald Duck']
        tkvar.set(choices[0])  # set the default option

        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        if self.environment==0:
            Label(mainframe, text="Choose a patient").grid(row=2, column=1)
        else:
            Label(mainframe, text="Choose a participant").grid(row=2, column=1)

        popupMenu.grid(row=3, column=1)

        def selectPatient(str):

            if self.patient is not None:
                for w in self.patient.widgets:
                    w.destroy()

            name_surname = str.get().split()

            self.patient = pw.PatientWindow(self.window, name_surname[0], name_surname[1], 0)

        # on change dropdown value
        def change_dropdown(*args):
            selectPatient(tkvar)

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)


