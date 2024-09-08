import cv2
import face_recognition
import numpy as np
import pickle
import os
from flask import Flask, render_template_string, jsonify
import threading

app = Flask(__name__)

recognized_faces = []

if os.path.exists("registered_faces.pkl"):
    with open("registered_faces.pkl", "rb") as f:
        registered_faces = pickle.load(f)

    for name, info in registered_faces.items():
        if 'encoding' in info:
            registered_faces[name]['encodings'] = [info['encoding']]
            del registered_faces[name]['encoding']
else:
    registered_faces = {}

def register_new_face(encoding):
    name = input("Enter your name: ")
    details = input(f"Enter details for {name}: ")
    registered_faces[name] = {"encodings": [encoding], "details": details}
    with open("registered_faces.pkl", "wb") as f:
        pickle.dump(registered_faces, f)
    print(f"New face registered for {name} with details: {details}")

@app.route('/')
def index():
    global recognized_faces
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Face Recognition Web Server</title>
    </head>
    <body>
        <h1>Recognized Faces</h1>
        <div id="faces">
        {% for face in faces %}
            <p>{{ face }}</p>
        {% endfor %}
        </div>
        <script>
        setInterval(function() {
            fetch('/faces').then(response => response.json()).then(data => {
                const facesDiv = document.getElementById('faces');
                facesDiv.innerHTML = '';
                data.faces.forEach(face => {
                    const p = document.createElement('p');
                    p.textContent = face;
                    facesDiv.appendChild(p);
                });
            });
        }, 1000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html, faces=recognized_faces)

@app.route('/faces')
def get_faces():
    return jsonify(faces=recognized_faces)

def recognize_faces():
    global recognized_faces
    video_capture = cv2.VideoCapture(0)

    TOLERANCE = 0.5  
    NUM_JITTERS = 2  
    while True:
        ret, frame = video_capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=NUM_JITTERS)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            match = None
            for name, info in registered_faces.items():
                matches = face_recognition.compare_faces(info['encodings'], face_encoding, tolerance=TOLERANCE)
                if True in matches:
                    match = name
                    break

            if match:
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"{match}: {registered_faces[match]['details']}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
                print(f"Recognized {match}: {registered_faces[match]['details']}")

                if f"{match}: {registered_faces[match]['details']}" not in recognized_faces:
                    recognized_faces.append(f"{match}: {registered_faces[match]['details']}")
            else:
                print("New face detected, registering...")
                register_new_face(face_encoding)

        if len(recognized_faces) > 10:
            recognized_faces = recognized_faces[-10:]

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

recognize_faces()
