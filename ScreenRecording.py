import os
import json

class ScreenRec:
    def __init__(self, id, exp_type,type,frame, duration):
        self.participantID = id
        self.exp_type = exp_type
        self.type = type
        self.frame = frame
        self.duration = duration

    #def screen_record(self):
        if self.exp_type == 1:
            fp = open('ffmpeg.txt', 'r')
            ffmpegsettings = json.load(fp)
            fp.close()

            fp1 = open('images.txt', 'r')
            dur = json.load(fp1)
            fp1.close()

            audio = ffmpegsettings['mic']
            video_size = ffmpegsettings['video_tobii']
            x = ffmpegsettings['x']
            y = ffmpegsettings['y']

            duration = self.duration
            print('existing duration ', self.duration)
            print('new duration ', dur['duration'])

            frame_rate = ffmpegsettings['framerate']
            filename = "data/Image/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_rec.mp4"
            file_path = "data/Image/" + str(self.participantID) + "/"
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
            video_size = ffmpegsettings['video_tobii']
            x = ffmpegsettings['x']
            y = ffmpegsettings['y']

            duration = dur['duration']

            frame_rate = ffmpegsettings['framerate']
            filename = "data/Video/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_rec.mp4"
            file_path = "data/Video/" + str(self.participantID) + "/"
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
            video_size = ffmpegsettings['video_tobii']
            x = ffmpegsettings['x']
            y = ffmpegsettings['y']

            duration = dur['duration']

            frame_rate = ffmpegsettings['framerate']
            filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen" + str(self.type) + "rec.mp4"
            file_path = "data/Browser/" + str(self.participantID) + "/"
            if len(os.listdir(file_path)) == 0:
                print("Directory is empty")
            else:
                if os.path.exists(filename):
                    print("file removed")
                    os.remove(filename)
                else:
                    print("No file exist")
                    # os.system(f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)
            if self.frame == True:
                        os.system(
                            f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" -rtbufsize 100M "{filename}" """)
            else:
                        os.system(
                            f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {0} -offset_y {0} -i desktop -f dshow -t {duration} -i audio="{audio}" -rtbufsize 100M "{filename}" """)


"""
            if self.type == 1:
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_web1_rec.mp4"
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
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_web2_rec.mp4"
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
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_web3_rec.mp4"
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
                filename = "data/Browser/" + str(self.participantID) + "/" + str(self.participantID) + "_Screen_web4_rec.mp4"
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
                print("No experiment")
"""
        #os.system(f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" "{filename}" """)
        #if self.frame == True :
        #    os.system(f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t {duration} -i audio="{audio}" -rtbufsize 100M "{filename}" """)
        #else:
        #    os.system(
        #        f"""ffmpeg -f gdigrab -t {duration} -framerate {frame_rate} -video_size {video_size} -offset_x {0} -offset_y {0} -i desktop -f dshow -t {duration} -i audio="{audio}" -rtbufsize 100M "{filename}" """)


    #screen_record(self)
