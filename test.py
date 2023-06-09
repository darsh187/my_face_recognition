from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from tkinter import *

# root = Tk()
# root.geometry("655x333")
# root.title("Attendance")

# frame = Frame(root, borderwidth=6, bg="gray", relief=SUNKEN)
# frame.pack(side=LEFT, anchor="nw")

# b1 = Button(frame,fg="red", text="Take attendence")
# b1.place(x=0,y=0,width=220,height=40)

# root.mainloop()

def take_attendence():
    video=cv2.VideoCapture(0)
    facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

    with open('data/names.pkl', 'rb') as f:
        LABELS=pickle.load(f)
    with open('data/faces_data.pkl', 'rb') as f:
        FACES=pickle.load(f)
    # Read the values from the pickle file
    with open('data/info.pkl', 'rb') as f:
        data = pickle.load(f)

    enrollment_number = data['enrollment_number']
    phone_number = data['phone_number']
    semester = data['semester']


    knn=KNeighborsClassifier(n_neighbors=5)
    knn.fit(FACES, LABELS)

    imgBackground=cv2.imread("bgat.png")

    COL_NAMES = ['NAME', 'ENROLL', 'PHONE', 'SEM', 'TIME']

    while True:
        ret,frame=video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces=facedetect.detectMultiScale(gray, 1.3 ,5)
        for (x,y,w,h) in faces:
            crop_img=frame[y:y+h, x:x+w, :]
            resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
            output=knn.predict(resized_img)
            ts=time.time()
            date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
            cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
            cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
            attendance = [str(output[0]), str(enrollment_number), str(phone_number), str(semester),  str(timestamp)]
        imgBackground[162:162 + 480, 55:55 + 640] = frame
        cv2.imshow("Frame",imgBackground)
        k=cv2.waitKey(1)
        if k==ord('o'):
            if exist:
                with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)
            else:
                with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
                csvfile.close()
        if k==ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
root = Tk()
root.geometry("550x550")
root.title("fr sys")

b1 = Button(root, text="Click here for Attenedence",command=take_attendence,bg="lightblue")
b1.place(x=100,y=225,width=350,height=50)

root.mainloop()

