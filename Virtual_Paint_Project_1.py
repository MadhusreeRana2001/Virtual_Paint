'''

--------------------------------- VIRTUAL PAINT ---------------------------------------------

As the name suggests, this code is used to create a Virtual Paint, which can draw beautiful
layers of colors according to the color of the color pen(s) or crayon(s) brought in front
of the webcam.

Note:
1. Try to execute the code against a distinct monochromatic background.
2. For referring to the BGR values of colors, go to this website:
https://www.rapidtables.com/web/color/RGB_Color.html

Developed by: Madhusree Rana

'''


import cv2
import numpy as np


FrameWidth, FrameHeight, FrameBrightness = 440, 580, 200


cap = cv2.VideoCapture(0)  # default id for single webcam on a laptop
cap.set(3, FrameWidth)  # id 3 is for width, which has been set to 440
cap.set(4, FrameHeight)  # id 4 is for height, which has been set to 580
cap.set(10, FrameBrightness)  # id 10 is for brightness, which has been set to 200


# HUE MIN, HUE MAX, SAT MIN, SAT MAX, VAL MIN, VAL MAX....  SAT -> Saturation, VAL -> Value
myColors = [[60, 96, 51, 255, 69, 255],  # for green color
         [0, 8, 130, 236, 74, 255],  # for red color
         [23, 35, 42, 255, 80, 255],  # for yellow color
         [102, 137, 63, 142, 41, 255]]  # for purple color


# contains the BGR values of the respective colors.
myColorValues = [[0, 255, 0],  # green
                [0, 0, 255],  # red
                [0, 255, 255],  # yellow
                [102, 0, 102]]  # purple


myPoints = []  # myPoints=[x,y,colorID], where colorID represents the ith color


def getContours(img):
    '''to find contours of the input image and the co-ordinates of the bounding box around
the contours'''
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)  # finding area for each contour
        if area > 500:  # checking the minimum area
            peri = cv2.arcLength(cnt, True)  # True signifies that the shape is closed
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y  # returning the co-ordinates of the centre of the tip of the pen


def findColor(img):
    '''to find the color(s) of the color pen(s) or crayon(s)'''
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # converting the BGR image to HSV image
    count = 0  # for keeping a track of the ith color
    newPoints = []
    for color in myColors:
        lower = np.array([color[0:6:2]])
        upper = np.array([color[1:6:2]])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)  # these are centre pts of tip of bounding box, not of contours
        if x != 0 and y != 0:
            cv2.circle(imgResult, (x, y), 15, myColorValues[count], cv2.FILLED)
            newPoints.append([x, y, count])
        count += 1
    return newPoints  # returns a list of lists


def drawOnCanvas(myPoints):
    '''to draw a layer of points of the same color as the color detected'''
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 15, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img)
    if len(newPoints) != 0:  # in case the values of x,y=0,0, so they aren't appended
        for newP in newPoints:  # each newP is actually the myPoints
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints)
    cv2.imshow("Result",imgResult)  # shows the output window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()