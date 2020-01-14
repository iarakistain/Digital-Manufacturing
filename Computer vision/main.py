from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import constants as c
from skittle import SKITTLE
import numpy as np
from copy import deepcopy

# cap = cv2.VideoCapture('skittles.mp4')
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
font = cv2.FONT_HERSHEY_SIMPLEX

pinkSkittle = []
yellowSkittle = []
orangeSkittle = []
greenSkittle = []
brownSkittle = []

ID = 0

pinkCtr = 0
yellowCtr = 0
orangeCtr = 0
greenCtr = 0
brownCtr = 0

pts_L1= np.array([[0, 220],[400, 220]])

def applyHSVRanges(frame, low, high):
    mask = cv2.inRange(f, low, high)
    return mask

def detectSkittle(mask, color, multiplier):
    global ID, pinkSkittle, pinkCtr, yellowSkittle, yellowCtr, orangeSkittle, orangeCtr, greenSkittle, greenCtr, brownSkittle, brownCtr
    skit = []
    skitCtr = 0
    if color == 'Pink':
        skit = deepcopy(pinkSkittle)
        skitCtr = deepcopy(pinkCtr)
        textColor = (147, 20, 255)
    if color == 'Yellow':
        skit = deepcopy(yellowSkittle)
        skitCtr = deepcopy(yellowCtr)
        textColor = (0, 255, 255)
    if color == 'Orange':
        skit = deepcopy(orangeSkittle)
        skitCtr = deepcopy(orangeCtr)
        textColor = (0, 120, 255)
    if color == 'Brown':
        skit = deepcopy(brownSkittle)
        skitCtr = deepcopy(brownCtr)
        textColor = (0, 20, 200)
    if color == 'Green':
        skit = deepcopy(greenSkittle)
        skitCtr = deepcopy(greenCtr)
        textColor = (0, 255, 0)
    _, contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>c.areaTH:
            # print(area)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            # print(x, y, w, h)
            for s in skit:
                s.setAge(s.getAge()+1)
                if s.getAge()>5:
                    skit.remove(s)
            new = True
            for s in skit:
                #Implement if a skittle goes out of frame it is deleted
                _, posY = s.getPosition()
                if abs(cy - posY)<=c.yTh:
                    new = False
                    s.setPosition(cx, cy)
                    s.setAge(0)
                    break
            if new:
                skit.append(SKITTLE(cx, cy, color, ID))
                ID = ID + 1
                # skit[ID-1].setPosition(cx, cy)

            # cv2.putText(f, color + str(ID), (x,y), font,1,(0,0,255), 2,cv2.LINE_AA)
            cv2.circle(f,(cx,cy), int(h/2), (0,0,255), 5)
            # skit[ID-1].setPosition(cx, cy)
    for s in skit:
        skitCtr = s.countSkittles(pts_L1[0,1], skitCtr)
    cv2.putText(f, color + ": "+ str(skitCtr), (15, 15 + multiplier*c.offset), font,0.5,textColor, 2,cv2.LINE_AA)
    # print(skitCtr)
    if color == 'Pink':
        pinkSkittle = deepcopy(skit)
        pinkCtr = deepcopy(skitCtr)
    if color == 'Yellow':
        yellowSkittle = deepcopy(skit)
        yellowCtr = deepcopy(skitCtr)
    if color == 'Orange':
        orangeSkittle = deepcopy(skit)
        orangeCtr = deepcopy(skitCtr)
    if color == 'Brown':
        brownSkittle = deepcopy(skit)
        brownCtr = deepcopy(skitCtr)
    if color == 'Green':
        greenSkittle = deepcopy(skit)
        greenCtr = deepcopy(skitCtr)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # r, f = cap.read()
    f = frame.array
    if not r:
        break
    R, C, Z = f.shape
    # f = f[:, 50:C-225]
    hsvFrame = cv2.cvtColor(f, cv2.COLOR_RGB2HSV)

    maskY = applyHSVRanges(hsvFrame, c.yMin, c.yMax)
    detectSkittle(maskY, 'Yellow', 0)
    maskP = applyHSVRanges(hsvFrame, c.pMin, c.pMax)
    detectSkittle(maskP, 'Pink', 1)
    maskO = applyHSVRanges(hsvFrame, c.oMin, c.oMax)
    detectSkittle(maskO, 'Orange', 2)
    # maskB = applyHSVRanges(hsvFrame, c.bMin, c.bMax)
    # detectSkittle(maskB, 'Brown', 3)
    maskG = applyHSVRanges(hsvFrame, c.gMin, c.gMax)
    detectSkittle(maskG, 'Green', 4)

    f = cv2.polylines( f, [pts_L1], False, (255,0,0),thickness=4)
    cv2.imshow('f', f)
    # cv2.imshow('mask', maskY)
    k = cv2.waitKey(20)
    if k == 27:
        break
