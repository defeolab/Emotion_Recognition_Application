import ctypes
import tkinter as tk
import threading
import GSR_rec2
import ScreenRecording
import ffmpeg
import ffmpeg_video_audio
import videoPlayer as vp
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import eyeTracker
import webInstruction
import webcam
import sys, os
import webBrowser
import json
import cv2
from PIL import Image, ImageTk
import time



# from PyQt5.QtWebEngineWidgets import QWebEngineView
from GSR.GSR_RECORD_SIGNAL import gsr_thread_record


class PatientWindow:

    def __init__(self, parent, id, name=None, surname=None, video_source=0):
        self.next_image = None
        self.name = name
        self.surname = surname
        self.patientId = id

        self.parent = parent  # window
        self.widgets = self.addWidgets()
        self.settings = None #possible settings : 'lab' or 'home'

        self.frame = None
        self.camera_on = False
        self.experiment = False
        self.timer = 0

    def add_webcam_frame(self):
        top = Toplevel()
        top.title("Webcam output")
        top.geometry("600x600")
        Label(top, text=' Webcam ', font='Times 25').grid(row=1, column=3, pady=40)

    def browseFiles(self):
        #print("Mark is our friend.")
        self.no_participant1.config(text="Mark is our friend!")
        #filename = filedialog.askopenfile(initialdir=os.getcwd() + "/data/" + str(self.patientId),
        #                                  title="Select a File",
        #                                  filetypes=(("csv files",
        #                                              "*.csv"),
        #                                             ("all files",
        #                                              "*.*")))

        #if filename is not None:

        #    comand = "start " + filename.name
        #    try:
        #        os.system(comand)
        #    except:
        #        print(comand)




    def addWidgets(self, neuro_frame=None):
        widgets = []
        style = ttk.Style()
        style.configure('Wild.TButton', background="white")
        style.map('Wild.TButton', background=[('disabled', 'yellow'),('pressed','red')])
        var = tk.IntVar()
        self.x = IntVar()
        self.x.set(0)

        #self.parent.columnconfigure(1, weight=2)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight=1)

        experiments_frame.grid(row=1, column=1, pady=3, padx=50, sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant " + self.patientId, font='Times 18').grid(row=0, column=1)

        but_frame = ttk.LabelFrame(self.parent)
        but_frame.columnconfigure(2, weight=1)

        but_frame.grid(row=1, column=2, pady=1, padx=50, sticky=tk.E + tk.W + tk.N + tk.S)
        ##ttk.Label(but_frame, text="Participant " + self.patientId, font='Times 18').grid(row=0, column=1)

        start_camera_button = ttk.Button(but_frame, command=self.start_camera, text="Start Recording")
        start_camera_button.grid(row=0, column=1,pady=10)

        stop_camera = ttk.Button(but_frame, command=self.stop_cam, text="Stop Recording")
        stop_camera.grid(row=1, column=1,pady=10)

        angraphic = ttk.Button(but_frame, command=self.show_anagraphic, text="Show Anagraphic")
        angraphic.grid(row=2, column=1, pady=100)

        self.lab_button = ttk.Radiobutton(but_frame, text="Switch to Lab Settings",command=self.switch_lab, variable = var, value=1)
        self.lab_button.grid(row=4, column=1)

        self.home_button = ttk.Radiobutton(but_frame, text="Switch to Home Settings",
                                 command=self.switch_home, variable=var, value=2)
        self.home_button.grid(row=5, column=1)

        widgets.append(experiments_frame)

        neuro_frame = ttk.LabelFrame(experiments_frame, text="Experiments", relief=tk.RIDGE)
        neuro_frame.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

        button1 = ttk.Button(neuro_frame, text="Image Experiment", command=self.run_expimage)
        button1.grid(row=1, column=1, pady=15)
        button2 = ttk.Button(neuro_frame, text="Video Experiment", command=self.run_expvideo)
        button2.grid(row=2, column=1, pady=15)
        button3 = ttk.Button(neuro_frame, text="Browser Experiment", command=self.openfile)
        button3.grid(row=3, column=1, pady=15)
        neuro_frame.columnconfigure(1, weight=1)
        self.no_participant1 = ttk.Label(neuro_frame, text="Please select one mode of settings!", font='Times 18')
        self.no_participant1.grid(row=4, column=1,padx=30, pady=20)

        show_data_but = ttk.Button(experiments_frame, text="Mark", command=self.browseFiles)
        show_data_but.grid(row=2, column=1, pady=10)

        del_data_but = ttk.Button(experiments_frame, text="Delete data", command=self.delete_data)
        del_data_but.grid(row=3, column=1, pady=10)

        widgets.extend([neuro_frame, button1, button2, button3, show_data_but])

        return widgets

    def stop_cam(self):
        ffmpeg.stop()

    def delete_data(self):
        print("data has been deleted!")
        path = filedialog.askopenfilename(initialdir=os.getcwd() + "/data/")

    def openfile(self):
        if (self.settings == 'lab') | (self.settings == 'home'):
            self.root = Tk()
            self.root.title("Enter URL")
            self.root.geometry("800x800")
            fp = open('websites.txt', 'r')
            self.websites = json.load(fp)
            fp.close()

            Label(self.root, text="Select Experiment", font='Times 16').grid(row=5, column=1, pady=20)

            but1 = Button(self.root, text="web1", command=self.website1).grid(row=7, column=1, padx=10,
                                                                                            pady=20)
            but2 = Button(self.root, text="web2", command=self.website2).grid(row=8, column=1, padx=10,
                                                                                            pady=20)
            but3 = Button(self.root, text="web3", command=self.website3).grid(row=9, column=1, padx=10,
                                                                                            pady=20)
            but4 = Button(self.root, text="web4", command=self.website4).grid(row=10, column=1, padx=10,
                                                                            pady=20)
            Label(self.root, text=self.websites['website1'], font='Times 14').grid(row=7, column=2, pady=20)
            Label(self.root, text=self.websites['website2'], font='Times 14').grid(row=8, column=2, pady=20)
            Label(self.root, text=self.websites['website3'], font='Times 14').grid(row=9, column=2, pady=20)
            Label(self.root, text=self.websites['website4'], font='Times 14').grid(row=10, column=2, pady=20)
            Label(self.root, text="To change website configuration please edit 'websites.txt' file", font='Times 16').grid(row=12, column=2, pady=20)

            self.parent.columnconfigure(6)
            self.parent.bind("<Return>", lambda e: self.web1())

        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No Mode Selected!")

    def website1(self):

        self.web1 = self.websites['website1']
        if self.settings == "lab":
        #    if self.camera_on is False:
        #        print("You need to turn the camera on")
        #    else:
            self.experiment = True
            #eyeTracker.runexpBrowser(self.web1, 1, self.patientId, self.parent, self.root,self.camera_on)
            eyeTracker.runexpBrowser(self.websites['website1'], 1, self.patientId, self.parent, self.root, self.camera_on)
        elif self.settings == "home":
            #if self.camera_on == True:
            self.experiment = True
            webBrowser.launch_browser(self.websites['website1'], 1,self.patientId,self.parent,self.root,self.frame)
        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def website2(self):

        self.web2 = self.websites['website2']
        if self.settings == "lab":
            self.experiment = True
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:
            eyeTracker.runexpBrowser(self.web2, 1, self.patientId, self.parent, self.root,self.camera_on)
        elif self.settings == "home":
            self.experiment = True
            webBrowser.launch_browser(self.web2, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def website3(self):
        self.web3 = self.websites['website3']
        if self.settings == "lab":
            self.experiment = True
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:

            eyeTracker.runexpBrowser(self.web3, 1, self.patientId, self.parent, self.root,self.camera_on)
        elif self.settings == "home":
            self.experiment = True
            webBrowser.launch_browser(self.web3, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def website4(self):

        self.web4 = self.websites['website4']
        if self.settings == "lab":
            self.experiment = True
            #if self.camera_on is False:
            #    print("You need to turn the camera on")
            #else:

            eyeTracker.runexpBrowser(self.web4, 1, self.patientId, self.parent, self.root,self.camera_on)
        elif self.settings == "home":
            self.experiment = True
            webBrowser.launch_browser(self.web4, 1,self.patientId,self.parent,self.root,self.frame)
        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def run_expimage(self):
        if self.settings == "lab":
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpImage(self.patientId)
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")"""

            eyeTracker.runexpImage(self.patientId)
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        elif self.settings == "home":
            timer = 0

            #webBrowser.launch_browser("file:///C:/Users/zeel9/Downloads/instruction/instruction.html",1,self.patientId,None,None,None)

            self.inst_win = tk.Toplevel()
            self.inst_win.title("Instruction")
            self.inst_win.geometry("1400x1100")

            fp = open('Images.txt', 'r')
            image_inst = json.load(fp)
            fp.close()
            img5 = image_inst['img5']

            img_5 = ImageTk.PhotoImage(master=self.inst_win, image=Image.open(img5))
            #img_5.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

            #Label(inst_win, text="Instruction \n" + image_inst['inst'], font='Times 14').grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=30, pady=15)

            label1 = tk.Label(self.inst_win, image=img_5)
            label1.grid(row=1, column=1, padx=10, pady=10,sticky = tk.W)

            start_but = ttk.Button(self.inst_win, text="Start Experiment!", command=self.start_image_exp)
            start_but.grid(row=2, column=1, padx=10, pady=10)


            self.inst_win.mainloop()
            os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def countdown(self, remaining=None):
        #self.chronometer['text'] = self.convert_seconds_left_to_time()
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.chronometer.configure(text="time's up!")
        else:
            self.chronometer.configure(text="remaining %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.top.after(1000, self.countdown)


    def start_image_exp(self):
        self.count_number = 0
        file = open('ffmpeg.txt', 'r')
        dur = json.load(file)
        file.close()
        self.duration = dur['dur']

        self.inst_win.destroy()
        self.top = Toplevel()
        self.top.title("Image Experiment")
        self.top.geometry("1100x900")

        frame_1 = ttk.LabelFrame(self.top)
        frame_1.columnconfigure(1, weight=1)

        frame_1.grid(row=0, column=2, pady=3, padx=10, sticky=tk.E + tk.W + tk.N + tk.S)

        skip = ttk.Button(frame_1, command=self.next_image, text="Skip")
        skip.grid(row=0, column=1, pady=5)

        self.chronometer = tk.Label(frame_1, text=" ", width=20)
        self.chronometer.grid(row=0, column=4)
        self.remaining = 0
        self.countdown(int(self.duration))

        frame_2 = ttk.LabelFrame(self.top)
        frame_2.columnconfigure(1, weight=2)

        frame_2.grid(row=1, column=2, pady=3, padx=5, sticky=tk.E + tk.W + tk.N + tk.S)

        fp = open('Images.txt', 'r')
        image = json.load(fp)
        fp.close()

        cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.patientId, 1))
        cam1.start()
        sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.patientId, 1))
        sc.start()
        gsr = threading.Thread(target=self.GSR_record, args=(self.patientId, 1))
        gsr.start()


        img1 = image['img1']
        img2 = image['img2']
        img3 = image['img3']
        img4 = image['img4']
        count_1 = image['count_1']
        count_2 = image['count_2']
        count_3 = image['count_3']
        count_4 = image['count_4']

        #path = filedialog.askopenfilename(initialdir=os.getcwd() + "/Image/")
        # path = os.getcwd() + "/Image/Capture.PNG"
        # if path is not None:
        img_1 = ImageTk.PhotoImage(master=frame_2, image=Image.open(img1))
        img_2 = ImageTk.PhotoImage(master=frame_2, image=Image.open(img2))
        img_3 = ImageTk.PhotoImage(master=frame_2, image=Image.open(img3))
        img_4 = ImageTk.PhotoImage(master=frame_2, image=Image.open(img4))

        label1 = tk.Label(frame_2, image=img_1)
        label1.pack(side="top", fill="both", expand="yes")


        def countdown_4(time):
            if time == -1:
                self.top.destroy()

            else:
                self.count_number = 4
                self.top.after(1000, countdown_4, time - 1)

        def countdown_3(time):
            if time == -1:
                # top.destroy()
                label1.config(image=img_4)
                im_timer_4 = threading.Thread(target=countdown_4, args=(int(count_4),))
                im_timer_4.start()


            else:
                self.count_number = 3
                self.top.after(1000, countdown_3, time - 1)

        def countdown_2(time):
            if time == -1:
                # top.destroy()
                label1.config(image=img_3)
                im_timer_3 = threading.Thread(target=countdown_3, args=(int(count_3),))
                im_timer_3.start()

            else:
                self.count_number = 2
                self.top.after(1000, countdown_2, time - 1)

        def countdown_1(time):
            if time == -1:
                # top.destroy()
                label1.config(image=img_2)
                im_timer_2 = threading.Thread(target=countdown_2, args=(int(count_2),))
                im_timer_2.start()

            else:
                self.count_number = 1
                self.top.after(1000, countdown_1, time - 1)

        im_timer_1 = threading.Thread(target=countdown_1, args=(int(count_1),))
        im_timer_1.start()
        if self.count_number == 1:
            #im_timer_1.self.raise_exception()
            im_timer_2 = threading.Thread(target=countdown_2, args=(int(count_2),))
            #filemenu.add_command(command=im_timer_2.start)
        if self.count_number == 2:
            im_timer_2 = threading.Thread(target=countdown_2, args=(int(count_2),))
            #filemenu.add_command(command=im_timer_2.start)
        if self.count_number == 3:
            im_timer_2 = threading.Thread(target=countdown_2, args=(int(count_2),))
            #filemenu.add_command(command=im_timer_2.start)
        #if self.count_number == 4:
            #filemenu.add_command(command=top.destroy)

        self.top.mainloop()

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def run_expvideo(self):
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":

            eyeTracker.runexpVideo(self.patientId)
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpVideo(self.patientId)"""

        elif self.settings == "home":
            #to be run after calibration
            top = tk.Toplevel()
            top.title("Experiment VLC media player")
            top.state('zoomed')
            player = None
            self.frame = True
            player = vp.Player(top, self.frame, title="tkinter vlc")
            def closeTop():
                player.timer.stop()
                if player.frame is not None:
                    player.frame.stop()
                top.destroy()
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLScyO5BiSStjkT3pBeV3PApzsOnxHwuhw0DiSszZZEKstdUUEg/viewform")
                player.OnStop()

            top.protocol("WM_DELETE_WINDOW", closeTop)

            def pause(arg):
                player.OnPause()

            top.bind('<space>', pause)

        else:
            self.no_participant1.config(text="No mode selected!")
            #print("No mode selected!")

    def switch_lab(self):
        if (self.settings == 'lab'):
            self.no_participant1.config(text="Already in the lab setting Mode!")
        else:
            self.no_participant1.config(text="lab setting Mode selected!")
            self.settings = 'lab'

    def GSR_record(self, pat, id):
        gsr = GSR_rec2.Record(pat, id)
        gsr.create_stream()
        gsr.on_rec()

    def start_camera(self):

        if (self.settings == 'lab') & (self.experiment == True):
            self.camera_on = True
            cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording,args=(self.patientId,3))
            cam1.start()
            sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.patientId,3))
            sc.start()
            gsr = threading.Thread(target=self.GSR_record, args=(self.patientId,3))
            gsr.start()

        elif (self.settings == 'home') & (self.experiment == True):
            self.camera_on = True
            cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.patientId,3))
            cam1.start()
            sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.patientId,3))
            sc.start()
            gsr = threading.Thread(target=self.GSR_record, args=(self.patientId,3))
            gsr.start()


        else:
            self.no_participant1.config(text="experiment is not started yet!")
            #print("experiment is not started yet!")

    def switch_home(self):
        print("home setting mode")

        if (self.settings == 'home'):
            self.no_participant1.config(text="Already in the home setting Mode!")
            print('already using home settings mode !')
        else:
            self.no_participant1.config(text="home setting Mode selected!")
            self.settings = 'home'

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
            ttk.Label(top, text="Data on Participant " + self.patientId + " not found.", font='Times 18').grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
