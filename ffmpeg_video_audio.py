"""
Using ffmpeg to capture video and audio
"""

import os
import json


class Camera_recording:

    def __init__(self, id, exp_type,type,frame):
        self.PatientID = id
        self.exp_type = exp_type
        self.type = type
        self.frame = frame




        if self.exp_type == 1:
            fp = open('ffmpeg.txt', 'r')
            ffmpegsettings = json.load(fp)
            fp.close()
            fp1 = open('images.txt', 'r')
            dur = json.load(fp1)
            fp1.close()

            audio = ffmpegsettings['mic']
            video = ffmpegsettings['video']
            video_home = ffmpegsettings['video_home']
            duration = dur['duration']#duration time can't recognise 60 sec, must be rounded to 1 min.
            framerate = ffmpegsettings['framerate']

            filename = "data/Image/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_output.mp4"
            file_path = "data/Image/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")

        if self.exp_type == 2:
            fp = open('ffmpeg.txt', 'r')
            ffmpegsettings = json.load(fp)
            fp.close()
            fp1 = open('video.txt', 'r')
            dur = json.load(fp1)
            fp1.close()

            audio = ffmpegsettings['mic']
            video = ffmpegsettings['video']
            video_home = ffmpegsettings['video_home']
            duration = dur['duration']
            framerate = ffmpegsettings['framerate']

            filename = "data/Video/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_output.mp4"
            file_path = "data/Video/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")

        if self.exp_type == 3:
            fp = open('ffmpeg.txt', 'r')
            ffmpegsettings = json.load(fp)
            fp.close()
            fp1 = open('websites.txt', 'r')
            dur = json.load(fp1)
            fp1.close()

            audio = ffmpegsettings['mic']
            video = ffmpegsettings['video']
            video_home = ffmpegsettings['video_home']
            duration = dur['duration']
            framerate = ffmpegsettings['framerate']

            if self.type == 1:
                filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_web1_output.mp4"
                file_path = "data/Browser/" + str(self.PatientID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 2:
                filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_web2_output.mp4"
                file_path = "data/Browser/" + str(self.PatientID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 3:
                filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_web3_output.mp4"
                file_path = "data/Browser/" + str(self.PatientID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 4:
                filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_web4_output.mp4"
                file_path = "data/Browser/" + str(self.PatientID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            else:
                print("no experiment!")
        if self.frame == True :
            os.system(f"""ffmpeg -f dshow -t {duration} -i video="{video}":audio="{audio}" -framerate {framerate} -rtbufsize 1000M -vcodec libx264 -r 10 -vb 512k -s 640x360 "{filename}" """)
        else:
            os.system(f"""ffmpeg -f dshow -t {duration} -i video="{video_home}":audio="{audio}" -framerate {framerate} -rtbufsize 1000M -vcodec libx264 -r 10 -vb 512k -s 640x360 "{filename}" """)


#ffmpeg -list_devices true -f dshow -i dummy


