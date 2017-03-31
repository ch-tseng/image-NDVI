# import the necessary packages
from scipy.spatial import distance as dist
import imutils
import numpy as np
import cv2
import argparse

# use Standard NDVI method, smaller for larger area
thRED1 = 210
thYELLOW1 = 132
thGREEN1 = 0

# use LAB channels, smaller for larger area
thRED2 = 100
thYELLOW2 = 130
thGREEN2 = 125


def createMask(grayImg, th=104):
    masked = cv2.inRange(grayImg, th, 255)
    return masked

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

def getRedArea(image, thG=75, thY=132, thR=158):
    #thR =255 - thR
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #channels = cv2.split(cspace)
    #cv2.imshow("Red Channel", channels[2])
    mask = createMask(cspace[:,:,2], thR)   # NDVI red area
    return mask


def getGreenArea(image, thG=75, thY=132, thR=158):
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #channels = cv2.split(cspace)
    #cv2.imshow("H", channels[0])
    #cv2.imshow("S", channels[1])
    #cv2.imshow("V", channels[2])

    mask = createMask(cspace[:,:,1], thG)  #NDVI green area
    return mask

def getYellowArea(image, thG=75, thY=132, thR=158 ):
    thY =255 - thY
    cspace = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = createMask(cspace[:,:,1], thY)
    return (255-mask)

    #cspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    #mask = createMask(cspace[:,:,2], thY)   # NDVI yellow area
    #return mask

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

def ndvi1(image):
    b, g, r = cv2.split(image)
    divisor = (r.astype(float) + b.astype(float))
    divisor[divisor == 0] = 0.01  # Make sure we don't divide by zero!

    ndvi = (b.astype(float) - r) / divisor

    #Paint the NDVI image
    ndvi2 = contrast_stretch(ndvi)
    ndvi2 = ndvi2.astype(np.uint8)

    redNDVI = cv2.inRange(ndvi2, thRED1, 255)
    yellowNDVI = cv2.inRange(ndvi2, thYELLOW1, thRED1)
    greenNDVI = cv2.inRange(ndvi2, thGREEN1, thYELLOW1)
    merged = cv2.merge([yellowNDVI, greenNDVI, redNDVI])

    print('\nMax NDVI: {m}'.format(m=ndvi.max()))
    print('Mean NDVI: {m}'.format(m=ndvi.mean()))
    print('Median NDVI: {m}'.format(m=np.median(ndvi)))
    print('Min NDVI: {m}'.format(m=ndvi.min()))

    return merged

def ndvi2(image):
    #create mask
    redArea = getRedArea(image=image, thR=thRED2)
    greenArea = getGreenArea(image=image, thG=thGREEN2)
    yellowArea = getYellowArea(image=image, thY=thYELLOW2, thR=thRED2)

    redImage = image.copy()
    redImage[redArea == 255] = [0, 0, 255]
    cv2.imshow("red", redImage)

    yellowImage = image.copy()
    yellowImage[yellowArea == 255] = [5, 255, 252]
    cv2.imshow("yellow", yellowImage)

    greenImage = image.copy()
    greenImage[greenArea == 255] = [0, 255, 0]
    cv2.imshow("green", greenImage)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="NDVI image")
ap.add_argument("-n", "--ndvi", required=True, help="Correct ndvi image.")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
nimage = cv2.imread(args["ndvi"])
image = imutils.resize(image, width = 500)
nimage = imutils.resize(nimage, width = 500)
zeros = np.zeros(image.shape[:2], dtype = "uint8")

ndvi2(image)

#display original image
cv2.imshow("Original", image)

#caculate NDVI  value
ndviIMG1 = ndvi1(image)

#display standard NDVI
cv2.imshow("NDVI-Original", nimage)

cv2.waitKey(0)
