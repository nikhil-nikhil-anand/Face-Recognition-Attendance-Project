from tkinter import TRUE
from flask import Flask, render_template, Response
import cv2
import face_recognition
import os
import cv2
import datetime
import time
import numpy as np
from numpy import load
import random
import psycopg2
from unicodedata import name

app = Flask(__name__)

KNOWN_FACES_DIR = 'known_faces'
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn '
camera = cv2.VideoCapture(0)

conn = psycopg2.connect(
host="localhost",
database="Student_Data",
user="postgres",
password="Nikhil37")
print ("Opened database successfully")

known_faces = []
known_names = []
process_this_frame = True

known_faces = list(load('face_repr.npy'))
known_names = list(load('labels.npy'))

attendance = []

def gen_frames():
    while True:
        success, image = camera.read()  
        if not success:
            break
        else:
            locations = face_recognition.face_locations(image, model=MODEL)
            encodings = face_recognition.face_encodings(image, locations)
            
            for face_encoding, face_location in zip(encodings, locations):
                results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
                match = None 
                if True in results:  
                    match = known_names[results.index(True)]
                    attendance.append(match)
                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    #color = name_to_color(match)
                    cv2.rectangle(image, top_left, bottom_right, (0,0,0), FRAME_THICKNESS)
                    top_left = (face_location[3], face_location[2])
                    bottom_right = (face_location[1], face_location[2] + 22)
                    cv2.rectangle(image, top_left, bottom_right, (0,0,0), cv2.FILLED)
                    cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()    
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

attendance=list(set(attendance))
print(attendance)
ct = str(datetime.datetime.now())

cur = conn.cursor()
for at in attendance:
    cur.execute(''' insert into "recognitionlog" ("datetime","recognition_status","hall_id","rollno") values (%s ,%s ,%s ,%s) ;''',(ct,'1',2,at))
print("Records created successfully")


conn.commit()
conn.close()