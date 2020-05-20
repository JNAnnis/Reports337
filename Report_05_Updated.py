# -*- coding: utf-8 -*-

"""
Report 5: Cellular Automata

A cellular automaton is a self-contained universe where its space is divided
into a grid of cells, and has its own "laws of physics". 

Each cell in the grid has its own state and a set of neighbors.

Time in this universe is a discrete set of steps. At each step of time, a
transition rule updates the state of every cell based on the current state of
the cell and its neighbors.
"""


import numpy as np
import matplotlib.pyplot as plt


def cell_auto():
    
    """
    Method to create a 2 x 2 subplot containing 4 plots with diffent cellular 
    automaton. Cellular automata have the following characteristics:
        - A one dimensional grid with each cell having just two neighbors, one
        on each side.
        - Four possible cell states: 1, 2, 3, 4, that are represented by a 
        different color.
        - Periodic edge conditions: the rightmost and leftmost cells are
        neighbors.
        - The transition rule is that the state of each cell is updated based
        on the sum of the current cell state and those of its neighbors.
    
    All cellular automata change everytime the function is run.
    
    Parameters:
        None
    
    Returns:
        None
    """
    
    
    nGen = 25 # number of generations to apply transition rule to
    nCells = 25 # number of cells
    
    colors = np.array([[1, 0, 0], [0, 1, 1], [0.5, 0, 1], [1, 1, 0]], 
                      dtype = float) # red, cyan, purple, yellow
    
    plt.figure(figsize = (10, 10))
    
    nRow = 2
    nCol = 2
    
    for j in range(1, nRow*nCol + 1):
        cellState = np.empty((nGen, nCells), dtype = int)
        cellState[0] = np.random.randint(4, size = nCells)
        rule = np.random.randint(4, size = 10) # transition rule
        
        for i in range(1, nGen):
            sumCells = (cellState[i-1] + np.roll(cellState[i-1], -1) 
                        + np.roll(cellState[i-1], 1))
            
            cellState[i] = rule[sumCells]
        
        
        cellColor = colors[cellState]
        
        plt.subplot(nRow, nCol, j)
        plt.subplots_adjust(wspace = 0.5)
        plt.imshow(cellColor, interpolation = 'None')
        
        plt.title(str(j), fontsize = 16)
        plt.xlabel(str(rule), fontsize = 16)
        plt.xticks([])
        plt.yticks([])