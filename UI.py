import tkinter as tk
import subprocess

def run_add_faces():
    subprocess.run(["python", "add_faces.py"])

def run_take_attendance():
    subprocess.run(["python", "test.py"])



root = tk.Tk()
root.title("Face Recognition Attendance")

btn_add_faces = tk.Button(root, text="Add Faces", command=run_add_faces)
btn_add_faces.pack(pady=10)

btn_take_attendance = tk.Button(root, text="Take Attendance", command=run_take_attendance)
btn_take_attendance.pack(pady=10)

root.mainloop()
