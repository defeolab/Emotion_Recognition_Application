import os
import json


class GSR_recording:
    def __init__(self, id, exp_type):
        self.PatientID = id
        self.exp_type = exp_type
        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()
        #filename = "data/" + str(self.PatientID) +"/"+ str(self.PatientID)+"_gsr.wav"

        gsr = mic['mic']
        duration = mic['duration']

        sampling_rate = mic['samplingrate']

        if self.exp_type == 3:
            filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_output.MP4"
            file_path = "data/Browser/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                print("file removed")
                os.remove(filename)

        #file_path = "data/" + str(self.PatientID) + "/"
        #if len(os.listdir(file_path)) == 0:
        #    print("Directory is empty")
        #else:
        #    print("file removed")
        #    os.remove(filename)

        os.system(f"""ffmpeg -f dshow -t {duration} -i audio="{gsr}" -acodec libmp3lame -ab 128k -ac 2 -ar {sampling_rate} "{filename}" """)

#GSR_recording()