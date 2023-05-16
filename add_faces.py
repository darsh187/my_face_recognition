import cv2
import pickle
import numpy as np
import os
import tkinter as tk

def save_info():
    global name, enrollment_number, phone_number, semester
    name = name_entry.get()
    enrollment_number = enrollment_entry.get()
    phone_number = phone_entry.get()
    semester = semester_entry.get()
    name_window.destroy()

name_window = tk.Tk()
name_window.title("Enter Information")

name_label = tk.Label(name_window, text="Name:")
name_label.pack(pady=10)
name_entry = tk.Entry(name_window)
name_entry.pack(pady=5)

enrollment_label = tk.Label(name_window, text="Enrollment Number:")
enrollment_label.pack(pady=10)
enrollment_entry = tk.Entry(name_window)
enrollment_entry.pack(pady=5)

phone_label = tk.Label(name_window, text="Phone Number:")
phone_label.pack(pady=10)
phone_entry = tk.Entry(name_window)
phone_entry.pack(pady=5)

semester_label = tk.Label(name_window, text="Semester:")
semester_label.pack(pady=10)
semester_entry = tk.Entry(name_window)
semester_entry.pack(pady=5)

submit_button = tk.Button(name_window, text="Submit", command=save_info)
submit_button.pack(pady=5)

name_window.mainloop()

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))
        
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        
        i = i + 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)
    
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

if 'names.pkl' not in os.listdir('data/'):
    names = [name] * 100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    
    names = names + [name] * 100
    
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    
    faces = np.append(faces, faces_data, axis=0)
    
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

data = {
    'enrollment_number': enrollment_number,
    'phone_number': phone_number,
    'semester': semester
}

with open('data/info.pkl', 'wb') as f:
    pickle.dump(data, f)