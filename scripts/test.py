import numpy as np
import cv2 as cv
import pytesseract
import time


filename = './Faze_Invitational/C9_TSM_group.mp4'
cap = cv.VideoCapture(filename)

cloud9 = ['Tenz', 'shinobi', 'vice', 'Relyks', 'mitch']
tsm = ['WARDELL', 'hazed', 'reltuC', 'drone', 'Subroza']
players = cloud9 + tsm
# poi = players of interest
# povs = point of views
poi = ['TenZ', 'WARDELL']
povs = {}
for player in poi:
    povs[player] = cv.VideoWriter((player + '.mp4'), cv.VideoWriter_fourcc(*'mp4v'), 60, (int(cap.get(3)),int(cap.get(4))))



count = 0
spectating = ['']
current_pov = None
while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    crop = frame[850:875, 125:250]
    #cv.imshow('frame', crop)
    count += 1
    if count % 60 == 0:
        text = pytesseract.image_to_string(crop, lang='eng')[:-2]
        if text in poi:
            current_pov = text
        elif spectating[-1] == current_pov:
            pass
        else:
            current_pov = None
        spectating.append(text)
    if current_pov:
        povs[current_pov].write(frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
for key in povs:
    povs[key].release()
cv.destroyAllWindows()

