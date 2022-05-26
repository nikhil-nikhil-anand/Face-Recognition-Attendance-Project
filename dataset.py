import cv2
import numpy as np
import os
import time
import random


cap = cv2.VideoCapture(0)
name=input("Enter your name: ")

cap = cv2.VideoCapture(0)
time.sleep(0.5)
while True:
    ret, frame = cap.read()
    cv2.imwrite("Training_images/" + name + ".jpg", frame)
    cv2.imshow('Face Cropper', frame)
    count = 1
    if cv2.waitKey(1) & count == 1:
        break
        
cap.release()
cv2.destroyAllWindows()      
print("Collecting Samples Complete")