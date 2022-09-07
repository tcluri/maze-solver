import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_create_cells(self):
        print("Test to see number of rows and columns")
        maze_test = Maze(1, 1, 10, 10, 2, 2)._create_cells()
        print(len(maze_test))
        self.assertEqual(10, len(maze_test))
        self.assertEqual(10, len(maze_test[0]))

    def test_break_entrance_and_exit(self):
        maze_test = Maze(1, 1, 10, 10, 2, 2)._break_entrance_and_exit()
        maze_test._break_entrance_and_exit()
        self.assertEqual(False, maze_test._cells[0][0].has_top_wall)
        self.assertEqual(False, maze_test._cells[maze_test.num_cols-1][maze_test.num_rows-1].has_bottom_wall)

if __name__ == "__main__":
    unittest.main()
