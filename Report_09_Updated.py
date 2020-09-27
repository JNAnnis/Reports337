# -*- coding: utf-8 -*-

"""
Report 9: Global Positioning System

Stumbledown Algorithm: comprises of repeatedly taking randomly generated steps
from a current position and only accepting the steps that are considered better
then the current position.

Stumbledown Reducing Algorithm: consists of keeping track of the number of 
failed steps and reducing the stepsize after a set number of failures.

The 2D GPS Problem:
    1) The calculated distance of a location (x, y) from a satellite, i, is 
    
    calculated_i = sqrt((x - x_i)^2 + (y - y_i)^2)
    
    2) The mismatch between a satellite, i, and a location (x, y) is given by
    the difference between the calculated distance and the actual reported 
    satellite distance 
    
    mismatch_i = calculated_i - d_i
    
    3) The GPS error is given by the sum of the mismatches of all the 
    satellites. To make sure the error is positive, the mismatches are squared.
    
    Error = sum(mismatch_i)^2
    
    Finding this unknown location (x, y) can now be considered an optimization 
    problem where the error is minimized.
"""


import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand


# Stumbledown Algorithm Exercise
def testf(x, y):
    
    """
    Contains the function to be minimized by the stumbledown algorithm.
    
    Parameters:
        x (float): x coordinate
        
        y (float): y coordinate
        
    Returns:
        f (float): value obtained after evaluating the function at the point
        (x, y)
    """
    
    f = (x - 5)**2 + (y - 3)**2 + 17
    
    return f


def stumbledown(f, p, stepSize, nSteps):
    
    """
    Implements the stumbledown algorithm.
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        points (array[float]): contains all of the (x, y) points, the function
        value of the points, and whether the new point was better than the 
        current point (True if new < current, False if new > current)
    """
    
    points  = np.empty((nSteps, 4))
    points[0] = [*p, f(*p), True]
    
    
    for i in range(1, nSteps):
        step = rand(2)*2*stepSize - stepSize
        q = p + step
        if f(*q) < f(*p):
            p = q
            points[i] = [*p, f(*p), True]
        else:
            points[i] = [*p, f(*p), False]
    
    return points


def print_stumbledown(f, p, stepSize, nSteps):
    
    """
    Prints the results of the stumbledown algorithm. (Run in console)
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        none
    """
    
    print("{:8}{:12}{:11}{:10}{}".format("Steps","Success","x","y","f(x,y)"))
    print("________________________________________________")
    
    info = stumbledown(f, p, stepSize, nSteps)
    
    for i in range(nSteps):
        if info[i, 3] == True:
            success = 'Yes'
        else:
            success = '   '
            
        print("{:2}{:>11}{:11.3f}{:11.3f}{:13.3f}".format(i, success, 
                                            info[i,0], info[i,1], info[i,2]))


# Stumbledown Reducing Algorithm Exercise
def stumbledown_reducing(f, p, stepSize, nSteps):
    
    """
    Implements the stumbledown reducing algorithm.
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        points (array[float]): contains all of the (x, y) points, the function
        value of the points, and whether the new point was better than the 
        current point (True if new < current, False if new > current)
    """
    
    points  = np.empty((nSteps, 4))
    points[0] = [*p, f(*p), True]
    
    i = 1 # current step
    counter = 0 # counts the number of fails
    factor = 0.5 # factor to decrease the step size by
    tolerance = 10**(-8)
    nFails = 5 # number of fails allowed before the step size is decreased
    multiplier = 0
    newStepSize = stepSize
    
    while newStepSize > tolerance and i < nSteps:
        newStepSize = stepSize*(factor**multiplier)
        step = rand(2)*(2*newStepSize) - newStepSize
        q = p + step
        
        if f(*q)<f(*p):
            p = q
            points[i] = [*p, f(*p), True]
        else:
            points[i] = [*p, f(*p), False]
            counter += 1
            
        if counter == nFails:
            multiplier += 1
            counter = 0 # reset the counter after reaching nfails
        i += 1 
                
    return points[:i]


def print_stumbledown_reducing(f, p, stepSize, nSteps):
    
    """
    Prints the results of the stumbledown algorithm. (Run in console)
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        none
    """
    
    print("{:8}{:12}{:11}{:10}{}".format("Steps","Success","x","y","f(x,y)"))
    print("________________________________________________")
    
    info = stumbledown_reducing(f, p, stepSize, nSteps)
    
    for i in range(nSteps):
        if info[i, 3] == True:
            success = 'Yes'
        else:
            success = '   '
            
        print("{:2}{:>11}{:11.3f}{:11.3f}{:13.3f}".format(i, success, 
                                            info[i,0], info[i,1], info[i,2]))
        

