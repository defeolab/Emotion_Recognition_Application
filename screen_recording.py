import os
import tkinter as tk
x= 0
def record():
	fld = "C:\\Users\\zeel9\\PycharmProjects\\ffmpeg\\output\\output"
	filename = fld + str(x) + ".mp4"

	audio = "Microphone Array (Realtek Audio)"
	video_size = "1366x768"

	os.system(f"""ffmpeg -y -rtbufsize 200M -f gdigrab -thread_queue_size 1024 -probesize 10M -r 10 -draw_mouse 1 -video_size {video_size} -t 00:00:15 -i desktop -f dshow -channel_layout stereo -thread_queue_size 1024 -t 00:00:15 -i audio="{audio}" -c:v libx264 -r 10 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p -c:a aac -strict -2 -ac 2 -b:a 128k -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" "{filename}" """)

def stop_rec():
	window.destroy()

if __name__ == "__main__":
	window = tk.Tk()
	window.geometry('300x300')
	window.title("Screen Recorder")

	btnStartRecording = tk.Button(window, text="Start Recording", command=lambda:record())
	btnStartRecording.place(x=90, y=120)

	btnStartRecording = tk.Button(window, text="stop Recording", command=lambda: stop_rec())
	btnStartRecording.place(x=90, y=200)

	window.mainloop()
