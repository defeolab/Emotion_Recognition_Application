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
        if self.exp_type == 3:
            filename = "data/Browser/" + str(self.PatientID) + "/" + str(self.PatientID) + "_Camera_output.MP4"
            file_path = "data/Browser/" + str(self.PatientID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                print("file removed")
                os.remove(filename)

        #filename = "screen_rec.MP4"
        #filename = "data/" + str(self.PatientID) +"/"+ str(self.PatientID)+"_Screen_rec.MP4"
        #os.getcwd() + '/data/Video/' + str(id) + '/GSR_data/'
        #print(filename)
        #file_path = "data/" + str(self.PatientID) + "/"
        #if file_path is not None:
            # file_path = '/tmp/file.txt'
        #    os.remove(filename)
        #    print('filename removed')

        #else:
        #    print("no file")
        #if len(os.listdir(file_path)) == 0:
        #    print("Directory is empty")
        #else:
        #    print("file removed")
        #    os.remove(filename)

        os.system(f"""ffmpeg -f gdigrab -show_region 1 -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)

    #os.system(f"""ffmpeg -f gdigrab -show_region 1 -t {duration} -framerate 60 -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)

#screen_record()
