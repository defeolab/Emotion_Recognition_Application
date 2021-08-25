import os
import json

class ScreenRec:
    def __init__(self, id, exp_type):
        self.PatientID = id
        self.exp_type = exp_type

    #def screen_record(self):
        fp = open('ffmpeg.txt', 'r')
        mic = json.load(fp)
        fp.close()
        audio = mic['mic']
        video_size = mic['video_size']
        x = mic['x']
        y = mic['y']
        duration = mic['duration']
        frame_rate = mic['framerate']
        if self.exp_type == 1:
            filename = "data/Image/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Screen_rec.MP4"
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
            filename = "data/Video/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Screen_rec.MP4"
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
            filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Screen_rec.MP4"
            file_path = "data/Browser/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")


        #os.system(f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)

        os.system(f"""ffmpeg -f gdigrab -show_region 1 -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)

#screen_record()
