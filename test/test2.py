import cv2
import numpy as np
import imutils

image = cv2.imread("../images/ndvi5.jpg")
image = imutils.resize(image, width = 800)

cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
channels = cv2.split(cspace)

red = channels[2]

cv2.imshow('red1', red)
#red[np.where( (red>150).all(axis=2)) ] = [255]
red2 = red[red>180, red=255, red=0]
cv2.imshow('red2', red2)
cv2.waitKey(0)

