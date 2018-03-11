import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import sys

# all inputs must be tuples
#return the angle pivoted by target
def calculateAngle(target, top, bottom):
    # find length of all sides of triangle
    a = math.sqrt((top[0] - bottom[0])**2 + (top[1] - bottom[1])**2)
    b = math.sqrt((target[0] - top[0])**2 + (target[1] - top[1])**2)
    c = math.sqrt((bottom[0] - target[0])**2 + (bottom[1] - target[1])**2)

    # apply cosine rule here
    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57 # arc cos(a) or arc cos(far)
    return angle

cap = cv2.VideoCapture(0)
file = open("centerPointsData.txt", "a+")
while(cap.isOpened()):
    # read image
    ret, img = cap.read()

    # get hand data from the rectangle sub window on the screen
    cv2.rectangle(img, (300,300), (100,100), (0,255,0),0)
    crop_img = img[100:300, 100:300]

    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # thresholdin: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # show thresholded image
    cv2.imshow('Thresholded', thresh1)

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version == '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)

    # find contour with max area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt)
    print(len(hull))
    #print(hull)
    clusterhull = []
    X = []
    Y = []
    for point in hull:
        clusterhull.append(point[0]) 
        X.append(point[0][0])
        Y.append(point[0][1])
        #print(tuple(point[0]), end="")
    print(clusterhull)
    # here to detect left and right gestures first

    # first cluster the hull points
    Z = np.float32(clusterhull)

    # define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    if len(hull) >= 5:
        ret,label,center=cv2.kmeans(Z,5,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        # k = 5
        #print(center)
        #print(center[0])
        plt.scatter(X,Y)
        # get a convex hull of the clustered points
        Xcenter = []
        Ycenter = []
        for c in center:
            Xcenter.append(c[0])
            Ycenter.append(c[1])
            file.write(str(c[0]))
            file.write(' ')
            file.write(str(c[1]))
            file.write(' ')
        plt.scatter(Xcenter, Ycenter, marker = 's')
        # clusterhull = cv2.convexHull(center)
        # print("right arrow point:", end = " ")
        # print(clusterhull[0][0]) # right target 
        # file.write(str(clusterhull[0][0][0])) #x
        # file.write(' ')
        # file.write(str(clusterhull[0][0][1])) #y
        # file.write(' ')
        #rightAngle = calculateAngle(tuple(clusterhull[0][0]), tuple(clusterhull[1][0]), tuple(clusterhull[len(clusterhull)-1][0]))

        # print("right arrow angle:", end = " ")
        # print(rightAngle)
        # print(clusterhull)

        # now calculate left arrow angle
        # file.write(str(rightAngle)) 
        # file.write(' ')
        # first find the minX point from the clusterhull
        # minX = [200, 200]
        # i = 0
        # minIndex = 0
        # for point in clusterhull:
        #     if point[0][0] < minX[0]:
        #         minX = point[0]
        #         minIndex = i
        #     i = i+1

        # print("left arrow point:", end = " ")
        # print(minX)
        # file.write(str(minX[0])) # x
        # file.write(' ')
        # file.write(str(minX[1])) # y
        # file.write(' ')
        #print(clusterhull[minIndex])
        # then get the two neighor points of the minX
        # calculate the angle formed targeted at minX point
        # leftAngle = calculateAngle(tuple(clusterhull[minIndex][0]), tuple(clusterhull[(minIndex+1) % len(clusterhull)][0]), tuple(clusterhull[minIndex-1][0]))
        # print("left arrow angle:", end = " ")
        # file.write(str(leftAngle))
        # file.write(' ')
        # print(leftAngle)
        # if leftAngle < rightAngle and clusterhull[0][0][1] > minX[1]:
        #     print("go left")
        # elif rightAngle < 95 and clusterhull[0][0][1] > 50 and clusterhull[0][0][1] < minX[1]:
        #     print("go right")

        plt.show()
        # if angle < 90 then a right arrow 

    
    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    if type(defects) != type(None):
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]

            start = tuple(cnt[s][0])# points
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57 # arc cos(a) or arc cos(far)

            # ignore angles > 90 and highlight rest with red dots
            if angle <= 90:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0,0,255], -1)
            #dist = cv2.pointPolygonTest(cnt,far,True)
            #if angle > 90:
                #print(angle)
            # draw a line from start to end i.e. the convex points (finger tips)
            # (can skip this part)
            cv2.line(crop_img,start, end, [0,255,0], 2)
            #cv2.circle(crop_img,far,5,[0,0,255],-1)

    # defects are the number of vertices in the convex hull
    # define actions required
    if count_defects == 1:
        cv2.putText(img,"I am Siyuan", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 2:
        string = "This is a basic hand gesture recognizer"
        cv2.putText(img, string, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img,"This is 4 :P", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 4:
        cv2.putText(img,"Hi!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    else:
        cv2.putText(img,"Hello World!!!", (50, 50),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)


    # show appropriate images in windows
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

    text = input("left is 1, right is 2, pause is 3, 0 for others")
    file.write(text)
    file.write('\n')

    k = cv2.waitKey(10)
    if k == 27:
        file.close()
        break
