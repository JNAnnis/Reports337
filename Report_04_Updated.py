# -*- coding: utf-8 -*-

"""
Report 4: Floating Point Numbers

Storing and using floating point numbers on a computer uses an appoximation
because memory is limited, and relies on the binary system instead of the base
10 system.

To convert to binary scientific notation, 

(-1)^s * (1.mantissa) * 2^(exponent - bias)

for normalized numbers and

(-1)^s * (0.mantissa) * 2^(1 - bias)

for denormalized numbers. The mantissa is the set of digits after the decimal
point, and "s" stands for the sign of the number.

Machine Epsilon: the smallest number that can be added to 1 to give a number 
greater than 1.
"""


import numpy as np
import matplotlib.pyplot as plt


def find_epsilon():
    
    """
    Finds and prints the exponent of the machine epsilon in base 2 and the
    actual value of the machine epsilon in base 10.
    
    Parameters:
        None
    
    Returns: 
        None
    """
    
    n = 1
    x = 2.**(-n)
    
    while 1 + x != 1:
        n += 1
        x = 2.**(-n)
        
    print('The base 2 exponent of the machine epsilon', -(n-1))
    print('The machine epsilon in base 10 is', 2.**(1-n))
    

def find_largest():
    
    """
    Finds and prints the exponent of the largest floating point number and
    the actual value of the largest floating point number, both in base 2.
    
    Parameters:
        None
    
    Returns:
        None
    """
    
    n = 1
    
    while True:
        try:
            x = 2.**n
            n += 1
        except:
            print('The largest exponent is', n - 1)
            print('The largest floating point number is 2^' + str(n - 1))
            break


def find_smallest():

    """
    Finds and prints the exponent of the smallest floating point number and
    the actual value of the smallest floating point number, both in base 2.
    
    Parameters:
        None
        
    Returns:
        None
    """
    
    n = 1
    x = 2.**n
    
    while x != 0:
        n -= 1
        x = 2.**n
    
    print('The smallest exponent is', n + 1)
    print('The smallest floating point number is 2^', n + 1)
    

# Plot a function close to zero and observe the behavior
# F(x) = log(x + 1) / x
plt.figure(figsize = (10, 10))

x = np.linspace(-1e-7, 1e-7, 1001)
y = np.where(x == 0, 1.0, np.log(1 + x)/x)

plt.plot(x, y, color = 'steelblue')

plt.title('F(x) Near Zero', fontsize = 16)
plt.xlabel('x', fontsize = 14, labelpad = 15)
plt.ylabel('y', fontsize = 14, labelpad = 15)
plt.ticklabel_format(axis = 'both', useMathText = True)


# Plot the same function closer to zero
plt.figure(figsize = (10, 10))

x = np.linspace(-1e-15, 1e-15, 1001)
y = np.where(x == 0, 1.0, np.log(1 + x)/x)

plt.plot(x, y, color = 'steelblue')

plt.title('F(x) More Near Zero', fontsize = 16)
plt.xlabel('x', fontsize = 14, labelpad = 15)
plt.ylabel('y', fontsize = 14, labelpad = 15)
plt.ticklabel_format(axis = 'both', useMathText = True)


# Plot the function and the Taylor series approximation
plt.figure(figsize = (10, 10))

x = np.linspace(-1e-7, 1e-7, 1001)
y = np.where(x == 0, 1.0, np.log(1 + x)/x)
z = 1 - ((x/2) + ((x**2)/3) - ((x**3)/4))

plt.plot(x, y, color = 'steelblue', label = 'F(x)')
plt.plot(x, z, color = 'maroon', label = 'Taylor')

plt.title('F(x) and its Taylor Series Approx.', fontsize = 16)
plt.xlabel('x', fontsize = 14, labelpad = 15)
plt.ylabel('y', fontsize = 14, labelpad = 15)
plt.ticklabel_format(axis = 'both', useMathText = True)

plt.legend()