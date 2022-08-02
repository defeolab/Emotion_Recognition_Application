"""
Using ffmpeg to capture video and audio
"""

import os
import json

# import patientWindow
#
# main_instance = patientWindow.PatientWindow()
# sub_instance = main_instance.start_image_exp()
# print('data from ffpeg video audio',sub_instance.duration_result)

class Camera_recording:

    def __init__(self, id, exp_type,type,frame, img_dur = None):
        self.participantID = id
        self.exp_type = exp_type
        self.type = type
        self.frame = frame
        self.img_dur = img_dur

        # 1: Image Experiment
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
            # duration = dur['duration']#duration time can't recognise 60 sec, must be rounded to 1 min.
            duration = self.img_dur
            print('existing duration ',self.img_dur)
            print('new duration ', dur['duration'])

            framerate = ffmpegsettings['framerate']

            filename = "data/Image/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_output.mp4"
            file_path = "data/Image/" + str(self.participantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")

        # 2: Video Experiment
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

            filename = "data/Video/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_output.mp4"
            file_path = "data/Video/" + str(self.participantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")

        # 3: Web Experiment
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

            # TYpe of websites
            if self.type == 1:
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_web1_output.mp4"
                file_path = "data/Browser/" + str(self.participantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 2:
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_web2_output.mp4"
                file_path = "data/Browser/" + str(self.participantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 3:
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_web3_output.mp4"
                file_path = "data/Browser/" + str(self.participantID) + "/"
                if len(os.listdir(file_path)) == 0:
                    print("Directory is empty")
                else:
                    if os.path.exists(filename):
                        print("file removed")
                        os.remove(filename)
                    else:
                        print("No file exist")

            elif self.type == 4:
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Camera_web4_output.mp4"
                file_path = "data/Browser/" + str(self.participantID) + "/"
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


