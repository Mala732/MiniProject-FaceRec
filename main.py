import os.path
import datetime
import subprocess
import numpy as np
import tkinter as tk
import cv2
import face_recognition
from PIL import Image, ImageTk
from face_recognition import face_encodings
import pickle
import util

import cvzone


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+50+30")

        self.login_button_main_window = util.get_button(self.main_window, 'Mark Attendence', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)
        #
        # self.known_face_names = []
        # self.known_face_encodings = []
        #
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.csv'

        self.Encode()

    def add_webcam(self, label):
        # pass
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(1)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        #pass
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)


    def login(self):
        #pass
        # unknown_img_path = './.tmp.jpg'
        #
        # cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        #
        # unknown_image = face_recognition.load_image_file(unknown_img_path)
        # unknown_face_locations = face_recognition.face_locations(unknown_image,number_of_times_to_upsample=3)
        # print("I found {} face(s) in this photograph.".format(len(unknown_face_locations)))
        #
        # for face_location in unknown_face_locations:
        #
        #     # Print the location of each face in this image
        #     top, right, bottom, left = face_location
        #     print(
        #         "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
        #                                                                                               right))
        #
        #     # You can access the actual face itself like this:
        #     face_image = unknown_image[top:bottom, left:right]
        #     pil_image = Image.fromarray(face_image)
        #     check_img_path = './.check_img.jpg'
        #     pil_image.save(check_img_path)
        #     output = str(subprocess.check_output(['face_recognition',self.db_dir,check_img_path]))
        #     name = output.split(',')[1][:-3]
        #
        #     if name in ['unknown_person', 'no_persons_found']:
        #         util.msg_box('Ups...', 'Unknown user. Please register new user or try again.')
        #     else:
        #         util.msg_box('Welcome back !', 'Welcome, {}.'.format(name))
        #         with open(self.log_path, 'a') as f:
        #             f.write('{},{}\n'.format(name, datetime.datetime.now()))
        #             f.close()
        #         os.remove(check_img_path)
        #
        #
        # util.msg_box('Ups...','Attendance Marked')
        # #os.remove(check_img_path)
        # os.remove(unknown_img_path)
        unknown = 0
        success, img =  self.cap.read()
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        print("I found {} face(s) in this photograph.".format(len(faceCurFrame)))

        if len(faceCurFrame) == 0:
            util.msg_box('OOPS...', 'No Faces Detected.Please Try Again')

        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurFrame):
            matches = face_recognition.compare_faces(self.encodeListKnown, encodeFace)
            faceDist = face_recognition.face_distance(self.encodeListKnown, encodeFace)

            print("matches", matches)
            print("faceDist", faceDist)

            if min(faceDist)> 0.6:
                unknown +=1
            matchIndex = np.argmin(faceDist)
            print("matchIndex", matchIndex)

            if matches[matchIndex]:
                print("Known face detected")
                print(self.studentIds[matchIndex])
                # util.msg_box('Welcome back !', 'Welcome, {}.'.format(self.studentIds[matchIndex]))
                with open(self.log_path, 'a') as f:
                    f.write('{},{}\n'.format(self.studentIds[matchIndex], datetime.datetime.now()))
                    f.close()
        if unknown :
            util.msg_box('OOPS...', '{} unknown faces detected out of {}. Please register new user/s or '
                                    'try again'.format(unknown, len(faceCurFrame)))

        util.msg_box('Attendence Marked !', 'Attencence Marked for {} out of {} students'.format(len(faceCurFrame),len(faceCurFrame)-unknown))











    def register_new_user(self):
        #pass
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+75+35")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)




    def try_again_register_new_user(self):
        #pass
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        #pass
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()


    def start(self):
        self.main_window.mainloop()

    def Encode(self, folderpath = './db'):
        PathList = os.listdir(folderpath)
        imgList = []
        self.studentIds = []

        for path in PathList:
            imgList.append(cv2.imread(os.path.join(folderpath, path)))
            self.studentIds.append(os.path.splitext(path)[0])

        # print(studentIds)
        # print(len(imgList))

        def findEncodings(imgageList):
            encodeList = []

            for img in imgageList:
                # img = cv2.cvtColor(imgageList, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        print("Encoding Started...")
        self.encodeListKnown = findEncodings(imgList)
        self.encodingListKnownWithIds = [self.encodeListKnown, self.studentIds]
        print(self.encodeListKnown)
        print("Encoding Complete")

        file = open("EncodeFile.p", 'wb')
        pickle.dump(self.encodingListKnownWithIds, file)
        file.close()
        print("File Saved")


    def accept_register_new_user(self,folderpath = './db'):
        #pass
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)
        self.Encode()
        util.msg_box('Success!', 'User was registered successfully !')

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()