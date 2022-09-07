import random
import time
from tkinter import Tk, BOTH, Canvas


class Window:
   def __init__(self, width, height):
       self.width = width
       self.height = height
       # Root widget using Tk
       self.root_widget = Tk()
       self.root_widget.geometry("900x900")
       self.root_widget.configure(bg="white")  # doesn't work
       self.root_widget.title = "Main Title"
       # Canvas as a data member
       self.canvas = Canvas(self.root_widget)
       self.canvas.pack(fill=BOTH, expand=1)
       # Window running status
       self.winrun = False
       # Close method
       self.root_widget.protocol("WM_DELETE_WINDOW", self.close)


   def draw_line(self, line_class, fill_color):
      line_class.draw(self.canvas, fill_color)


   def redraw(self):
      self.root_widget.update_idletasks()
      self.root_widget.update()


   def wait_for_close(self):
      self.winrun = True
      while self.winrun:
         self.redraw()


   def close(self):
      self.winrun = False


class Point:
   def __init__(self, x, y):
      self.x = x
      self.y = y


class Line:
   def __init__(self, point1, point2):
      self.point1 = point1
      self.point2 = point2


   def draw(self, inp_canvas, color):
      self.canvas = inp_canvas
      self.color = color
      # Canvas operations - create line
      self.canvas.create_line(self.point1.x, self.point1.y,
                              self.point2.x, self.point2.y,
                              fill=self.color, width=4)
      self.canvas.pack()


class Cell:
   def __init__(self, x1, y1, x2, y2, _win=None, has_left_wall=True, has_right_wall=True,
                                                 has_top_wall=True, has_bottom_wall=True):
      self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
      self.win = _win
      self.has_left_wall = has_left_wall
      self.has_right_wall = has_right_wall
      self.has_top_wall = has_top_wall
      self.has_bottom_wall = has_bottom_wall
      self.visited = False


   def draw(self):
      # Finding the top left and bottom right co-ordinates
      # of the rectangle.
      left_x = min(self.x1, self.x2)
      right_x = max(self.x1, self.x2)
      top_y = min(self.y1, self.y2)
      bottom_y = max(self.y1, self.y2)
      # Get the co-ordinates of the four points - anti-clockwise
      px1, py1 = left_x, top_y
      px2, py2 = left_x, bottom_y
      px3, py3 = right_x, bottom_y
      px4, py4 = right_x, top_y

      if self.win:
         # Draw lines using the co-ordinates depending
         # on if there is a wall.
         if self.has_left_wall:
            self.win.draw_line(Line(Point(px1, py1), Point(px2, py2)), "black")
         else:
            self.win.draw_line(Line(Point(px1, py1), Point(px2, py2)), "white")
         if self.has_bottom_wall:
            self.win.draw_line(Line(Point(px2, py2), Point(px3, py3)), "black")
         else:
            self.win.draw_line(Line(Point(px2, py2), Point(px3, py3)), "white")
         if self.has_right_wall:
            self.win.draw_line(Line(Point(px3, py3), Point(px4, py4)), "black")
         else:
            self.win.draw_line(Line(Point(px3, py3), Point(px4, py4)), "white")
         if self.has_top_wall:
            self.win.draw_line(Line(Point(px4, py4), Point(px1, py1)), "black")
         else:
            self.win.draw_line(Line(Point(px4, py4), Point(px1, py1)), "white")


   def draw_move(self, to_cell, undo=False):
      # Drawing a line from center of one cell to the next
      if not undo:
         color = "red"
      else:
         color = "gray"
      # Finding the mid point of the current cell and to_cell
      self_mid_x, self_mid_y = (self.x1+self.x2)/2, (self.y1+self.y2)/2
      other_mid_x, other_mid_y = (to_cell.x1+to_cell.x2)/2, (to_cell.y1+to_cell.y2)/2
      # Drawing a line between the two midpoints
      self.win.draw_line(Line(Point(self_mid_x, self_mid_y), Point(other_mid_x, other_mid_y)), color)


