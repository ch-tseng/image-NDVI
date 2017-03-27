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

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="NDVI image")
ap.add_argument("-n", "--ndvi", required=True, help="Correct ndvi image.")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width = 800)

cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
channels = cv2.split(cspace)

V = createMask(channels[2], 220)
cv2.imshow("V", V)

S = createMask(channels[1], 135)  #NDVI green area
cv2.imshow("S", S)

H = (255 - S)
cv2.imshow("H", H)
#H = createMask(channels[0], 134)
#cv2.imshow("H", H)

#redCovered = cv2.merge([channels[0], channels[1], red])
cv2.imshow("Original", image)
#cv2.imshow("Red Area", redCovered)

cv2.imshow("NDVI Original", cv2.imread(args["ndvi"]))

cv2.waitKey(0)
