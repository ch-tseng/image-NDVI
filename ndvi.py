# import the necessary packages
from scipy.spatial import distance as dist
import imutils
import numpy as np
import cv2
import argparse

# for Normal NDVI caculation
thRED1 = 158
thGREEN1 = 132
thYELLOW1 = 75

# for NDVI myself
thRED2 = 158
thGREEN2 = 132
thYELLOW2 = 75


def addTransparent(overlay, output, alpha):
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def replaceColor(image, fromC=[0,0,0], toC=[255,255,255]):
    image[np.where((image==fromC).all(axis=2))] = toC
    return image

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
    R = getRedArea(image, thRED2)
    masked = cv2.bitwise_not(YR, YR, mask=R)

    return masked

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
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    b, g, r = cv2.split(image)
    divisor = (r.astype(float) + b.astype(float))
    divisor[divisor == 0] = 0.01  # Make sure we don't divide by zero!

    ndvi = (r.astype(float) - b) / divisor
    ndvi2 = contrast_stretch(ndvi)
    ndvi2 = ndvi2.astype(np.uint8)
    ndvi2 = (255-ndvi2)
    ndvi2 = cv2.inRange(ndvi2, thRED1, 255)
    #ndvi = cv2.bitwise_not(ndvi)
    merged = cv2.merge([g, r, ndvi2])

    print('\nMax NDVI: {m}'.format(m=ndvi.max()))
    print('Mean NDVI: {m}'.format(m=ndvi.mean()))
    print('Median NDVI: {m}'.format(m=np.median(ndvi)))
    print('Min NDVI: {m}'.format(m=ndvi.min()))

    return merged

def ndvi2(image):
    redArea = getRedArea(image=image, th=thRED2)
    greenArea = getGreenArea(image=image, th=thGREEN2)
    yellowArea = getYellowArea(image=image, th=thYELLOW2)

    b, g, r = cv2.split(image)

    merged = cv2.merge([greenArea, yellowArea, redArea])
    return merged

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="NDVI image")
ap.add_argument("-n", "--ndvi", required=True, help="Correct ndvi image.")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = imutils.resize(image, width = 800)
zeros = np.zeros(image.shape[:2], dtype = "uint8")

#displayCspace(image, ctype="RGB")

#My way
ndviIMG2 = ndvi2(image)

dst = cv2.addWeighted(ndviIMG2,0.6,image,0.4,0)
cv2.imshow("NDVI-2", dst)

ndviIMG1 = ndvi1(image)
cv2.imshow("NDVI-1", ndviIMG1)

cv2.waitKey(0)
