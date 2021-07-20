import tkinter as tk
import cv2
import time
import PIL
import numpy as np
from PIL import ImageTk
import gaze_tracking
import pandas as pd
import matplotlib.pyplot as plt
import patientWindow as pw
"""from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D"""


class App:
    def __init__(self, window, window_title, id, old_window,video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.PatientId = id
        self.old_window = old_window
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tk.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.btn_stop = tk.Button(window, text="STOP RECORDING", width=50, command=self.stop)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("data/snapshots/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def stop(self):
        cv2.destroyAllWindows()
        self.window.destroy()
        #self.vid.__del__()
        pw.PatientWindow(self.old_window, self.PatientId)

        # check this if it is replacable because it is creating problem
        self.vid.__del__()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)


class Faceless_app: # I show just a 'Stop record' Button
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        self.btn_stop = tk.Button(window, text="STOP RECORDING", width=50, command=self.stop)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)
        self.delay = 10
        self.update()


    def stop(self):
        self.window.destroy()
        self.vid.__del__()

    def update(self):
        # Get a frame from the video source

        self.vid.get_frame()
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        self.gaze = gaze_tracking.GazeTracking()

        #vid record
        capture = cv2.VideoCapture(0)

        # video recorder
        #fourcc = cv2.cv.CV_FOURCC(*'XVID')  # cv2.VideoWriter_fourcc() does not exist
        #video_writer = cv2.VideoWriter("output.avi", fourcc, 20, (680, 480))

        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #self.fer_model = self.get_emotion_prediction_label_model()
        self.coordinates = []
    def get_emotion_prediction_label_model(self):
        model = Sequential()

        model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
        model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(7, activation='softmax'))
        model.load_weights('./fer/model.h5')
        return model
    def get_emotion_label(self,frame):
        emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
        # face detection using CV2
        facecasc = cv2.CascadeClassifier('./fer/haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        maxindex = 4
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            # predict the label for each face in the frame by CNN model that using
            # cropped version of frame as an input
            prediction = self.fer_model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
        return emotion_dict[maxindex]
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            # add features to webcam input
            self.gaze.refresh(frame)
            frame = self.gaze.annotated_frame()
            # =========== added by Mostafa (Start) ===============================
            #predicted_label = self.get_emotion_label(frame)
            #cv2.putText(frame, "Emotion : " + predicted_label, (90, 230), cv2.FONT_HERSHEY_DUPLEX, 0.9,
            #            (147, 58, 31), 1)
            # =========== added by Mostafa (End) ===============================
            if ret:
                left_pupil = self.gaze.pupil_left_coords()
                right_pupil = self.gaze.pupil_right_coords()
                if (left_pupil is not None) & (right_pupil is not None):
                    self.coordinates.append([self.vid.get(cv2.CAP_PROP_FPS), left_pupil[0], left_pupil[1],right_pupil[0], right_pupil[1]])

                cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                            (147, 58, 31), 1)
                cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9,
                            (147, 58, 31), 1)
                # Return a boolean success flag and the current frame converted to BGR
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            raise ValueError("Unable to get a frame")

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            fieldnames = ['timestamp', 'left_pupil_x', 'left_pupil_y', 'right_pupil_x', 'right_pupil_y']

            my_df = pd.DataFrame(self.coordinates, columns=fieldnames)
            my_df.to_csv('test.csv', index=False, header=True)

            #heatmap in the end of the use of the camera
            x, y = my_df["left_pupil_x"], my_df["left_pupil_y"]
            plt.hist2d(x, y, bins=(50, 50), cmap=plt.cm.jet)
            plt.savefig('heatmap.png')
            self.vid.release()

