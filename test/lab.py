# import the necessary packages
from scipy.spatial import distance as dist
import imutils
import numpy as np
import cv2
import argparse

def replaceColor(image, fromC=[0,0,0], toC=[255,255,255]):
    image[np.where((image==fromC).all(axis=2))] = toC
    return image

def createMask(grayImg, th=104):
    masked = cv2.inRange(grayImg, th, 255)
    return masked

def getRedArea(image, th=104):
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    channels = cv2.split(cspace)
    cv2.imshow("L", channels[0])
    cv2.imshow("A", channels[1])
    cv2.imshow("B", channels[2])

    mask = createMask(channels[2], th)   # NDVI red area
    return mask

def getGreenArea(image, th=135):
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    channels = cv2.split(cspace)
    cv2.imshow("H", channels[0])
    cv2.imshow("S", channels[1])
    cv2.imshow("V", channels[2])

    mask = createMask(channels[1], th)  #NDVI green area
    return mask

def getYellowArea(image, th=124):
    #cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #channels = cv2.split(cspace)
    #mask = createMask(channels[1], th)   # NDVI yellow area
    yellow = (255 -  getGreenArea(image, 255-th))
    return yellow

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="NDVI image")
ap.add_argument("-n", "--ndvi", required=True, help="Correct ndvi image.")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width = 800)

redArea = getRedArea(image=image, th=105)
greenArea = getGreenArea(image=image, th=132)
yellowArea = getYellowArea(image=image, th=153)

#cv2.imshow("Original", image)
cv2.imshow("NDVI Original", cv2.imread(args["ndvi"]))
cv2.imshow("RED", redArea)
cv2.imshow("GREEN", greenArea)
cv2.imshow("YELLOW", yellowArea)

cv2.waitKey(0)
