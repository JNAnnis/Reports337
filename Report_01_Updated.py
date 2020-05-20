# -*- coding: utf-8 -*-

"""
Report 1: Primitive Pythagorean Triples

A pythagorean triple consists of a set of positive integers, (a, b, c)
that satisfies the equation a^2 + b^ = c^2.
"""


import matplotlib.pyplot as plt
import math


def mygcd(a, b):
    
    """
    Method to determine the greatest common denominator of two numbers.
    
    Parameters:
        a (int): first number, must be greater than 0
        b (int): second number, must be greater than 0
        
    
    Returns:
        a (int): greatest common denominator of parameters a and b
    """
    
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    
    return a


def is_square(a, b):
    
    """
    Method to determine whether two numbers make a perfect square.
    
    Parameters:
        a (int): first number, must be greater than 0
        b (int): second number, must be greater than 0
        
    Returns: 
        bool: True if perfect square, False if not
    """
    
    c = a**2 + b**2
    x = math.sqrt(c)
    y = math.ceil(x)
    
    return x == y


def ppt_generate(w, x, y, z, title):
    
    """
    Generates a plot of points, (a, b), that make pythagorean triples, 
    with duplicates removed via the condition a < b.
    
    Parameters: 
        w (int): start value for the range of 'a' values to test, must be 
        greater than 0
    
        x (int): end value for the range of 'a' values to test, must be
        greater than 0
    
        y (int): start value for the range of 'b' values to test, must be 
        greater than 0
    
        z (int): end value for the range of 'b' values to test, must be 
        greater than 0
    
        title (str): title for the graph
    
    Returns: 
        None
    """
    
    plt.figure(figsize = (10, 10))
    plt.title(title, fontweight = 'bold', fontsize = 18, pad = 10)
    plt.xlabel('a', fontweight = 'bold', fontsize = 14, labelpad = 10)
    plt.ylabel('b', fontweight = 'bold', fontsize = 14, labelpad = 10)
    
    for a in range(w, x):
        for b in range(y, z):
            if mygcd(a, b) == 1 and is_square(a, b) == True and a < b:
                plt.plot(a, b, 'b.', markersize = 5)


def ppt_print(e, f, g, h):
    
    """
    Creates a table of pythagorean triples (a, b, c) that exist in a specified
    range of 'a' and 'b' values, with duplicates removed via the condition
    a < b.
    
    Parameters: 
        e (int): start value for the range of 'a' values to test, must be 
        greater than 0
    
        f (int): end value for the range of 'a' values to test, must be
        greater than 0
    
        g (int): start value for the range of 'b' values to test, must be 
        greater than 0
    
        h (int): end value for the range of 'b' values to test, must be 
        greater than 0
    
    Returns: 
        None
    """
    
    print("{}\t{}\t{}".format('a', 'b', 'c'))
    print('___________')
    
    for a in range(e, f):
        for b in range(g, h):
            if mygcd(a, b) == 1 and is_square(a, b) == True and a < b:
                cVal = math.sqrt(a**2 + b**2)
                c = int(cVal)
                
                print("{}\t{}\t{}".format(a, b, c))