import cv2
import face_recognition
import numpy as np
import pickle
import os
from tkinter import *
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

if os.path.exists("registered_faces.pkl"):
    with open("registered_faces.pkl", "rb") as f:
        registered_faces = pickle.load(f)
else:
    registered_faces = {}

tolerance = 0.5  

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        self.video_frame = Label(self.root)
        self.video_frame.pack(padx=10, pady=10)

        self.face_label = Label(self.root, text="Face: None", font=("Arial", 14))
        self.face_label.pack(pady=10)

        self.capture = cv2.VideoCapture(0)

        self.update_video_feed()

    def register_new_face(self, face_encoding):
        name = simpledialog.askstring("New Face Detected", "Enter your name:")
        if name:
            details = simpledialog.askstring("Details", "Enter details about yourself:")
            registered_faces[name] = {"encoding": face_encoding, "details": details}
            with open("registered_faces.pkl", "wb") as f:
                pickle.dump(registered_faces, f)
            messagebox.showinfo("Success", f"New face registered: {name} - {details}")
        else:
            messagebox.showwarning("Warning", "Face registration canceled")

    def update_video_feed(self):
        ret, frame = self.capture.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                match = None
                for name, info in registered_faces.items():
                    matches = face_recognition.compare_faces([info['encoding']], face_encoding, tolerance=tolerance)
                    if matches[0]:
                        match = name
                        break

                if match:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"{match} - {registered_faces[match]['details']}", (left, top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    self.face_label.config(text=f"Recognized: {match} - {registered_faces[match]['details']}")
                else:
                    self.register_new_face(face_encoding)

            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_frame.imgtk = imgtk
            self.video_frame.config(image=imgtk)

        self.root.after(10, self.update_video_feed)

    def on_closing(self):
        self.capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")  

    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
