import pytest

from maze import Maze


def test_maze_create_cells():
    rows = 10
    cols = 12
    m = Maze(0, 0, rows, cols, 10, 10)

    assert len(m._cells) == rows
    assert len(m._cells[1]) == cols


@pytest.mark.parametrize(
    "r, c, visited, neighbours",
    [
        [0, 0, [], [(1, 0), (0, 1)]],
        [4, 4, [], [(4, 3), (3, 4)]],
        [10, 10, [], []],
        [1, 2, [], [(1, 1), (2, 2), (1, 3), (0, 2)]],
        [1, 2, [(2, 2), (1, 3)], [(1, 1), (0, 2)]],
    ],
)
def test_get_unvisited_neighbours(r, c, visited, neighbours):
    m = Maze(0, 0, 5, 5, 10, 10)
    for r2, c2 in visited:
        m._cells[r2][c2].visited = True

    assert m.get_unvisited_neighbours(r, c) == neighbours


def test_break_walls_r_and_reset_cells_visited():
    rows = 10
    cols = 12
    m = Maze(0, 0, rows, cols, 10, 10)

    for row in m._cells:
        assert not any(c.visited for c in row)

    m._break_walls_r(0, 0)

    for row in m._cells:
        assert all(c.visited for c in row)

    m._reset_cells_visited()

    for row in m._cells:
        assert not any(c.visited for c in row)
