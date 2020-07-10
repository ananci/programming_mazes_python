#!/usr/bin/env python3

import random
from cairosvg import svg2png

def write_svg_wall(x1, y1, x2, y2):
  """Write a single wall to the SVG image file handle f."""

  return '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'.format(
    x1=x1, y1=y1, x2=x2, y2=y2)

class _Cell(object):

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

  def to_svg_list(self, scx, scy):
    """Generate a list of SVG strings creating lines.

    Args:
      scx: (INT) Scaling factor for x values
      scy: (INT) Scaling factor for y values

    Returns:
        List of strings
    """
    svg_list = []
    x, y = self.column, self.row
    if not self.linked(self.south):
      x1, y1, x2, y2 = x*scx, (y+1)*scy, (x+1)*scx, (y+1)*scy
      svg_list.append(write_svg_wall(x1, y1, x2, y2))
    if not self.linked(self.east):
      x1, y1, x2, y2 = (x+1)*scx, y*scy, (x+1)*scx, (y+1)*scy
      svg_list.append(write_svg_wall(x1, y1, x2, y2))
    if not self.linked(self.north):
      x1, y1, x2, y2 = x*scx, y*scy, (x+1)*scx, y*scy
      svg_list.append(write_svg_wall(x1, y1, x2, y2))
    if not self.linked(self.west):
      x1, y1, x2, y2 = x*scx, y*scy, x*scx, (y+1)*scy
      svg_list.append(write_svg_wall(x1, y1, x2, y2))
    return svg_list

class Grid(object):

  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = self._prepare_grid()
    self._configure_cells()

  def _flat_grid(self):
      for row in self.grid:
          for cell in row:
              yield cell

  def _prepare_grid(self):
    grid = []
    for row in range(self.rows):
      temp_ls = []
      grid.append(temp_ls)
      for col in range(self.columns):
        cell = _Cell(row=row, column=col)
        temp_ls.append(cell)
    return grid

  def _configure_cells(self):
    for cell in self._flat_grid():
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
    return random.choice(self.flat_grid())

  def size(self):
    return len(self.flat_grid())

  def each_row(self):
    for row in self.grid:
      yield row

  def each_cell(self):
    for cell in self._flat_grid():
        yield cell

  def __str__(self):
    """Generate an ASCII representation of the maze."""
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
      """Write the maze to a PNG file."""
      svg2png(bytestring=self._generate_svg_data(), write_to=filename)

  def write_svg(self, filename):
    """Write the maze to a SVG file."""
    with open(filename, 'w') as f:
      f.write(self._generate_svg_data())

  def _generate_svg_data(self):
    """Transform the maze into it's SVG representation."""
    aspect_ratio = self.rows / self.columns
    # Pad the maze all around
    padding = 0
    # Height and width of the maze image (excluding padding), in pixels
    height = 500
    width = int(height * aspect_ratio)

    # Scaling factors mapping maze coordinates to image coordinates
    scy, scx = height / self.columns, width / self.rows

    # Write the SVG image file for maze
    svg_data = ''
    # SVG preamble and styles.
    svg_data += '<?xml version="1.0" encoding="utf-8"?>'
    svg_data += '<svg xmlns="http://www.w3.org/2000/svg"'
    svg_data += '  xmlns:xlink="http://www.w3.org/1999/xlink"'
    svg_data += (
      '  width="{:d}" height="{:d}" viewBox="{} {} {} {}">').format(
      width+2*padding,
      height+2*padding,
      -padding,
      -padding,
      width+2*padding,
      height+2*padding)
    svg_data += '<defs>\n<style type="text/css"><![CDATA['
    svg_data += 'line {'
    svg_data += '  stroke: #000000;\n  stroke-linecap: square;'
    svg_data += '  stroke-width: 5;\n}'
    svg_data += ']]></style>\n</defs>'
    svg_data += '<rect width="100%" height="100%" fill="#878787"/>'
    # Generate the SVG strings representing lines for each cell.
    # Using a set here as this will prevent duplicate lines.
    svg_set = {wall for cell in self.each_cell()
                  for wall in cell.to_svg_list(scx=scx, scy=scy)}
    svg_data += "\n".join(svg_set)
    svg_data += '</svg>'
    return svg_data