class Maze:
   def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
      self.x1 = x1
      self.y1 = y1
      self.num_rows = num_rows
      self.num_cols = num_cols
      self.cell_size_x = cell_size_x
      self.cell_size_y = cell_size_y
      self.win = win
      # Random seed to test not so random seed
      if seed:
         random.seed(seed)
      else:
         random.seed()
      # Cells matrix list
      self._cells = []
      # Call create cells method and return the list back
      self._cells = self._create_cells()


   def _create_cells(self):
      for i in range(self.num_cols):
         each_col = []
         for j in range(self.num_rows):
            if self.win:
               each_col.append(self._draw_cell(i, j))
            else:
               each_col.append("None")
         self._cells.append(each_col)
      return self._cells


   def _draw_cell(self, i, j,
                  left_wall_bool=True, right_wall_bool=True,
                  top_wall_bool=True, bottom_wall_bool=True):
      # Calculate the co-ordinates of the cell and call _animate
      coordinate_x1 = self.x1 + (i*self.cell_size_x)
      coordinate_y1 = self.y1 + (j*self.cell_size_y)
      coordinate_x2 = self.x1 + ((i+1)*self.cell_size_x)
      coordinate_y2 = self.y1 + ((j+1)*self.cell_size_y)
      ## X and Y position of each cell
      # center_point_x = (coordinate_x1 + coordinate_x2)/2
      # center_point_y = (coordinate_y1 + coordinate_y2)/2
      ##
      # Construct cell and draw it
      cell = Cell(coordinate_x1, coordinate_y1, coordinate_x2, coordinate_y2,
                  _win=self.win, has_left_wall=left_wall_bool, has_right_wall=right_wall_bool,
                                 has_top_wall=top_wall_bool, has_bottom_wall=bottom_wall_bool)
      cell.draw()
      self._animate()
      return cell


   def _animate(self):
      self.win.redraw()
      time.sleep(0.05)


   def _break_entrance_and_exit(self):
      # # Top left cell
      # self._draw_cell(0, 0, top_wall_bool=False)
      # # Bottom right cell
      # self._draw_cell(self.num_cols-1, self.num_rows-1, bottom_wall_bool=False)

      # Directly changing the color of the entrance and exit
      entrance = self._cells[0][0]
      entrance.has_top_wall = False
      entrance.draw()
      exit = self._cells[self.num_cols-1][self.num_rows-1]
      exit.has_bottom_wall = False
      exit.draw()


   def _break_walls_r(self, i, j):
      # Mark current cell as visited
      current_cell = self._cells[i][j]
      current_cell.visited = True
      while True:
         to_visit = []
         # Setting "to direction" in to_visit.append value
         # example: "right" means both the right wall of current cell
         # and the left wall of the next cell will be False
         try:
            next_col_cell = self._cells[i+1][j]
            if not next_col_cell.visited:
               to_visit.append(("right",i+1,j))
         except IndexError:
            # print("There are no cells in the next column i.e to the right")
            pass
         try:
            next_row_cell = self._cells[i][j+1]
            if not next_row_cell.visited:
               to_visit.append(("bottom",i,j+1))
         except IndexError:
            # print("There are no cells in the next row i.e to the bottom")
            pass
         try:
            if i-1 >= 0:
               before_col_cell = self._cells[i-1][j]
               if not before_col_cell.visited:
                  to_visit.append(("left",i-1,j))
            else:
               before_col_cell = self._cells[i][j]
               if not before_col_cell.visited:
                  to_visit.append(("left",i,j))
         except IndexError:
            # print("There are no cells in the previous column i.e to the left")
            pass
         try:
            if j-1 >= 0:
               before_row_cell = self._cells[i][j-1]
               if not before_row_cell.visited:
                  to_visit.append(("top",i,j-1))
            else:
               before_row_cell = self._cells[i][j]
               if not before_row_cell.visited:
                  to_visit.append(("top",i,j))
         except IndexError:
            # print("There are no cells in the previous row i.e to the top")
            pass
         # Draw the current cell and return if to_visit is empty
         if not to_visit:
            current_cell.draw()
            self._animate()
            return
         else:
            rand_move = random.choice(to_visit)
            next_cell = self._cells[rand_move[1]][rand_move[2]]
            if rand_move[0] == "right":
               current_cell.has_right_wall=False
               current_cell.draw()
               # self._animate()
               next_cell.has_left_wall=False
            elif rand_move[0] == "bottom":
               current_cell.has_bottom_wall=False
               current_cell.draw()
               # self._animate()
               next_cell.has_top_wall=False
            elif rand_move[0] == "left":
               current_cell.has_left_wall=False
               current_cell.draw()
               # self._animate()
               next_cell.has_right_wall=False
            elif rand_move[0] == "top":
               current_cell.has_top_wall=False
               current_cell.draw()
               # self._animate()
               next_cell.has_bottom_wall=False
            # Drawing the next cell without the wall
            next_cell.draw()
            self._animate()
            self._break_walls_r(rand_move[1], rand_move[2])


   def _reset_cells_visited(self):
      for col in self._cells:
         for cell in col:
            cell.visited = False
      return


   def solve(self):
      return self._solve_r(0, 0)


   def _solve_r(self, i, j):
      self._animate()
      current_cell = self._cells[i][j]
      current_cell.visited = True
      if (i,j) == (self.num_cols-1, self.num_rows-1):
         return True
      # For all four directions
      dir_right = (i+1, j, "right") if i+1 <= self.num_cols-1 else None
      dir_bottom = (i, j+1, "bottom") if j+1 <= self.num_rows-1 else None
      dir_left = (i-1,j, "left") if i-1 >= 0 else None
      dir_top = (i, j-1, "top") if j-1 >= 0 else None
      all_dirs = [dir_right, dir_bottom, dir_left, dir_top]
      # Randomize the direction the recursive _solve_r will take
      random.shuffle(all_dirs)
      # next_col_cell = self._cells[i+1][j]  # right wall
      # next_row_cell = self._cells[i][j+1]  # bottom wall
      # prev_col_cell = self._cells[i-1][j]  # left wall
      # prev_row_cell = self._cells[i][j-1]  # top wall

      for each_dir in all_dirs:
         # print(f"Each dir is {each_dir}")
         # If the direction exists
         if each_dir:
            next_cell = self._cells[each_dir[0]][each_dir[1]]
            # Initialize all the no_walls to False
            no_right_wall = False
            no_bottom_wall = False
            no_left_wall = False
            no_top_wall = False
            # Check the direction
            each_dir_word = each_dir[2]
            if each_dir_word == "right":
               # Check if there is a wall between current and next cell
               no_right_wall = not current_cell.has_right_wall and not next_cell.has_left_wall
            if each_dir_word == "bottom":
               no_bottom_wall = not current_cell.has_bottom_wall and not next_cell.has_top_wall
            if each_dir_word == "left":
               no_left_wall = not current_cell.has_left_wall and not next_cell.has_right_wall
            if each_dir_word == "top":
               no_top_wall = not current_cell.has_top_wall and not next_cell.has_bottom_wall
            # Next cell visit status
            not_visited = not next_cell.visited
            # Draw move if there is not wall
            if no_right_wall and not_visited:
               current_cell.draw_move(next_cell)
               if self._solve_r(i+1, j):
                  return True
               else:
                  current_cell.draw_move(next_cell, undo=True)
            if no_bottom_wall and not_visited:
               current_cell.draw_move(next_cell)
               if self._solve_r(i, j+1):
                  return True
               else:
                  current_cell.draw_move(next_cell, undo=True)
            if no_left_wall and not_visited:
               current_cell.draw_move(next_cell)
               if self._solve_r(i-1, j):
                  return True
               else:
                  current_cell.draw_move(next_cell, undo=True)
            if no_top_wall and not_visited:
               current_cell.draw_move(next_cell)
               if self._solve_r(i, j-1):
                  return True
               else:
                  current_cell.draw_move(next_cell, undo=True)
      return False


