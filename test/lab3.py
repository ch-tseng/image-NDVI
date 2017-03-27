# import the necessary packages
from scipy.spatial import distance as dist
import imutils
import numpy as np
import cv2
import argparse

thRED = 220
thGREEN = 132
thYELLOW = 132

def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def getNDVI(image):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    b, g, r = cv2.split(image)
    divisor = (r.astype(float) + b.astype(float))
    divisor[divisor == 0] = 0.01  # Make sure we don't divide by zero!

    ndvi = (r.astype(float) - b) / divisor
    ndvi = contrast_stretch(ndvi)
    ndvi = ndvi.astype(np.uint8)
    ndvi = (255-ndvi)
    ndvi = cv2.inRange(ndvi, thRED, 255)
    #ndvi = cv2.bitwise_not(ndvi)

    zeros = np.zeros(image.shape[:2], dtype = "uint8")
    merged = cv2.merge([g, r, ndvi])
    cv2.imshow("Merged", merged)
    return ndvi

def addTransparent(overlay, output, alpha):
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def replaceColor(image, fromC=[0,0,0], toC=[255,255,255]):
    image[np.where((image==fromC).all(axis=2))] = toC
    return image

def createMask(grayImg, th=104):
    masked = cv2.inRange(grayImg, th, 255)
    return masked

def getRedArea(image, th=104):
    cv2.imshow("ndvi", image)
    #thresh = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)
    (T, thresh) = cv2.threshold(image, th,  255, cv2.THRESH_BINARY) 
    cv2.imshow("ndvi2", thresh )
    #cv2.imshow("ndvi3", cv2.inRange(thresh, th, 255) )
    #cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #channels = cv2.split(cspace)
    #cv2.imshow("L", channels[0])
    #cv2.imshow("A", channels[1])
    #cv2.imshow("B", channels[2])

    #mask = createMask((255-channels[1]), th)   # NDVI red area
    #return mask

def getRedArea2(image, th=104):
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
    #cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #channels = cv2.split(cspace)
    #mask = createMask(channels[1], th)   # NDVI yellow area
    th = 255 -th
    YR = getRedArea2(image, th)
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

ndvi = getNDVI(image)
cv2.imshow("ndvi", ndvi)
#blurred = cv2.GaussianBlur(ndvi, (5, 5), 0)
#getRedArea(image=ndvi, th=thRED)
#greenArea = getGreenArea(image=image, th=thGREEN)
#yellowArea = getYellowArea(image=image, th=thYELLOW)



"""
imgRED = np.zeros(image.shape[:3], np.uint8)
imgRED[:] = (1, 54, 253)
maskedRED = cv2.bitwise_and(imgRED, imgRED, mask=redArea)
imgGREEN = np.zeros(image.shape[:3], np.uint8)
imgGREEN[:] = (0, 249, 69)
maskedGREEN = cv2.bitwise_and(imgGREEN, imgGREEN, mask=greenArea)
imgYELLOW = np.zeros(image.shape[:3], np.uint8)
imgYELLOW[:] = (0, 255, 237)
maskedYELLOW = cv2.bitwise_and(imgYELLOW, imgYELLOW, mask=yellowArea)

greenNDVI = cv2.addWeighted(image, 0.5, maskedGREEN, 0.5, 0)
yellowNDVI = cv2.addWeighted(image, 0.5, maskedYELLOW, 0.5, 0)
redNDVI = cv2.addWeighted(image, 0.5, maskedRED, 0.5, 0)

cv2.imshow("NDVI Original", cv2.imread(args["ndvi"]))
cv2.imshow("NDVI-Green", greenNDVI)
cv2.imshow("NDVI-Yellow", yellowNDVI)
cv2.imshow("NDVI-Red", redNDVI)

cv2.imshow("RED", maskedRED)
cv2.imshow("GREEN", maskedGREEN)
cv2.imshow("YELLOW", maskedYELLOW)
"""
cv2.waitKey(0)
