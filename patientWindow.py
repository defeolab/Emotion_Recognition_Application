import tkinter as tk
import threading

from psychopy import monitors, __all__, visual
from psychopy.visual import helpers
from screeninfo import get_monitors

from datetime import timedelta
import GSR_rec
import ScreenRecording
import eyeTracker
import eyeTrackerV
import ffmpeg
import ffmpeg_video_audio
import videoPlayer as vp
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import eyeTracker as ey
import os
import json
import WebsiteExperiment
from PIL import Image, ImageTk

# from PyQt5.QtWebEngineWidgets import QWebEngineView
from GSR.GSR_RECORD_SIGNAL import gsr_thread_record


class PatientWindow():
    def __init__(self, parent, id, name=None, surname=None, video_source=0):
        self.next_image = None
        self.name = name
        self.surname = surname
        self.participantId = id
        self.count_number = 0
        self.images_list = []
        self.after_id = None
        self.imag_exp = 0
        self.web_exp = 0
        self.video_ep = 0
        self.time_conversion = None
        self.parent = parent  # window
        self.widgets = self.addWidgets()
        self.settings = None  # possible settings : 'lab' or 'home'

        self.frame = None  # to enable lab setting frame in the experiment
        self.camera_on = False
        self.experiment = False
        self.timer = 0

    def add_webcam_frame(self):
        top = Toplevel()
        top.title("Webcam output")
        top.geometry("600x600")
        Label(top, text=' Webcam ', font='Times 25').grid(row=1, column=3, pady=40)

    def browseFiles(self):
        self.no_participant1.config(text="Mark is our friend!")

    def addWidgets(self, neuro_frame=None):
        widgets = []
        style = ttk.Style()
        style.configure('Wild.TButton', background="white")
        style.map('Wild.TButton', background=[('disabled', 'yellow'), ('pressed', 'red')])
        var = tk.IntVar()
        self.x = IntVar()
        self.x.set(0)

        experiments_frame = ttk.LabelFrame(self.parent)
        experiments_frame.columnconfigure(1, weight=1)

        experiments_frame.grid(row=1, column=1, pady=3, padx=50, sticky=tk.E + tk.W + tk.N + tk.S)
        ttk.Label(experiments_frame, text="Participant " + self.participantId, font='Times 18').grid(row=0, column=1)

        but_frame = ttk.LabelFrame(self.parent)
        but_frame.columnconfigure(2, weight=1)

        but_frame.grid(row=1, column=2, pady=1, padx=50, sticky=tk.E + tk.W + tk.N + tk.S)

        start_camera_button = ttk.Button(but_frame, command=self.start_camera, text="Start Recording")
        start_camera_button.grid(row=0, column=1, pady=10)

        stop_camera = ttk.Button(but_frame, command=self.stop_cam, text="Stop Recording")
        stop_camera.grid(row=1, column=1, pady=10)

        angraphic = ttk.Button(but_frame, command=self.show_anagraphic, text="Show Anagraphic")
        angraphic.grid(row=2, column=1, pady=100)

        self.lab_button = ttk.Radiobutton(but_frame, text="Switch to Lab Settings", command=self.switch_lab,
                                          variable=var, value=1)
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
        self.no_participant1.grid(row=4, column=1, padx=30, pady=20)

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
        # self.web_exp = 1
        if (self.settings == 'lab') | (self.settings == 'home'):
            self.root = Tk()
            self.root.title("Enter URL")
            self.root.geometry("800x800")
            '''
            fp = open('ffmpeg.txt', 'r')
            self.reso = json.load(fp)
            fp.close()
            self.sw, self.sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry('%sx%s+%s+%s' % (self.reso['tobii_width'], self.reso['tobii_hight'], -self.sw + self.reso['screen_shift'], 0))
            '''
            fp = open('websites.txt', 'r')
            self.websites = json.load(fp)
            fp.close()

            Label(self.root, text="Select Experiment", font='Times 16').grid(row=5, column=1, pady=20)
            Button(self.root, text="web1", command=lambda: self.run_websiteExp1(1)).grid(row=7, column=1, padx=10, pady=20)
            #Button(self.root, text="web1", command=self.run_websiteExp1(1)).grid(row=7, column=1, padx=10, pady=20)
            Button(self.root, text="web2",  command=lambda: self.run_websiteExp1(2)).grid(row=8, column=1, padx=10, pady=20)
            Button(self.root, text="web3",  command=lambda: self.run_websiteExp1(3)).grid(row=9, column=1, padx=10, pady=20)
            Button(self.root, text="web4",  command=lambda: self.run_websiteExp1(4)).grid(row=10, column=1, padx=10, pady=20)
            Button(self.root, text="web5",  command=lambda: self.run_websiteExp1(5)).grid(row=11, column=1, padx=10, pady=20)
            Button(self.root, text="web6",  command=lambda: self.run_websiteExp1(6)).grid(row=12, column=1, padx=10, pady=20)
            Button(self.root, text="web7",  command=lambda: self.run_websiteExp1(7)).grid(row=7, column=3, padx=10, pady=20)
            Button(self.root, text="web8",  command=lambda: self.run_websiteExp1(8)).grid(row=8, column=3, padx=10, pady=20)
            Button(self.root, text="web9",  command=lambda: self.run_websiteExp1(9)).grid(row=9, column=3, padx=10, pady=20)
            Button(self.root, text="web10",  command=lambda: self.run_websiteExp1(10)).grid(row=10, column=3, padx=10, pady=20)
            Button(self.root, text="web11",  command=lambda: self.run_websiteExp1(11)).grid(row=11, column=3, padx=10, pady=20)
            Button(self.root, text="web12", command=lambda: self.run_websiteExp1(12)).grid(row=12, column=3, padx=10, pady=20)
            Button(self.root, text="web13", command=lambda: self.run_websiteExp1(13)).grid(row=7, column=5, padx=10, pady=20)
            Button(self.root, text="web14",  command=lambda: self.run_websiteExp1(14)).grid(row=8, column=5, padx=10, pady=20)
            Button(self.root, text="web15",  command=lambda: self.run_websiteExp1(15)).grid(row=9, column=5, padx=10, pady=20)
            Button(self.root, text="web16", command=lambda: self.run_websiteExp1(16)).grid(row=10, column=5, padx=10, pady=20)
            Button(self.root, text="web17",  command=lambda: self.run_websiteExp1(17)).grid(row=11, column=5, padx=10, pady=20)
            Button(self.root, text="web18", command=lambda: self.run_websiteExp1(18)).grid(row=12, column=5, padx=10, pady=20)
            Button(self.root, text="web19", command=lambda: self.run_websiteExp1(19)).grid(row=7, column=6, padx=10, pady=20)
            Button(self.root, text="web20",  command=lambda: self.run_websiteExp1(20)).grid(row=8, column=6, padx=10, pady=20)

            #Label(self.root, text=self.websites['website1'], font='Times 14').grid(row=7, column=2, pady=20)
            #Label(self.root, text=self.websites['website2'], font='Times 14').grid(row=8, column=2, pady=20)
            #Label(self.root, text=self.websites['website3'], font='Times 14').grid(row=9, column=2, pady=20)
            #Label(self.root, text=self.websites['website4'], font='Times 14').grid(row=10, column=2, pady=20)
            #Label(self.root, text="To change website configuration please edit 'websites.txt' file",
            #      font='Times 16').grid(row=14, column=2, pady=20)

            def on_closing():

                self.root.destroy()

            close_but = Button(self.root, text="Close", command=on_closing)
            close_but.grid(row=15, column=3, padx=10, pady=20)

            self.parent.columnconfigure(6)
            self.parent.bind("<Return>", lambda e: self.web1())
        else:
            self.no_participant1.config(text="No mode selected!")

            self.finish = Label(self.root, text="", font='Times 14')
            self.finish.grid(row=11, column=2, pady=20)

    def run_websiteExp1(self, type):
        #self.experiment = True
        if self.settings == "lab":
            labExp = ey.run_browser_experiment(os.getcwd() + self.websites['website21'], type, self.participantId, self.parent,
                                               self.root, True)
            labExp.runexpweb()
        elif self.settings == "home":
            WebsiteExperiment.launch_browser(os.getcwd() + self.websites['website21'], type, self.participantId,
                                             self.root, self.settings, False)
        else:
            self.no_participant1.config(text="No mode selected!")
    #-------------------------------------Image Experiment-------------------------------------------

    def run_expimage(self):
        if self.settings == "lab":
            """
            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTracker.runexpImage(self.participantId)
                os.startfile(
                    "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")"""

            ey.runexpImage(self.participantId)
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        elif self.settings == "home":
            self.inst_win = Toplevel()
            self.inst_win.title("Instruction")
            self.inst_win.attributes('-fullscreen', True)

            fp = open('ffmpeg.txt', 'r')
            self.reso = json.load(fp)
            fp.close()

            img_5 = ImageTk.PhotoImage(master=self.inst_win, image=Image.open(os.getcwd() + '/Instructions.png'))
            tk.Label(self.inst_win, image=img_5).pack()

            ttk.Button(self.inst_win, text="Start Experiment!", command=self.start_image_exp).pack()

            self.inst_win.mainloop()
            os.startfile(
                "https://docs.google.com/forms/d/e/1FAIpQLSfZ89WXRbBi00SrtwIb7W_FLGMzkd9IkS8Ot5McfHF137sCqA/viewform")

        else:
            self.no_participant1.config(text="No mode selected!")

    def countdown(self, remaining=None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.chronometer.configure(text="time's up!")
        else:
            self.chronometer.configure(text="remaining %d" % self.remaining)
            self.remaining = self.remaining - 1
            self.top.after(1000, self.countdown)

    def start_image_exp(self):

        self.inst_win.destroy()
        self.top = Toplevel()
        self.top.title("Image Experiment")
        self.top.geometry("1100x900")
        self.top.attributes('-fullscreen', True)

        frame_1 = tk.Frame(self.top)
        frame_1.columnconfigure(0, weight=1)
        frame_1.pack()

        fp1 = open('images.txt', 'r')
        counts = json.load(fp1)
        fp1.close()

        durations = [int(counts['count_1']), int(counts['count_2']), int(counts['count_3']), int(counts['count_4'])]
        total_duration = sum(durations)
        self.time_conversion = str(timedelta(seconds=total_duration))

        (h, m, s) = self.time_conversion.split(':')
        duration_result = int(h) * 3600 + int(m) * 60 + int(s)

        self.chronometer = tk.Label(frame_1, text=" ", width=20)
        self.chronometer.grid(row=0, column=2)
        self.remaining = 0
        self.countdown(duration_result)

        frame_2 = ttk.Frame(self.top)
        frame_2.columnconfigure(1, weight=2)
        frame_2.pack()

        cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.participantId, 1, 0, False,
                                                                                  self.time_conversion))
        cam1.start()
        sc = threading.Thread(target=ScreenRecording.ScreenRec,
                              args=(self.participantId, 1, 0, False, self.time_conversion))
        sc.start()

        directory = os.getcwd() + '/Image Experiment'

        for image_file in os.listdir(directory):
            image_path = os.path.join(directory, image_file)
            image_show = Image.open(image_path)
            image_show = image_show.resize((1000, 600), Image.ANTIALIAS)
            image_PIL = ImageTk.PhotoImage(master=frame_2, image=image_show)
            self.images_list.append(image_PIL)

        label1 = tk.Label(frame_2, image=self.images_list[self.count_number])
        label1.pack()

        # transition of images based on the user defined count timer
        def img_count(count):
            if count == 0:
                self.top.after_cancel(self.after_id)
                self.count_number += 1
                label1.config(image=self.images_list[self.count_number])
                iterateCounter(self.count_number)
            else:
                self.after_id = self.top.after(1000, img_count, count - 1)

        def iterateCounter(count_number):
            if count_number == 0:
                img_count(int(durations[0]))
            if count_number == 1:
                img_count(int(durations[1]))
            if count_number == 2:
                img_count(int(durations[2]))
            if count_number == 3:
                img_count(int(durations[3]))
            if count_number == 4:
                self.top.destroy()

        # iterate the individual counters based on the user defined count timers
        iterateCounter(self.count_number)

        def next_image():
            if self.count_number == 0:
                img_count(0)
            elif self.count_number == 1:
                img_count(0)
            elif self.count_number == 2:
                img_count(0)
            elif self.count_number == 3:
                img_count(0)
            else:
                self.top.destroy()

        ttk.Button(frame_1, command=next_image, text="Skip").grid(row=0, column=10, pady=5)

        self.top.mainloop()

    # ------------------------------------------- END -----------------------------------------------
    # -------------------------------------Video Experiment-------------------------------------------

    def run_expvideo(self):
        # self.video_ep = 1
        # little test here (should be reworked) (make the experiment INSIDE expgiulia.py)
        if self.settings == "lab":
            # eyeTrackerV.runexpVideo(self.participantId)

            if self.camera_on is False:
                print("You need to turn the camera on")
            else:
                eyeTrackerV.runexpVideo(self.participantId)

        elif self.settings == "home":
            self.video_win = Toplevel()
            self.video_win.title("Instruction")

            img_5 = ImageTk.PhotoImage(master=self.video_win, image=Image.open(os.getcwd() + '/Instructions.png'))
            tk.Label(self.video_win, image=img_5).pack()
            ttk.Button(self.video_win, text="Start Experiment!", command=self.start_video_exp).pack()

            self.video_win.mainloop()

        else:
            self.no_participant1.config(text="No mode selected!")

    def start_video_exp(self):
        self.video_win.destroy()
        self.video_win = tk.Toplevel()
        self.video_win.title("Experiment VLC media player")
        # top.geometry('700x500')
        self.frame = True
        vp.Player(self.video_win, self.frame, title="tkinter vlc")


    # ------------------------------------------- END -----------------------------------------------
    def switch_lab(self):
        if (self.settings == 'lab'):
            self.no_participant1.config(text="Already in the lab setting Mode!")
        else:
            self.no_participant1.config(text="lab setting Mode selected!")
            self.settings = 'lab'

    def GSR_rec(self, pat, id, type):
        main = GSR_rec.Record(pat, id, type)
        main.create_stream()
        main.on_rec()

    def start_camera(self):
        if (self.settings == 'lab') & (self.experiment == True):
            self.camera_on = True
            if self.imag_exp == 1:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording,
                                        args=(self.participantId, 1, 0, self.frame,
                                              self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.participantId, 1, 0, True,
                                                                              self.time_conversion))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.participantId, 1, 0))
                gsr.start()
            elif self.imag_exp == 2:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.participantId, 2, 0,
                                                                                          self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec,
                                      args=(self.participantId, 2, 0, self.time_conversion))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.participantId, 2, 0))
                gsr.start()
            elif self.imag_exp == 3:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.participantId, 3, 1,
                                                                                          self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.participantId, 3, 1,
                                                                              self.time_conversion))
                sc.start()
                gsr = threading.Thread(target=self.GSR_rec, args=(self.participantId, 3, 1))
                gsr.start()

        elif (self.settings == 'home') & (self.experiment == True):
            self.camera_on = True
            if self.imag_exp == 1:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording,
                                        args=(self.participantId, 1, 0, self.frame,
                                              self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec, args=(self.participantId, 1, 0, self.frame,
                                                                              self.time_conversion))
                sc.start()

            elif self.imag_exp == 2:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.participantId, 2, 0,
                                                                                          self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec,
                                      args=(self.participantId, 2, 0, self.time_conversion))
                sc.start()

            elif self.imag_exp == 3:
                cam1 = threading.Thread(target=ffmpeg_video_audio.Camera_recording, args=(self.participantId, 3, 1,
                                                                                          self.time_conversion))
                cam1.start()
                sc = threading.Thread(target=ScreenRecording.ScreenRec,
                                      args=(self.participantId, 3, 1, self.time_conversion))
                sc.start()
        else:
            self.no_participant1.config(text="experiment is not started yet!")

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
            if str(p['id']) == self.participantId:
                user = p
                break

        if user is not None:

            ttk.Label(top, text="Participant n " + self.participantId, font='Times 26').grid(row=0, column=1, pady=30,
                                                                                         padx=20)
            ttk.Label(top, text="Age :  " + user['age'], font='Times 18').grid(row=1, column=1, sticky=tk.W, pady=20,
                                                                               padx=5)
            ttk.Label(top, text="Gender :  " + user['gender'], font='Times 18').grid(row=2, column=1, sticky=tk.W,
                                                                                     pady=20, padx=5)
            ttk.Label(top, text="Educational Level :  " + user['edu'], font='Times 18').grid(row=3, column=1,
                                                                                             sticky=tk.W, pady=20,
                                                                                             padx=5)



        else:
            ttk.Label(top, text="Data on Participant " + self.participantId + " not found.", font='Times 18').grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=5)
            top.rowconfigure(0, weight=1)

        ttk.Button(top, text="Close", command=top.destroy).grid(row=4, column=1, pady=50)
