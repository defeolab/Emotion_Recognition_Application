import os
import json

def screen_record():
    fp = open('ffmpeg.txt', 'r')
    mic = json.load(fp)
    fp.close()
    audio = mic['mic']
    video_size = mic['video_size']
    x = mic['x']
    y = mic['y']
    os.system(f"""ffmpeg -f gdigrab -t 00:00:10 -framerate 60 -offset_x 500 -offset_y 20 -video_size vga -i desktop -f dshow -t 00:00:10 -i audio="{audio}"  screen_rec.mp4""")

    #os.system(f"""ffmpeg -f gdigrab -show_region 1 -t 00:00:05 -framerate 60 -video_size {video_size} -offset_x {x} -offset_y {y} -i desktop -f dshow -t 00:00:10 -i audio="{audio}" screen_rec.mp4""")
#screen_record()
