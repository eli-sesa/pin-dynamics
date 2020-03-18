# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:22:43 2020

@author: eli
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Hardcoding filenames that we care about.  COuld do with some listdir method
filenames = ['H1P0','H1P1','H2P0','H2P1','H3P0','H3P1','H4P0','H4P1']
filenames = [filenames[i] + 'thetadata.csv' for i in range(len(filenames))]

#Quick n dirty hardcoded ledgend names to make human readable
legend_names = ['Pin 1, No Flaps',
                'Pin 1 Flaps',
                'Pin 2 No Flaps',
                'Pin 2 Flaps',
                'Pin 3, No Flaps',
                'Pin 3 Flaps',
                'Pin 4, No Flaps',
                'Pin 4 Flaps',]

for filename in filenames:
    data = pd.read_csv(filename, delimiter= ',', names=['t', 'x', 'y', 'theta', 'theta_filt'], skiprows=1)

    t = data['t']
    # We can pull in either the raw or filtered data    
    theta = data['theta_filt']
    
    # find initial starting value
    theta0 = np.average(theta[0:100])

    # Define some range where we believe the pin is moving.  
    # Must be big enough to dodge noise but catch the beginning of the motion
    
    # Once the value dips below some percentage threshold
    # keep = theta < .99 * theta0
    # Or some fixed angle range (this more closely matches our 2 degree threshold in the dynamic model)
    keep = theta < theta0 - 2 
    
    # Find the times and angles with our moving condition applied
    t_trim = np.array(t[keep])
    theta_trim = theta[keep]

    
    # plt.plot(t, theta, '-o')
    plt.plot(t_trim - t_trim[0], theta_trim)
    plt.legend(legend_names)
    plt.xlabel('Time (shifted) [s]')
    plt.ylabel(r'$\theta   [deg]$')
    t_collapse = t_trim[-1] - t_trim[0]
    
    print(' The time to collapse for %s is %f' %(filename, t_collapse))
    '''
    
    thetad = np.diff(theta)
    plt.subplot(212)
    plt.plot(t[:-1],thetad)'''
