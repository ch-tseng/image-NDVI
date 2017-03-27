# import the necessary packages
from scipy.spatial import distance as dist
import imutils
import numpy as np
import cv2
import argparse

thRED = 158
thGREEN = 132
thYELLOW = 75

def addTransparent(overlay, output, alpha):
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def replaceColor(image, fromC=[0,0,0], toC=[255,255,255]):
    image[np.where((image==fromC).all(axis=2))] = toC
    return image

def createMask(grayImg, th=104):
    masked = cv2.inRange(grayImg, th, 255)
    return masked

def getRedArea1(image, th=104):
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(cspace)
    #cv2.imshow("L", channels[0])
    #cv2.imshow("A", channels[1])
    #cv2.imshow("B", channels[2])

    mask = createMask((255-channels[1]), th)   # NDVI red area
    return mask

def displayCspace(image, ctype="RGB"):
    if(ctype=="HSV"):
        cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif(ctype=="LAB"):
        cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    else:
        cspace = image

    channels = cv2.split(cspace)

    cv2.imshow("#1", channels[0])
    cv2.imshow("#2", channels[1])
    cv2.imshow("#3", channels[2])

def getRedArea(image, th=104):
    th =255 - th
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    channels = cv2.split(cspace)

    mask = createMask(channels[2], th)   # NDVI red area
    return mask


def getGreenArea(image, th=135):
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(cspace)
    #cv2.imshow("H", channels[0])
    #cv2.imshow("S", channels[1])
    #cv2.imshow("V", channels[2])

    mask = createMask(channels[1], th)  #NDVI green area
    return mask

def getYellowArea(image, th=124):
    th =255 - th
    #cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #channels = cv2.split(cspace)
    #mask = createMask(channels[1], th)   # NDVI yellow area
    YR = getRedArea(image, th)
    cv2.imshow("YR", YR)
    R = getRedArea(image, thRED)
    cv2.imshow("R", R)
    masked = cv2.bitwise_not(YR, YR, mask=R)

    return masked


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="NDVI image")
ap.add_argument("-n", "--ndvi", required=True, help="Correct ndvi image.")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width = 800)
zeros = np.zeros(image.shape[:2], dtype = "uint8")

#displayCspace(image, ctype="RGB")

#---
b, g, r = cv2.split(image)
image = cv2.merge([zeros, g, zeros])
#----
cv2.imshow("No Green", image)

redArea = getRedArea(image=image, th=thRED)
greenArea = getGreenArea(image=image, th=thGREEN)
yellowArea = getYellowArea(image=image, th=thYELLOW)

b, g, r = cv2.split(image)

merged = cv2.merge([greenArea, yellowArea, redArea])
cv2.imshow("Merged", merged)

dst = cv2.addWeighted(merged,0.5,image,0.5,0)
cv2.imshow("Total", dst)

'''
cv2.imshow("RED", maskedRED)
cv2.imshow("GREEN", maskedGREEN)
cv2.imshow("YELLOW", maskedYELLOW)
'''

cv2.waitKey(0)
