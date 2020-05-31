#!/usr/bin/env python3

import random
from cairosvg import svg2png

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

    def __str__(self):
        print('{}:{}:{}:{}'.format(self.north, self.east, self.south, self.west))


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
            for cell in row:
                    yield cell

    def __str__(self):
        output = "+" + "---+"*self.columns + "\n"
        for row in self.each_row():
            top = "|"
            bottom = "+"
            for cell in row:
                body = '   '
                east_boundary = ' ' if cell.linked(cell.east) else '|'
                top += body
                top += east_boundary

                south_boundary = '   ' if cell.linked(cell.south) else '---'
                corner = '+'
                bottom += south_boundary
                bottom += corner
            output += top
            output += '\n'
            output += bottom
            output += '\n'
        return output
    
    def write_png(self, filename):

        aspect_ratio = self.rows / self.columns
        # Pad the maze all around
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)

        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.columns, width / self.rows

        def write_wall(x1, y1, x2, y2):
            """Write a single wall to the SVG image file handle f."""

            return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2)

        # Write the SVG image file for maze
        svg_data = ''
        # SVG preamble and styles.
        svg_data += '<?xml version="1.0" encoding="utf-8"?>'
        svg_data += '<svg xmlns="http://www.w3.org/2000/svg"'
        svg_data += '    xmlns:xlink="http://www.w3.org/1999/xlink"'
        svg_data += '    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'.format(width+2*padding, height+2*padding, -padding, -padding, width+2*padding, height+2*padding)
        svg_data += '<defs>\n<style type="text/css"><![CDATA['
        svg_data += 'line {'
        svg_data += '    stroke: #000000;\n    stroke-linecap: square;'
        svg_data += '    stroke-width: 5;\n}'
        svg_data += ']]></style>\n</defs>'
        # Draw the "South" and "East" walls of each cell, if present (these
        # are the "North" and "West" walls of a neighbouring cell in
        # general, of course).
        for row in self.each_row():
            for cell in row:
                x, y = cell.row, cell.column
                if bool(cell.south):
                    x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
                    svg_data += write_wall(x1, y1, x2, y2)
                if bool(cell.east):
                    x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
                    svg_data += write_wall(x1, y1, x2, y2)
        # Draw the North and West maze border, which won't have been drawn
        # by the procedure above. 
        svg_data += '<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width)
        svg_data += '<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height)
        svg_data += '</svg>'

        svg2png(bytestring=svg_data,write_to=filename)

