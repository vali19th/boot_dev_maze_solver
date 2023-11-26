from maze import Maze


def test_maze_create_cells():
    rows = 10
    cols = 12
    m = Maze(0, 0, rows, cols, 10, 10)

    assert len(m._cells) == rows
    assert len(m._cells[1]) == cols
