import os
import cv2
import numpy as np
import face_recognition
from datetime import datetime

#Loading images using path
path = 'Images'
images = []
names = []
List = os.listdir(path)
#print(List)

for name in List:
    img = cv2.imread(f'{path}/{name}')
    images.append(img)
    names.append(os.path.splitext(name)[0])

#print(names)

#Function to find encodings for all images in directory

def encode(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeImg = face_recognition.face_encodings(img)[0]
        encode_list.append(encodeImg)
    return encode_list

def record_attendance(name):
    with open('attendance.csv', 'r+') as file:
        List = file.readlines()
        namelist = []

        for line in List:
            record = line.split(',')
            namelist.append(record[0])
        if name not in namelist:
            now = datetime.now()
            dt = now.strftime('%H:%M:%S')
            file.writelines(f'\n{name},{dt}')

print("Encoding Images...")
encodeList = encode(images)
print("Encoding Completed.")

#Initializing webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    #Reducing size of real-time image to 1/4th
    imgResize = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgResize = cv2.cvtColor(imgResize, cv2.COLOR_BGR2RGB)

    # Finding face in current frame
    face = face_recognition.face_locations(imgResize)
    # Encode detected face
    encodeImg = face_recognition.face_encodings(imgResize, face)

    #Finding matches with existing images
    for encodecurr, loc in zip(encodeImg, face):
        match = face_recognition.compare_faces(encodeList, encodecurr)
        faceDist = face_recognition.face_distance(encodeList, encodecurr)
        print(faceDist)
        #Lowest distance will be best match
        index_BestMatch = np.argmin(faceDist)

        if match[index_BestMatch]:
            name = names[index_BestMatch]
            y1,x2,y2,x1 = loc
            #Retaining original image size for rectangle location
            y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),1)
            cv2.rectangle(img,(x1,y2-30),(x2,y2), (255,0,255), cv2.FILLED)
            cv2.putText(img, name, (x1+8, y2-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,255),2)
            record_attendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)



