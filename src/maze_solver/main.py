from tkinter import Tk, Canvas

from maze import Maze


def main():
    w = Window(600, 600, "The Magical Maze")
    maze = Maze(50, 50, 10, 10, 50, 50, w)
    maze.solve()
    w.run()


class Window:
    def __init__(self, width, height, title):
        self._root = Tk()
        self._root.geometry(f"{width}x{height}")
        self._root.title(title)
        self._root.protocol("WM_DELETE_WINDOW", self.close)

        self._canvas = Canvas(self._root, width=width, height=height)
        self._canvas.pack()
        self._root.bind("<KeyPress>", self.handle_key)

        self._is_running = False

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def run(self):
        self._is_running = True
        while self._is_running:
            self.redraw()

    def close(self):
        self._is_running = False

    def draw_line(self, line, color):
        line.draw(self._canvas, color)

    def handle_key(self, event):
        if event.keysym == "q":
            self.close()


if __name__ == "__main__":
    main()
