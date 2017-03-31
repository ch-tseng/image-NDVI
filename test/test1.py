import cv2
import numpy as np
import imutils

def colorArea(image, lower, upper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(image,image, mask= mask)

    return res

image = cv2.imread("../images/ndvi5.jpg")
image = imutils.resize(image, width = 800)

# define range of blue color in HSV
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

lower_green = np.array([50,255,255])
upper_green = np.array([70,255,255])

cv2.imshow('oroginal',image)
cv2.imshow('blue', colorArea(image, lower_blue, upper_blue))
cv2.imshow('green',colorArea(image, lower_green, upper_green))

cv2.imshow('ndvi', cv2.imread("../images/ondvi5.jpg"))
cv2.waitKey(0)

