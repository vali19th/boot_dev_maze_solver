import random
from time import sleep

from graphics import Line


class Maze:
    def __init__(
        self,
        x0,
        y0,
        rows,
        cols,
        dx,
        dy,
        win=None,
        seed=None,
    ):
        self._x0 = x0
        self._y0 = y0
        self._rows = rows
        self._cols = cols
        self._dx = dx
        self._dy = dy
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        if self._win:
            self._draw_cells()
            self._break_entrance_and_exit()
            self._break_walls_r(0, 0)

    def solve(self):
        self._reset_cells_visited()
        return self._solve_r(0, 0)

    def _solve_r(self, r, c):
        self._cells[r][c].visited = True
        if (r == len(self._cells) - 1) and (c == len(self._cells[0]) - 1):
            return True

        for r2, c2 in self.get_unvisited_neighbours(r, c):
            if not self._can_move((r, c), (r2, c2)):
                continue

            self._cells[r][c].draw_move(self._cells[r2][c2])
            if self._solve_r(r2, c2):
                return True

            self._cells[r][c].draw_move(self._cells[r2][c2], undo=True)

        return False

    def _can_move(self, cell_1, cell_2):
        r, c = cell_1
        r2, c2 = cell_2
        cell_1 = self._cells[r][c]
        cell_2 = self._cells[r2][c2]
        if r < r2 and not (cell_1.bottom or cell_2.top):
            return True
        elif r > r2 and not (cell_1.top or cell_2.bottom):
            return True
        elif c < c2 and not (cell_1.right or cell_2.left):
            return True
        elif c > c2 and not (cell_1.left or cell_2.right):
            return True
        else:
            return False

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def _break_walls_r(self, r, c):
        current_cell = self._cells[r][c]
        current_cell.visited = True

        while True:
            to_visit = self.get_unvisited_neighbours(r, c)
            if not to_visit:
                current_cell.draw()
                return

            r2, c2 = other = random.choice(to_visit)
            other_cell = self._cells[r2][c2]

            self._break_walls_between(current_cell, other_cell)
            self._break_walls_r(r2, c2)

    def _break_walls_between(self, cell_1, cell_2):
        (x1, y1), (X1, Y1) = cell_1._p1, cell_1._p2
        (x2, y2), (X2, Y2) = cell_2._p1, cell_2._p2
        if x1 == X2:
            cell_1.left = cell_2.right = False
        elif X1 == x2:
            cell_1.right = cell_2.left = False
        elif y1 == Y2:
            cell_1.bottom = cell_2.top = False
        elif Y1 == y2:
            cell_1.top = cell_2.bottom = False

        cell_1.draw()
        cell_2.draw()

    def get_unvisited_neighbours(self, r, c):
        coords = [
            (r, c - 1),
            (r + 1, c),
            (r, c + 1),
            (r - 1, c),
        ]
        return [
            (r, c)
            for r, c in coords
            if 0 <= r < len(self._cells)
            and 0 <= c < len(self._cells[0])
            and not self._cells[r][c].visited
        ]

    def _break_entrance_and_exit(self):
        self._cells[0][0].top = False
        self._cells[-1][-1].bottom = False
        self._cells[0][0].draw()
        self._cells[-1][-1].draw()

    def _draw_cells(self):
        if not self._win:
            return

        for row in self._cells:
            for cell in row:
                cell.draw()

    def _create_cells(self):
        self._cells = []
        for r in range(self._rows):
            row = [Cell(self._win, *self._calc_pts(r, c)) for c in range(self._cols)]
            self._cells.append(row)

    def _calc_pts(self, r, c):
        y = r * self._dy + self._y0
        Y = y + self._dy
        x = c * self._dx + self._x0
        X = x + self._dx
        return (x, y), (X, Y)


class Cell:
    def __init__(self, win, p1, p2, top=True, right=True, bottom=True, left=True):
        self._win = win

        (x1, y1), (x2, y2) = p1, p2
        self._p1 = min(x1, x2), max(y1, y2)
        self._p2 = max(x1, x2), min(y1, y2)

        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

        self.visited = False

    def __repr__(self):
        return f"Cell({self._win}, {self._p1}, {self._p2}, {self.top}, {self.right}, {self.bottom}, {self.left})"

    def _calc_center(self):
        x = (self._p1[0] + self._p2[0]) / 2
        y = (self._p1[1] + self._p2[1]) / 2
        return x, y

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        x, y = self._calc_center()
        x2, y2 = to_cell._calc_center()
        line = Line((x, y), (x2, y2))
        self._win.draw_line(line, color)

        self._animate()

    def draw(self):
        (x, y), (X, Y) = self._p1, self._p2
        walls = [
            (Line((x, Y), (X, Y)), self.top),
            (Line((X, y), (X, Y)), self.right),
            (Line((x, y), (X, y)), self.bottom),
            (Line((x, y), (x, Y)), self.left),
        ]

        if not self._win:
            return

        color = {
            False: self._win._root.cget("bg"),
            True: "black",
        }

        for wall, exists in walls:
            self._win.draw_line(wall, color[exists])

        self._animate()

    def _animate(self):
        if self._win:
            self._win.redraw()
            sleep(0.001)
