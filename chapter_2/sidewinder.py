#!/usr/bin/env python3

from mazes import grid
import random

class Sidewinder(object):

    def on(self, grid):
        for row in grid.each_row():
            run = []

            for cell in row:
                run.append(cell)

                at_eastern_boundary = not bool(cell.east)
                at_northern_boundary = not bool(cell.north)

                should_close_out = at_eastern_boundary or (not at_northern_boundary and random.randint(0, 1) == 0)

                if should_close_out:
                    member = random.choice(run)
                    if member.north:
                        member.link(member.north)
                    run = []
                else:
                    if cell.east:
                        cell.link(cell.east)


sidewinder_maze = grid.Grid(10, 10)
Sidewinder().on(sidewinder_maze)
print(sidewinder_maze)
