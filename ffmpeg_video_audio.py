"""
Using ffmpeg to capture video and audio
"""

import os
import json
import subprocess


class Camera_recording:

    def __init__(self, id, exp_type):
        self.PatientID = id
        self.exp_type = exp_type

        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()

        audio = mic['mic']
        video = mic['video']
        duration = mic['duration']
        framerate = mic['framerate']

        if self.exp_type == 1:
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
            filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_output.mp4"
            file_path = "data/Browser/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")


        os.system(f"""ffmpeg -f dshow -t {duration} -i video="{video}":audio="{audio}" -framerate {framerate} -rtbufsize 100M -vcodec libx264 -r 10 -vb 512k -s 640x360 "{filename}" """)

#ffmpeg -list_devices true -f dshow -i dummy

#Camera_recording()

