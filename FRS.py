import cv2
import face_recognition
import numpy as np
import pickle
import os
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

if os.path.exists("registered_faces.pkl"):
    with open("registered_faces.pkl", "rb") as f:
        registered_faces = pickle.load(f)
else:
    registered_faces = {}

def register_new_face(face_encoding):
    root = tk.Tk()
    root.withdraw()

    name = simpledialog.askstring("New Face Detected", "Enter your name:")
    if name is None:  
        root.destroy()
        return

    details = simpledialog.askstring("New Face Detected", "Enter additional details:")
    if details is None: 
        root.destroy()
        return

    subject = simpledialog.askstring("New Face Detected", "Enter the subject:")
    if subject is None:  
        root.destroy()
        return

    standard = simpledialog.askstring("New Face Detected", "Enter the standard:")
    if standard is None:  
        root.destroy()
        return

   
    registered_faces[name] = {
        "encoding": face_encoding,
        "details": details if details else "N/A",
        "subject": subject if subject else "N/A",
        "standard": standard if standard else "N/A"
    }
    
    with open("registered_faces.pkl", "wb") as f:
        pickle.dump(registered_faces, f)
    
    root.destroy()

def main():
   
    capture = cv2.VideoCapture(0)

    root = tk.Tk()
    root.title("Face Recognition System")

    video_label = tk.Label(root)
    video_label.pack()

    face_label = tk.Label(root, text="Face: None", font=('Helvetica', 14))
    face_label.pack()

    details_box = tk.Text(root, height=5, width=50, font=('Helvetica', 14))
    details_box.pack()

    def update_frame():
        ret, frame = capture.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                match = None
                for name, info in registered_faces.items():
                    matches = face_recognition.compare_faces([info['encoding']], face_encoding, tolerance=0.5)
                    if matches[0]:
                        match = name
                        break

                top, right, bottom, left = face_location
                if match:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    face_label.config(text=f"Recognized: {match}")

                    details_box.delete('1.0', tk.END)
                    details_box.insert(tk.END, f"Details: {registered_faces[match].get('details', 'N/A')}\n")
                    details_box.insert(tk.END, f"Subject: {registered_faces[match].get('subject', 'N/A')}\n")
                    details_box.insert(tk.END, f"Standard: {registered_faces[match].get('standard', 'N/A')}")

                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    register_new_face(face_encoding)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)

            video_label.config(image=imgtk)
            video_label.image = imgtk

        video_label.after(10, update_frame)

    update_frame()

    root.mainloop()

    capture.release()

if __name__ == '__main__':
    main()
