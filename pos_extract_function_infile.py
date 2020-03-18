#  -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:47:28 2020

@author: eli
"""

import cv2
import imutils
import skimage
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal


def get_coord(filename, origin, PLOT=True):
    
    # Initalize some variables for loop logic
    i = 0
    none_frames = 0
    # some large radius preallocation to avoid immeadtly breaking loop
    radius = 100
    
    # empty lists for appending.  Converted to numpy arrays at the end
    t = []
    pts = []
    
    
    cap = cv2.VideoCapture(filename)
    
    # Again, hardcoded for this application.  Extend for further applications
    framerate = 1000
    
    while(cap.isOpened()):
    
        ret, frame = cap.read()
        
        # If the video ends, there are 20 empty detections, or the radius gets small
        # corresponding to detecting the marker in the skate body, break the loop
        if frame is None or none_frames > 20 or radius < 25:
            cap.release()
            cv2.destroyAllWindows()
            break
        
        # Typical image processing, blur to reduce noise.
        blurred = cv2.GaussianBlur(frame, (11, 11), 10)
        
        # convert to hue saturation value.  this is easier to pull colorbands
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # set some expected threshold values from the known yellow color of object tracker
        # This is highly application dependent for extent to future projects.  Requires some trial and error
        lower_yellow = np.array([30, 50, 85])
        upper_yellow = np.array([70, 255, 255])
        
    
        # Convert to binary mask
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # morphological operations to reduce binary image noise
        #  mask = cv2.erode(mask, None, iterations=1)
        
        # This dialation is CRUCIAL to merge contours..  Cannot currently handle multiple contours
        mask = cv2.dilate(mask, None, iterations=10)
        
        # this result can help visualize whats going on, but is not used for anything else
        res = cv2.bitwise_and(frame, frame, mask=mask)
    
        # find contours.  That was easy; Thanks opencv!
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        		cv2.CHAIN_APPROX_SIMPLE)
        
        #  This is some magic pulled from pyimagesearch.  Need to learn what it does
        cnts = imutils.grab_contours(cnts)
    
        # If we dont see any frames for some time, we want to kill the loop
        if len(cnts) == 0:
            none_frames += 1
            pts.append((np.NaN, np.NaN))
            
        else:
            # Take the biggest contour 
            c = max(cnts, key=cv2.contourArea)
            # enclose the contour with a circle to track the point
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            center = (int(x),int(y))
            radius = int(radius)
            
            # Store the centerpoint for each timestep
            pts.append(center)
            
            # Add circle for the detected point and origin for each frame
            cv2.circle(frame, center, radius, (0,0,255),5)
            cv2.circle(frame, origin, 50, (0,0,255), 5)
        
        # We can watch the movie play while this happens
        if PLOT:
            cv2.imshow('test',frame)
            
            key = cv2.waitKey(0)
            if key == ord("q"):
                print(radius)
                break
        
        
        # Count time throughtout the videos.  This is sloppy
        t.append(i * (1/framerate))
        i+=1

    # After the loop, convert to numpy and the x,y space we expect
    pts = np.array(pts)
    x = np.array(pts[:,0]) - origin[0]
    # hardcoded frame height.  This should be extended to a general video frame
    y =  1920 - np.array(pts[:,1]) - origin[1]
    
    return np.array(t), x, y, pts


filenames = ['H1P0','H1P1','H2P0','H2P1','H3P0','H3P1','H4P0','H4P1']
filenames = [filenames[i] + '.mp4' for i in range(len(filenames))]

# turns out that for the most part the origin is the same.  
# This is MEGA SLOPPY, but allowed for fast guess and check origin finding
origins = [(320,895), (320,895), (320,895), (265,905), (320,895), (320,895), (320,895), (320,895)]


for filename, origin in zip(filenames, origins):
#  case = 4
#  filename = filenames[case]
#  origin = origins[case]
    
    # update whats going on
    print('Processing... ' + filename)
    
    # Call our function
    t, x, y, ~ = get_coord(filename, origin, PLOT=False)
    
    theta = np.arctan(x/y)
    # arctan returns negative values for negative xs.  Add pi to offset this where negative
    
    #  theta = np.nan_to_num(theta)
    keep = np.logical_not(np.isnan(theta))    
    
    t_true = t[keep]
    x_true = x[keep]
    y_true = y[keep]
    theta_true = theta[keep]
    
    #  theta_true = np.where(theta_true<0, theta_true+np.pi/2, theta_true)
    
    # Take the angle that we found and convert to global angle space
    # Also convert to degrees so that we can understand
    theta_true = np.rad2deg(np.pi/2 - theta_true)
    
    # Filter the noisy data using a zerophase, second order butterworth filter
    sos = scipy.signal.butter(2, .25, output='sos')
    
    # sometimes the last value jumps.  Just filter all but the last
    # to conserve length of vectors.  This is some sketchy patch
    theta_filt = scipy.signal.sosfiltfilt(sos, theta_true[:-1])
    theta_filt = np.append(theta_filt, theta_filt[-1])
    
    # preallocate for data output
    data_out = np.zeros((len(t_true), 5))
    
    data_out[:,0] = t_true
    data_out[:,1] = x_true
    data_out[:,2] = y_true
    data_out[:,3] = theta_true
    data_out[:,4] = theta_filt

    # record what the columns are, and the origin used.  
    # This data includes both raw extracted and some calculated values. 
    # Should allow others to use the data
    
    note = 'columns t, x, y, theta, theta_filtered.  origin = %s' %(origin,)
    np.savetxt(filename[:-4] + 'thetadata.csv', data_out, delimiter=',', header=note)
    
    # Plot what we get 
    plt.figure()
    plt.plot(t_true, theta_true, '-o')
    plt.plot(t_true, theta_filt, 'r')
    plt.title(filename)
