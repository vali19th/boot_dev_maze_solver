class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"

    def __str__(self):
        return f"({self.p1}, {self.p2})"

    def draw(self, canvas, color):
        canvas.create_line(*self.p1, *self.p2, fill=color, width=2)
        canvas.pack()
