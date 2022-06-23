import cv2
import numpy as np
import os
import time
import random
import psycopg2
from unicodedata import name
import requests
import json
import sys


cap = cv2.VideoCapture(0)
count = 0

get="get_student_details"
rollno=input("Enter your roll_no: ")
url="http://1.6.113.224/?action=" + get + "&rollno=" + rollno

response = requests.get(url)
parse_data = json.loads(response.text)

if(parse_data['data']==None):
    sys.exit("No Data Found")

if not os.path.exists("Datasets/" + rollno):
    os.mkdir("Datasets/" + rollno)
else:
    print("Directory already exists")

FirstName=parse_data['data']['FirstName']
MiddleName=parse_data['data']['MiddleName']
LastName=parse_data['data']['LastName']
DOB=parse_data['data']['DOB']
Semester=parse_data['data']['Semester']
Department=parse_data['data']['Department']

name = parse_data['data']['FirstName'] + " " + parse_data['data']['MiddleName']  + " " + parse_data['data']['LastName']
print("Name: " + name)
print("DOB: " + DOB)
print("semester: " + Semester)
print("Department: " + Department)

conn = psycopg2.connect(
host="localhost",
database="Student_Data",
user="postgres",
password="Nikhil37")
print ("Opened database successfully")

cur = conn.cursor()
cur.execute(''' insert into "StudentDetails" ("FirstName","MiddleName","LastName","DOB","RollNo","Semester","Department") values (%s ,%s ,%s ,%s ,%s ,%s ,%s) ;''',(FirstName,MiddleName,LastName,DOB,rollno,Semester,Department))
print("Records created successfully")

conn.commit()
conn.close()


def face_extractor(frame,count):
    n=0
    cropped_face = frame
    if count%6==0:
        return cropped_face
    elif count%6==1:
        cropped_face = cv2.GaussianBlur(cropped_face, (11, 11), 0)
        return cropped_face
    elif count%6==2:
        cropped_face = cv2.bilateralFilter(cropped_face, 9, 75, 75)
        return cropped_face
    elif count%6==3:
        alpha = random.uniform(0.5, 1.1)
        beta = random.randint(0,15)
        cropped_face = cv2.convertScaleAbs(cropped_face, alpha=alpha, beta=beta)
        return cropped_face
    elif count%6==4:
        return cropped_face
    elif count%6==5:
        return cropped_face


cap = cv2.VideoCapture(0)
count = -1

while True:

    ret, frame = cap.read()
    if face_extractor(frame,count) is not None:
        count += 1
        if count<1:
            continue
        face=face_extractor(frame,count)
        cv2.imwrite("Datasets/" + rollno + "/" +str(count) + ".jpg", face)
        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Face Cropper', face)
        if count >= 10:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()      
print("Collecting Samples Complete")