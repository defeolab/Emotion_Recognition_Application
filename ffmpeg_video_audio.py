"""
Using ffmpeg to capture video and audio
"""

import os
import json

class Camera_recording:

    def __init__(self, id):
        self.PatientID = id

        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()

        audio = mic['mic']
        video = mic['video']
        duration = mic['duration']
        filename = "data/" + str(self.PatientID) +"/"+ str(self.PatientID)+"_Camera_output.MP4"
        file_path = "data/" + str(self.PatientID)+ "/"
        if len(os.listdir(file_path)) == 0:
            print("Directory is empty")
        else:
            print("file removed")
            os.remove(filename)


        os.system(f"""ffmpeg -f dshow -t {duration} -i video="{video}":audio="{audio}" -vcodec libx264 -r 10 -vb 512k -s 640x360 "{filename}" """)

#ffmpeg -list_devices true -f dshow -i dummy

#Camera_recording()

