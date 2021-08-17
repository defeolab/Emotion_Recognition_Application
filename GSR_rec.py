import os
import json


class GSR_recording:
    def __init__(self, id):
        self.PatientID = id
#def GSR_recording():
        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()
        filename = "data/" + str(self.PatientID) +"/"+ str(self.PatientID)+"_gsr.wav"

        gsr = mic['mic']
        duration = mic['duration']
        file_path = "data/" + str(self.PatientID) + "/"
        if len(os.listdir(file_path)) == 0:
            print("Directory is empty")
        else:
            print("file removed")
            os.remove(filename)

        os.system(f"""ffmpeg -f dshow -t {duration} -i audio="{gsr}" -acodec libmp3lame -ab 128k -ac 2 -ar 44100 "{filename}" """)

#GSR_recording()