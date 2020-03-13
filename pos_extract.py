# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:28:03 2020

@author: eli
"""

import cv2
import imutils
import skimage
import numpy as np
import matplotlib.pyplot as plt

def rgb2gray(image):
    R = image[:, :, 0]
    G = image[:, :, 1]
    B = image[:, :, 2]
    gray = 0.2989*R + 0.5870*G + 0.1140*B
    return np.array(gray)

cap = cv2.VideoCapture('pin.mp4')
# cv2.namedWindow('frame',cv2.WINDOW_NORMAL)

num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
og_size = np.array((1080, 1920))

scale_factor = 10

size = (og_size/scale_factor).astype('int')

data_mat = np.zeros((size[0], size[1], num_frames))

i = 0
pts = []
while(cap.isOpened()):
    ret, frame = cap.read()
    
        
    # cv2.imshow('frame', frame)
    # plt.pause(1/(250*480))
    # print(frame.shape)  
    
    # the color of the yellow part of motion tracker is hsv(51.87°, 61.15, 61.57) from pic pic
    
    # frame_bw = skimage.color.rgb2gray(frame)
    # data_mat[:,:,i] = skimage.transform.resize(frame_bw, size)
    # i +=1
    
    #blur image to reduce high frequency noise
    blurred = cv2.GaussianBlur(frame, (11, 11), 10)
    #We will work in hsv colorspace to enable easy thresholding 
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #set some expected threshold values from the known yellow color of object tracker
    lower_yellow = np.array([20, 120, 100])
    upper_yellow = np.array([60, 255, 255])
    
    #preserve pixels in the color range
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    #some morphological operations
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=10)
    
    #and if we want, this would return the image with mask applied
    res = cv2.bitwise_and(frame, frame, mask=mask)
    

    
    #here begins a bit more copy pasting.  Will want to debug / clean up. 
    
    #find the contours of the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)
    
    #some package that adrian from pyimagesearch used  
    cnts = imutils.grab_contours(cnts)
    
    #this takes
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    center = (int(x),int(y))
    radius = int(radius)
    
    pts.append(center)
    #     M = cv2.moments(c)
    # 	center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    
    # cv2.imshow('Contours', mask)	D
    cv2.circle(frame, center, radius, (0,0,255),5)
    cv2.imshow('test',frame)

    key = cv2.waitKey(5)
   
    if key == ord("q"):
        break
    
    if frame is None:
            cap.release()
            cv2.destroyAllWindows()
            
            break
    
#%%
coord = np.array(pts)

plt.plot(coord[:,0],coord[:,1],'-o')
    


#%%
data_mat = np.load('pin_w_flaps.npy')
#%%
        
def rank_approx(A_rel, rank):
# t h i s e x p e c t s rows wi t h mean 0
    U, S_vec , V = np.linalg.svd(A_rel, full_matrices=False)
    S = np.diag(S_vec)
    A_approx = U[:,0:rank] @ (S[0:rank , 0:rank] @ V[0:rank , :])
    return A_approx
#%%

delta = data_mat[:,:,:-1] - data_mat[:,:,1::]
data = data_mat - np.mean(data_mat, axis=2, keepdims=True)
A = np.reshape(data, (20736, 480))

U, S_vec, V = np.linalg.svd(A, full_matrices=False)
S = np.diag(S_vec)
rank = 5

A_approx = U[:,0:rank] @ (S[0:rank , 0:rank] @ V[0:rank , :])

A_approx_reshape = np.reshape(A_approx, (108, 192, 480))
for i  in range(480):
    plt.imshow(delta[:,:,i])
    plt.pause(1/250)
    plt.clf()
    print(i)