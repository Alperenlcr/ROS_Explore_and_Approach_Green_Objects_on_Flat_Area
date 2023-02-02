#!/usr/bin/env python
#--coding: utf-8 --
 
from numpy.lib.function_base import average
import rospy
import sys
import cv2
import numpy as np
import time
import imutils
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from time import sleep
from std_msgs.msg import String

def get_green_object_coordinates(data):
    #rate = rospy.Rate(10)
    
    bridge=CvBridge()
    cv_image=bridge.imgmsg_to_cv2(data, "bgr8")

    image = cv_image.copy()
    cv_image = cv2.cvtColor(cv_image,cv2.COLOR_RGB2BGR)
    imghsv = cv2.cvtColor(cv_image,cv2.COLOR_BGR2HSV)
    lower = np.array([32, 89, 21])
    upper = np.array([69, 255, 255])
    mask = cv2.inRange(imghsv, lower, upper)  
    result = cv2.bitwise_and(cv_image,cv_image, mask = mask)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)


    # Find contours and extract the bounding rectangle coordintes
    # then find moments to obtain the centroid
    cnts, hierarchy = cv2.findContours(result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cnts = imutils.grab_contours(cnts)
    #try:
    #    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    #except IndexError:
    #    print("Camera goruntusunde probe yok.")
    coordinate_x = []
    coordinate_y = []
    for c in cnts:
        # compute the center of the contour
        s = str(c[0])
        s = s[2:-2]
        temp = s.split()
        coordinate_x.append(int(temp[0]))
        coordinate_y.append(int(temp[1]))

        # draw the contour and center of the shape on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        # show the image
        cv2.imshow("Image", image)
        cv2.waitKey(1)
    print("[center_publisher]", end="     ")
    try:
        if int(average(coordinate_y)) > 400:
            center = [int(average(coordinate_x)), int(average(coordinate_y))]
            print("Green object coordinates : ",end="")
        else:
            center = [0,0]
            print("No green object", end=" ")
    except ValueError:
        center = [0,0]
        print("No green object", end=" ")

    p = str(center[0])+" "+str(center[1])
    print(p)
    pub.publish(p)
    if center[0] < 700 and center[0] < 580 and center[1] > 500 and center[1] < 550:
        print("\n\n\n\n\nhhhh\n\n\n\n")
        rospy.sleep(5)


if __name__=="__main__":
    rospy.init_node("center_publisher",anonymous=False)
    pub = rospy.Publisher('center', String, queue_size=10)
    image_sub = rospy.Subscriber("/gazebo/camera1/image_raw", Image, get_green_object_coordinates)
    rospy.spin()