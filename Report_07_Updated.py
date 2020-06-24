# -*- coding: utf-8 -*-

"""
Report 7: bouncing Ping Pong Ball

After a ping pong ball has been dropped from some initial height onto a hard, 
solid surface, it bounces back up. However, it does not bounce back up to the 
initial height. Because of this, the collision between the ball and the surface 
can be characterized as an inelastic collision.

The goal is to test whether or not the real behavior of the ping pong
ball fits the model

t(i+1) = 2v(i+1)/g = r2v(i)/g = rt(i)

where 

t(i+1) is the time of the ith + 1 bounce of the ball
v(i+1) is the velocity of the ith + 1 bounce of the ball
t(i) is the time of the ith bounce of the ball
v(i) is the velocity of the ith bounce of the ball
g is the gravitational constant
r is the fixed amount that the time between consecutive bounces is reduced by

Note: this report requires a .wav file containing the audio of a ping pong ball
bouncing on a hard surface
"""


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.io import wavfile


# Import the ping pong sound data
rate, data = wavfile.read('pingpong.wav') # rate is the sampling rate: 44100

sound = data[:315000,0]
npts = len(sound)
time = np.arange(npts)/rate # convert to time points (seconds)


# Plot the sound amplitude vs time
plt.figure(figsize = (7, 5))
plt.plot(time, sound, color = 'darkgreen')

plt.title('Sound Amplitude vs. Time', fontsize = 16)
plt.xlabel('Time (s)', fontsize = 14)
plt.ylabel('Amplitude', fontsize = 14)

ax1 = plt.gca()
ax1.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


# Find, extract, and indicate the times of each bounce
t0 = np.argmax(sound) # index of max value

wait = 7000 # set an arbitrary wait time, half the distance to t1
tmax = 305000
bounceTimes = [t0]

while t0 < tmax:
    # define an arbitrary window to slice over
    start = t0 + wait
    end = t0 + wait*3
    
    relative = np.argmax(sound[start:end])
    t1 = relative + start # get the actual index of bounce
    bounceTimes.append(t1)
    
    wait = int((t1-t0)/2)
    t0 = t1

# Plot the bounce times over the original sound data
plt.figure(figsize = (7, 5))
plt.plot(time, sound, color = 'darkblue')

for i in time[bounceTimes]: # bounce times as vertical lines
    plt.axvline(i, color = 'greenyellow')

plt.title('Plotting Bounce Times', fontsize = 16)
plt.xlabel('Time (s)', fontsize = 14)
plt.ylabel('Amplitude', fontsize = 14)

ax2 = plt.gca()
ax2.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


# Calculate the least squares regression line to find the value of r
bounceTimes = np.array(bounceTimes, dtype = int)
interval = bounceTimes[1:] - bounceTimes[:-1] # 72 intervals
nBounces = np.arange(len(interval)) # number of bounces
logInterval = np.log(interval)

# Compute the variables in the regression equation
xbar = np.mean(nBounces)
ybar = np.mean(logInterval)
x2bar = np.mean(nBounces**2)
xybar = np.mean(nBounces*logInterval)

a = np.array([[1, xbar], [xbar, x2bar]])
b = np.array([ybar, xybar])
w0, w1 = np.linalg.solve(a, b)

r = np.exp(w1)
ti = (r**nBounces)*np.exp(w0) # time of ith bounce

# Plot the regression with the original data
plt.figure(figsize = (7, 5))
plt.semilogy(nBounces, interval, color = 'blue', label = 'Original Data')
plt.semilogy(nBounces, ti, color = 'deeppink', label = 'Linear Regression')

plt.title('Original Data and Linear Regression', fontsize = 16)
plt.xlabel('Number of Bounces', fontsize = 14)
plt.ylabel('log($t_i$), log(interval)', fontsize = 14)

plt.legend()

print('The fixed fraction of energy lost on each bounce is: {:.2f}'.format(r))


# Plot the amplitude vs time for one bounce
singleBounce = data[39400:41500,0]
timePts = np.arange(len(singleBounce))/rate

plt.figure(figsize = (14, 7))
plt.plot(timePts, singleBounce, color = 'purple')

plt.title('Sound Amplitude vs. Time for One Bounce', fontsize = 16)
plt.xlabel('Time (s)', fontsize = 14)
plt.ylabel('Amplitude', fontsize = 14)

ax3 = plt.gca()
ax3.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# Find the dominant frequency of this bounce
plt.figure()
bouncePSD = plt.psd(singleBounce, Fs = 44100) # power spectral density

maxAmp = np.argmax(bouncePSD[0])
maxFrequency = bouncePSD[1][maxAmp]

print('The dominant ringing frequency is: {:,.0f}'.format(maxFrequency))
