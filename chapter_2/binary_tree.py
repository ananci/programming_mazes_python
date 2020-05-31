#!/usr/bin/env python3

from mazes import grid
import random

class BinaryTree(object):

    def on(self, grid):
        for cell in grid.each_cell():
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)
            if neighbors:
                neighbor = random.choice(neighbors)
                cell.link(neighbor)


binary_maze = grid.Grid(10, 10)
BinaryTree().on(binary_maze)
print(binary_maze)

