import sounddevice as sd
import soundfile as sf
import threading
import os
import json

class GSR_recording:
    def __init__(self, id,exp_type):
        self.ParticipantID = id
        self.exp_type = exp_type
        fp = open('ffmpeg.txt', 'r')
        duration = json.load(fp)
        fp.close()

        self.duration = duration['dur']
        self.sample_rate = 300000
        if self.exp_type == 3:
            self.filename = "data/Browser/" + str(self.ParticipantID) + "/" + str(self.ParticipantID) + "_GSR_rec.wav"
            file_path = "data/Browser/" + str(self.ParticipantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(self.filename):
                    print("file removed")
                    os.remove(self.filename)
                else:
                    print("No file exist")

        thread = threading.Thread(target=self.manage,
                                  kwargs=dict(frames=int(self.duration * self.sample_rate), samplerate=self.sample_rate,
                                              channels=2, blocking='False', sample=self.sample_rate,
                                              filename = self.filename), )
        thread.start()
        print(sd.query_devices())

    def manage(self,filename, sample, **soundfile_args):
        self.signal = sd.rec(**soundfile_args)
        sf.write(filename, self.signal, sample)