def plot_stumbledown(f, p, stepSize, nSteps):
    
    """
    Plots the steps taken by the Stumbledown Reducing algorithm and the 
    level curves of the testf function. (Run in console)
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        none
    """
    
    info = stumbledown_reducing(f, p, stepSize, nSteps)
    
    location = info[:,:2]
    x = location[:,0]
    y = location[:,1]
    
    xpts = np.linspace(0, 6, 100)
    ypts = np.linspace(0, 6, 100)
    
    X, Y = np.meshgrid(xpts, ypts)
    Z = testf(X, Y)
    
    plt.plot(x, y, color = 'black', linewidth = 2)
    plt.plot(x[-1], y[-1], color ='black', marker = '.', markersize = 2)
    plt.contourf(X, Y, Z, cmap = 'BuPu')
    plt.colorbar()
    
    plt.title('Contour Plot and Algorithm Steps', fontsize = 16, pad = 10)
    plt.xlabel('x', fontsize = 14, labelpad = 10)
    plt.ylabel('y', fontsize = 14, labelpad = 10)


# GPS Error Exercise
def gps_error(x, y):
    
    """
    Calculates the error for any (x, y) position based on the mismatch 
    between the calculated and actual distances of each satellite.
    
    Parameters:
        x (float): the x coordinate
        
        y (float): the y coordinate
        
    Returns:
        mismatchError (float): the sum of the errors between the calculated and
        actual distances of each of the 5 satellites and the position (x, y)
    """
    
    satellite = np.array([[567, 390.7, 366.9], [73.2, 499.5, 444.9], 
                          [204, 501, 386], [337.3, 609.3, 480.5], 
                          [368.5, 116.3, 57.0]]) #[x,y,d]
    
    calculated1 = np.sqrt((x - satellite[0,0])**2 + (y - satellite[0,1])**2)
    mismatch1 = (calculated1 - satellite[0,2])**2
    
    calculated2 = np.sqrt((x - satellite[1,0])**2 + (y - satellite[1,1])**2)
    mismatch2 = (calculated2 - satellite[1,2])**2
    
    calculated3 = np.sqrt((x - satellite[2,0])**2 + (y - satellite[2,1])**2)
    mismatch3 = (calculated3 - satellite[2,2])**2
    
    calculated4 = np.sqrt((x - satellite[3,0])**2 + (y - satellite[3,1])**2)
    mismatch4 = (calculated4 - satellite[3,2])**2
    
    calculated5 = np.sqrt((x - satellite[4,0])**2 + (y - satellite[4,1])**2)
    mismatch5 = (calculated5 - satellite[4,2])**2
    
    mismatchError = np.sum([mismatch1, mismatch2, mismatch3, mismatch4, mismatch5])
    
    return mismatchError


def print_gps(f, p, stepSize, nSteps):
    
    """
    Plots the steps taken by the Stumbledown Reducing algorithm and prints the 
    final x and y location.
    
    Parameters:
        f (function): the function to be minimized
        
        p (array[float]): a 2 element array containing the initial (x, y) 
        coordinates
        
        stepSize (float): maximum stepsize used to find the next position (x, y)
        
        nSteps (int): number of steps the algorithm will run through
        
    Returns:
        none
    """
    
    info = stumbledown_reducing(f, p, stepSize, nSteps)
    
    location = info[:,:2]
    x = location[:,0]
    y = location[:,1]
    
    print('Final x location:', x[-1])
    print('Final y location:', y[-1])
    
    plt.plot(x, y, color = 'purple', linewidth = 2)
    plt.plot(x[-1], y[-1], color = 'black', marker = '.', markersize = 15)


# Plot the satellite circles and final location
satellite = np.array([[567, 390.7, 366.9], [73.2, 499.5, 444.9], [204, 501, 386], 
                      [337.3, 609.3, 480.5], [368.5, 116.3, 57.0]]) #[x,y,d]
startPoint = np.array([500, 500])

plt.figure(figsize = (10, 7))
ax = plt.gca()
print_gps(gps_error, startPoint, 400, 1000)
for sats in satellite: # plots a circle of radius d around each satellite
    circle = plt.Circle((sats[0], sats[1]), radius = sats[2], fc = 'none', ec = 'turquoise')
    ax.add_patch(circle)

plt.xlim([-400, 1000])
plt.ylim([0, 1200])

plt.title('Satellite Circles and the Final Location', fontsize = 16, pad = 10)
plt.xlabel('x', fontsize = 14, labelpad = 10)
plt.ylabel('y', fontsize = 14, labelpad = 10)
ax.tick_params(axis = 'both', labelsize = 12)