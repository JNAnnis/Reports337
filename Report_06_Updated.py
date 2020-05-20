# -*- coding: utf-8 -*-

"""
Report 6: Magnetic Pendulum

A magnetic pendulum consists of a magent suspended from a pivot located
at the center, and three other magnets are fixed at different (x, y)
positions.

There are 3 main forces that act on the pendulum system:
    1) Gravity, represented by G
    2) Frictional forces at the pivot and air resistance, represented by R
    3) Forces due to magnetic dipoles
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


def dP_dt(P, G, R, d):
    
    """
    Calculate the values in the governing differential equation for the 
    pendulum system.
    
    Parameters:
        P (array[float]): the inital state of the system. An array of x and y 
        positions and the x and y velocities. Order: x positon, y postion, x 
        velocity, y velocity
        
        G (float): the force due to gravity
        
        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
        
    Returns:
        array (float): an array containing the x and y velocities and the sum
        of all the forces in the x and y directions. Order: x positon, y postion, 
        x velocity, y velocity
    """
    
    x, y, vx, vy = P
    
    xLoc = [1, -0.5, -0.5] # x location of the magnets
    yLoc = [0, np.sqrt(3)/2, -np.sqrt(3)/2] # y location of the magnets
    
    ax = -G*x - R*vx
    ay = -G*y - R*vy
    
    for i in range(3):
        r = np.sqrt((x - xLoc[i])**2 + (y - yLoc[i])**2 + d**2)
        ax += ((x - xLoc[i])/r**5) * (1 - ((5*d**2)/r**2))
        ay += ((y - yLoc[i])/r**5) * (1 - ((5*d**2)/r**2))
        
    return np.array([vx, vy, ax, ay])


def calculate_path(tMax, h, P, G, R, d):
    
    """
    Applies the improved Euler method to find the path that the pendulum takes
    based on the initial state.
    
    Parameters:
        tMax (int): the maximum amount of time the simulation will run,0
        in seconds
    
        h (float): the step size
        
        P (array[float]): the inital state of the system. An array of x and y 
        positions and the x and y velocities. Order: x positon, y postion, x 
        velocity, y velocity
        
        G (float): the force due to gravity

        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
    
    Returns:
        path (array[float]): an array of arrays containing all the calculated 
        x and y velocities and the sum of all the forces in the x and y 
        directions. Order: x positon, y postion, sum x velocity, sum y velocity
    """
    
    steps = int(tMax/h)
    path = np.empty((steps, 4))
    path[0] = P
    
    for i in range(1, steps):
        f1 = h*dP_dt(P, G, R, d)
        f2 = h*dP_dt(P + f1, G, R, d)
        P += (f1 + f2)/2
        path[i] = P
        
    return path


def plot_path(tMax, h, P, G, R, d):
    
    """
    Plots the pendulum path created by the calculate_path function.

    Parameters:
        tMax (int): the maximum amount of time the simulation will run, 
        in seconds
    
        h (float): the step size
        
        P (array[float]): the inital state of the system. An array of x and y 
        positions and the x and y velocities. Order: x positon, y postion, x 
        velocity, y velocity
        
        G (float): the force due to gravity

        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
    
    Returns:
        None
    """
    
    # plot the 3 stationary magnets
    plt.plot(1, 0, 'ro')
    plt.plot(-0.5, np.sqrt(3)/2, 'go')
    plt.plot(-0.5, -np.sqrt(3)/2, 'bo')
    
    # plot the path
    path = calculate_path(tMax, h, P, G, R, d)
    plt.plot(path[:,0], path[:,1], color = 'k')


def pendulum_animate(tMax, h, P, G, R, d):
    
    """
    Animates the pendulum path created by the calculate_path function.
    
    Parameters:
        tMax (int): the maximum amount of time the simulation will run, 
        in seconds
    
        h (float): the step size
        
        P (array[float]): the inital state of the system. An array of x and y 
        positions and the x and y velocities. Order: x positon, y postion, x 
        velocity, y velocity
        
        G (float): the force due to gravity

        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
    
    Returns:
        function animation
    """
    
    path = calculate_path(tMax, h, P, G, R, d)
    
    frames = int(tMax/h)
    fig, ax = plt.subplots(figsize = (8, 8))
    ax.set_aspect('equal')
    
    point, = plt.plot([], [], 'ko') # assigns it to the first element in the list, not the whole list
    line, = plt.plot([], [], 'k')
    
    plt.plot(1, 0, 'ro')
    plt.plot(-0.5, np.sqrt(3)/2, 'go')
    plt.plot(-0.5, -np.sqrt(3)/2, 'bo')
    
    width = 0.25 + np.amax(np.abs(path[:,:2])) # finds the largest x or y value and adds 0.25
    plt.xlim(-width, width)
    plt.ylim(-width, width)
    
    def animate(frame, point, line, path):
        
        """
        Gets the updated frame for every frame
        """
        
        x, y = path[frame,:2]
        point.set_data(x, y)
        line.set_data(path[:frame,0], path[:frame,1])
        
        return point, line,
    
    return animation.FuncAnimation(fig, animate, frames = frames,
                    fargs = (point, line, path), interval = 0, repeat = True)


def calculate_final_position(tMax, h, P, G, R, d):
    
    """
    Finds the final position of the pendulum based on its inital state.
    
    Parameters:
        tMax (int): the maximum amount of time the simulation will run, 
        in seconds
    
        h (float): the step size
        
        P (array[float]): the inital state of the system. An array of x and y 
        positions and the x and y velocities.
        
        G (float): the force due to gravity

        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
    
    Returns:
        P (array[float]): final state of the pendulum. Order: x positon, y postion, 
        x velocity, y velocity
    """
    
    steps = int(tMax/h)
    
    for i in range(1, steps):
        f1 = h*dP_dt(P, G, R, d)
        f2 = h*dP_dt(P + f1, G, R, d)
        P += (f1 + f2)/2
    
    return P


def color_grid(tMax, nPts, h, G, R, d):
    
    """
    Used to visually show what magnet the pendulum will end up over if it
    starts in a specific location.
    
    Parameters:
        tMax (int): the maximum amount of time the simulation will run, 
        in seconds
        
        nPts (int): number of x and y points
    
        h (float): the step size
        
        G (float): the force due to gravity

        R (float): the frictional forces
        
        d (float): the distance in the z direction (vertical distance)
    
    Returns:
        None
    """
    
    width = 5
    xPts = np.linspace(-width, width, nPts)
    yPts = np.linspace(-width, width, nPts)
    X, Y = np.meshgrid(xPts, yPts)
    VX, VY = np.zeros((2, nPts, nPts))
    P0 = np.array([X, Y, VX, VY])
    
    P = calculate_final_position(tMax, h, P0, G, R, d)
    
    magnets = np.array([[1, 0], [-0.5, np.sqrt(3)/2], [-0.5, -np.sqrt(3)/2]])
    magnetColors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype = float)
    
    X, Y = P[:2]
    xMags = magnets[:,0]
    yMags = magnets[:,1]
    nMags = len(magnets)
    
    xDiffs = X - xMags.reshape(nMags, 1, 1)
    yDiffs = Y - yMags.reshape(nMags, 1, 1)
    distSquared = xDiffs**2 + yDiffs**2
    closest = np.argmin(distSquared, axis = 0) # index of min value
    
    plt.figure(figsize = (8, 8))
    img = magnetColors[closest]
    plt.imshow(img, interpolation = 'None')
    plt.xticks([])
    plt.yticks([])
    

# Pendulum Plots
# Initial State 1
# tmax = 100, h = 0.01, G = 1, R = 0.5, d = 1
# start at (1,1)
plt.figure(figsize = (6, 6))
plt.gca().set_aspect('equal')
P0 = np.array([1., 1., 0.5, 0.5])
plot_path(100, 0.01, P0, 1., 0.5, 1.)
plt.title('Initial State 1')

# Initial State 2
# tmax = 100, h = 0.01, G = 1, R = 0.5, d = 1
# start at origin with small velocities
plt.figure(figsize = (6, 6))
plt.gca().set_aspect('equal')
P0 = np.array([0, 0, 0.1, 0.1])
plot_path(100, 0.01, P0, 1., 0.5, 1.)
plt.title('Initial State 2')

# Initial State 3
# tmax = 100, h = 0.01, G = 2, R = 0.5, d = 1
# start at origin with no x velocity
plt.figure(figsize = (6, 6))
plt.gca().set_aspect('equal')
P0 = np.array([0, 0, 0, 2.])
plot_path(100, 0.01, P0, 2, 0.5, 1.)
plt.title('Initial State 3')

# Initial State 4
# tmax = 100, h = 0.01, G = 1.5, R = 1, d = 1
# start at (2,2) and large velocities
plt.figure(figsize = (6, 6))
plt.gca().set_aspect('equal')
P0 = np.array([0, 0, 5., 5.])
plot_path(100, 0.01, P0, 1.5, 1., 1.)
plt.title('Initial State 4')


# Color Grid 1
color_grid(100, 100, 0.01, 1, 0.5, 1)

# Color Grid 2
color_grid(50, 25, 0.01, 1, 0.1, 1)

# Color Grid 3
color_grid(50, 25, 0.01, 1, 0.65, 1)

# Color Grid 4
color_grid(50, 25, 0.01, 1, 10, 1)


# Animate the Pendulum
"""
NOTE: To run the animation, you must enter %matplotlib qt5 into the IPython console
before running. Then enter the following two lines into the console. Or, comment
out all other pendulum plots in the file, uncomment the two lines, then run the file.
"""
# P0 = np.array([0.5, 0.5, 3., 3.])
# pendulum_animate(100, 0.01, P0, 1., 0.5, 1.)