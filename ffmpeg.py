"""
Using ffmpeg to capture video and audio
"""

import os
#ffmpeg -list_devices true -f dshow -i dummy

import subprocess

def start():
    cmd = ('ffmpeg -f dshow -t 00:03:00 -i video="USB 2.0 Camera":audio="Realtek HD Audio 2nd output (Realtek High Definition Audio)" out.MP4 ')
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.STDOUT)


def stop():
    os.system('TaskKill /im ffmpeg.exe /F')
        #os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        #self.proc.kill() # <-- terminate the process

