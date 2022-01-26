from tkinter import *
from tkinter import ttk
import userWindow as uw
import json

class loginWindow:

    def __init__(self):

        self.window = Tk()
        self.window.title('Vibe')
        self.window.geometry("600x400")
        #fp = open('ffmpeg.txt', 'r')
        #self.reso = json.load(fp)
        #fp.close()
        #self.sw, self.sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        #self.window.geometry('%sx%s+%s+%s' % (1020, 960, -self.sw + self.reso['screen_shift'], 700))


        Label(text=' Login ', font='Times 25').grid(row=1, column=3, pady=40)

        Label(text = ' Username ', font='Times 15').grid(row=2, column=1, pady=20)
        self.username = Entry()
        self.username.grid(row=2, column=2, columnspan=10)

        Label(text = ' Password ',font='Times 15').grid(row=3, column=1, pady=10)
        self.password = Entry(show='*')
        self.password.grid(row=3, column=2, columnspan=10)

        ttk.Button(text='LOGIN', command=self.login_user).grid(row=4,column=3)

        self.window.columnconfigure(3, weight=5)

        self.window.bind("<Return>", lambda e: self.login_user())

        self.window.mainloop()


    def login_user(self):

        '''Check username and password entered are correct'''

        fp = open('credentials.txt', 'r')
        credentials = json.load(fp)
        fp.close()

        self.user = credentials['username']
        self.passw = credentials['password']

        if self.username.get() == self.user and self.password.get() == self.passw:

            self.message = Label(text='Ok!!!!', fg='Red')
            self.message.grid(row=6, column=3)

            #Destroy the current window
            self.window.destroy()

            #Open new window
            newWindow = uw.userWindow("Vito", "De Feo", 1234)
            newWindow.window.mainloop()

        else:

            '''Prompt user that either id or password is wrong'''
            self.message = Label(text = 'Username or Password incorrect. Try again!', fg = 'Red')
            self.message.grid(row=6, column=3)
