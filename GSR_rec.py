import os
import json

def GSR_recording():
    fp = open('ffmpeg.txt', 'r')
    mic = json.load(fp)
    fp.close()

    gsr = mic['gsr']

    os.system(f"""ffmpeg -f dshow -t 00:00:05 -i audio="{gsr}" -acodec libmp3lame -ab 128k -ac 2 -ar 44100 gsr.wav""")

#GSR_recording()