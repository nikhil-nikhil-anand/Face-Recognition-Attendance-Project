import face_recognition
import os
import cv2
import datetime
import numpy as np
from numpy import load
from json import JSONEncoder


KNOWN_FACES_DIR = 'Datasets'
TOLERANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'
video = cv2.VideoCapture(0)


def name_to_color(name):
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

t0= datetime.datetime.now()
print('Encoding faces...')
known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

t1 = datetime.datetime.now() - t0
print("Time elapsed: ", t1)

np.save('face_repr.npy', known_faces)
np.save('labels.npy', known_names)

print('.....SAVED.....\n')

print(name)


 