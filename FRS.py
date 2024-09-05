import cv2
import face_recognition
import numpy as np
import pickle
import os

# Load registered faces and details
if os.path.exists("registered_faces.pkl"):
    with open("registered_faces.pkl", "rb") as f:
        registered_faces = pickle.load(f)
else:
    registered_faces = {}

def register_new_face(encoding):
    name = input("Enter your name: ")
    details = input(f"Enter details for {name}: ")
    registered_faces[name] = {"encoding": encoding, "details": details}
    with open("registered_faces.pkl", "wb") as f:
        pickle.dump(registered_faces, f)
    print(f"New face registered for {name} with details: {details}")

def recognize_faces():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            match = None
            for name, info in registered_faces.items():
                if face_recognition.compare_faces([info['encoding']], face_encoding)[0]:
                    match = name
                    break

            if match:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"{match}: {registered_faces[match]['details']}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                print(f"Recognized {match}: {registered_faces[match]['details']}")
            else:
                register_new_face(face_encoding)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

recognize_faces()
