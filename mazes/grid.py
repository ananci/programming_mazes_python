#!/usr/bin/env python3

import random

class Cell(object):

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self._links = {}
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def link(self, cell, bidi=True):
        self._links[cell] = True
        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True):
        del self._links[cell]
        if bidi:
            cell.unlink(self, False)

    def links(self):
        return list(self._links.keys())

    def linked(self, cell):
        return self._links.get(cell, False)

    def neighbors(self):
        ls = []
        ls.append(self.north)
        ls.append(self.east)
        ls.append(self.south)
        ls.append(self.west)
        return ls


class Grid(object):

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid, self._flat_grid = self._prepare_grid()
        self._configure_cells()

    def _prepare_grid(self):
        grid = []
        flat_grid = []
        for row in range(self.rows):
            temp_ls = []
            grid.append(temp_ls)
            for col in range(self.columns):
                cell = Cell(row=row, column=col)
                temp_ls.append(cell)
                flat_grid.append(cell)
        return grid, flat_grid

    def _configure_cells(self):
        for cell in self._flat_grid:
            row, col = cell.row, cell.column
            cell.north = self.access(row - 1, col)
            cell.south = self.access(row + 1, col)
            cell.west = self.access(row, col - 1)
            cell.east = self.access(row, col + 1)

    def access(self, row, column):
        if (row >= 0 and row < self.rows and column >= 0 and column < self.columns):
            return self.grid[row][column]
        return None

    def random_cell(self):
        return random.choice(self.flat_grid)

    def size(self):
        return len(self.flat_grid)

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.grid:
            for col in row:
                for cell in col:
                    yield cell

