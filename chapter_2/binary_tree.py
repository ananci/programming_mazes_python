#!/usr/bin/env python

from .grid import Grid
import random

class BinaryTree(object):

    def on(self, grid):
        for cell in grid.each_cell:
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)

            neighbor = random.Choice(neighbors)
            cell.link(neighbor)


binary_maze = Grid.grid(4, 4)
BinaryTree().on(binary_maze)

