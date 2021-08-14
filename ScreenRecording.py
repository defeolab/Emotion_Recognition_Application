import os
import json

def screen_record():
    fp = open('ffmpeg.txt', 'r')
    mic = json.load(fp)
    fp.close()
    audio = mic['gsr']
    video_size = mic['video_size']
    #os.system("""ffmpeg -f dshow -t 00:00:15 -i video="screen-capture-recorder" -video_size {video_size} output.mp4""")
    #os.system("""ffmpeg -f gdigrab -t 00:00:15 -i desktop -video_size 2560x1440 -offset_x 2560 -offset_y 0 output.mp4""")

    #os.system(f"""ffmpeg -f dshow -t 00:00:15 -i video="screen-capture-recorder" -offset_x 1440 -offset_y 0 -video_size 2560x1440 -framerate 25 out.mp4""")
    os.system("""ffmpeg -f gdigrab -t 00:00:15 -framerate 6 -offset_x 50 -offset_y 28 -video_size vga -i desktop screen_rec.mp4""")


    #os.system(f"""ffmpeg -y -rtbufsize 200M -f dshow -i video="screen-capture-recorder" -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)
    #os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

    #os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

#screen_record()
