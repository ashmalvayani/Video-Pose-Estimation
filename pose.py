#for pose detection
from mmpose.apis import MMPoseInferencer
import cv2

#for pose estimation
import sys
import cv2
import os
from sys import platform
import argparse
from math import sqrt, acos, degrees, atan, degrees
import numpy as np

def extract_keypoints(vid_path):
    inferencer = MMPoseInferencer('human')

    cap = cv2.VideoCapture(vid_path)
    keypoints = []
    visualizations = []

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        result_generator = inferencer(frame, show=False, return_vis= True)
        result = next(result_generator)
        keypoints.append(result['predictions'][0][0]['keypoints'])

        visualizations.append(result['visualization'][0])

        print(visualizations[0].shape, visualizations)
        cv2.imwrite("frame1.jpg", visualizations[0])
        break
        
    cap.release()
    print(len(keypoints))

    return keypoints
  

def get_angle(a,b):
    del_y = a[1]-b[1]
    del_x = b[0]-a[0]
    if del_x == 0:
        del_x = 0.1

    angle = 0

    if del_x > 0 and del_y > 0:
        angle = degrees(atan(del_y / del_x))
    elif del_x < 0 and del_y > 0:
        angle = degrees(atan(del_y / del_x)) + 180

    return angle


def angle_gor(a,b,c,d):
    ab=[a[0]-b[0],a[1]-b[1]]
    ab1=[c[0]-d[0],c[1]-d[1]]
    cos=abs(ab[0]*ab1[0]+ab[1]*ab1[1])/(sqrt(ab[0]**2+ab[1]**2)*sqrt(ab1[0]**2+ab1[1]**2))
    ang = acos(cos)
    return ang*180/np.pi


def sit_ang(a,b,c,d):
	ang=angle_gor(a,b,c,d)
	s1=0
	if ang != None:
		if ang < 120 and ang>40:
			s1=1
	return s1

def sit_rec(a,b,c,d):
	ab = [a[0] - b[0], a[1] - b[1]]
	ab1 = [c[0] - d[0], c[1] - d[1]]
	l1=sqrt(ab[0]**2+ab[1]**2)
	l2=sqrt(ab1[0]**2+ab1[1]**2)
	s=0
	if l1!=0 and l2!=0:
		if l2/l1>=1.5:
			s=1
	return s
	
def detect_poses(keypoints):
    for j in range(len(keypoints)):
        x1=0
        x2=0
        s=0
        s1=0

        ang1 = get_angle(keypoints[j][8], keypoints[j][10])
        ang2 = get_angle(keypoints[j][7], keypoints[j][9])
        if (30 < ang1 < 150):
            x1 = 1
        if (30 < ang2 < 150):
            x2 = 1
        x3 = x1+x2

        if (x3 == 1):
            print("The {} person says: HELLO !".format(j+1))
        elif (x3 == 2):
            print("The {} person says: STOP PLEASE !".format(j+1))

        s  += sit_rec(keypoints[j][12], keypoints[j][14],keypoints[j][14], keypoints[j][16])
        s  += sit_rec(keypoints[j][11], keypoints[j][13], keypoints[j][13], keypoints[j][15])
        s1 += sit_ang(keypoints[j][12], keypoints[j][14], keypoints[j][14], keypoints[j][16])
        s1 += sit_ang(keypoints[j][11], keypoints[j][13], keypoints[j][13], keypoints[j][15])

        if s > 0 or s1>0:
            print("The {} person is sitting".format(j+1))
        if s == 0 and s1 == 0:
            print("The {} person is standing".format(j+1))

        print("___________________________")
        print("      ")


vid_path = 'sample.mp4'
keypoints = extract_keypoints(vid_path)
print(keypoints)
