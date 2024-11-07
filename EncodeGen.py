import os
import cv2
import face_recognition

import pickle

folderpath = './db'
PathList = os.listdir(folderpath)
imgList = []
studentIds = []

for path in  PathList:
    imgList.append(cv2.imread(os.path.join(folderpath, path)))
    studentIds.append(os.path.splitext(path)[0])
#print(studentIds)
#print(len(imgList))

def findEncodings(imgageList):
    encodeList = []

    for img in imgageList:
        #img = cv2.cvtColor(imgageList, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodingListKnownWithIds = [encodeListKnown,studentIds]
print(encodeListKnown)
print("Encoding Complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodingListKnownWithIds,file)
file.close()
print("File Saved")