def main():
   win = Window(1500, 1500)
   """
   ## 1
   # Input points
   p1 = Point(10, 15)
   p2 = Point(500, 550)
   # Line between the points
   line1 = Line(p1, p2)
   # Draw line on canvas
   win.draw_line(line1, "blue")
   """
   """
   ## 2
   #
   # cell2 = Cell(150, 100, 200, 150, win, has_left_wall=False, has_right_wall=False)
   # cell3 = Cell(300, 200, 105, 150, win) # trying out wrong order of x,y co-ordinates
   #cell2.draw()
   #cell3.draw()
   """
   """
   ## 3
   # cell1 = Cell(100, 100, 150, 150, win, has_right_wall=False, has_bottom_wall=False)
   # cell2 = Cell(150, 100, 300, 250, win, has_left_wall=False)
   cell1 = Cell(100, 100, 150, 150, win)
   cell2 = Cell(150, 100, 300, 250, win)
   cell1.draw()
   cell2.draw()
   cell1.draw_move(cell2, undo=False)
   """
   """
   ## 4
   # Draw maze and wait for it to close
   ## Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win)
   Maze(100, 100, 10, 10, 50, 50, win)
   win.wait_for_close()
   """
   # init_maze = Maze(100, 100, 30, 30, 20, 20, win=win, seed=5)
   init_maze = Maze(100, 100, 10, 10, 30, 30, win=win) #, seed=5)
   init_maze._break_walls_r(0,0)
   init_maze._break_entrance_and_exit()
   init_maze._reset_cells_visited()
   init_maze.solve()
   win.wait_for_close()

## 5
main()
