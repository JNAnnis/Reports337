# -*- coding: utf-8 -*-

"""
Report 2: Prime Spiral

A prime spiral is a plot in which only the positive integers are arranged
into a spiral, with the prime numbers being highlighted in some way.
"""


import matplotlib.pyplot as plt


def is_prime(P):
    
    """
    Method to check if a number is prime or composite.
    
    Parameters:
        P (int): number to be checked, must be greater than 1
    
    Returns: 
        bool: True if prime, False if composite
    """
    
    for i in range(2, P):
        j = P % i
        
        if j == 0:
            return False
        
    return True
    
    
plt.figure(figsize = (20, 20))
plt.xlim(-16, 17)
plt.ylim(-16, 17)
plt.xticks([])
plt.yticks([])

# Initialize the (x, y) coordinate
# Plot 1 here because it is neither prime nor composite 
x, y = 0, 0
plt.text(x, y, 1, color = 'lightgrey', fontsize = 10)

# Create the rest of the prime spiral (30 x 30 grid)
step = 1
num2Plot = 1
lastMove = 'Down'
nextMove = ''

for i in range(1, 32):
    step += 1
    
    # Set the direction of the numbers to be plotted, two directions per step
    for j in range(2):
        if lastMove == 'Down':
            nextMove = 'Right'
        if lastMove == 'Right':
            nextMove = 'Up'
        if lastMove == 'Up':
            nextMove = 'Left'
        if lastMove == 'Left':
            nextMove = 'Down'
        
        lastMove = nextMove
        
        # Plot a number at the correct coordinate and determine if it's prime
        for k in range(1, step):
            num2Plot += 1
            
            if nextMove == 'Right':
                x += 1
            if nextMove == 'Up':
                y +=1
            if nextMove == 'Left':
                x -= 1
            if nextMove == 'Down':
                y -= 1
            
            if is_prime(num2Plot):
                plt.text(x, y, num2Plot, color = 'indigo', fontsize = 12,
                         fontweight = 'bold')
            else:
                plt.text(x, y, num2Plot, color = 'lightgrey', fontsize = 10)
                