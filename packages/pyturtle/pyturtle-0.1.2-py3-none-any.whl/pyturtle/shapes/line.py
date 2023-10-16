import turtle
import numpy.typing as npt
import numpy as np
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D


class Line(Shape):
    def __init__(self, x1, y1, x2, y2, **kwargs):
        super().__init__(**kwargs)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_slope(self):
        """
        returns slope of a line
        """
        return (self.y2 - self.y1) / (self.x2 - self.x1)

    def get_intercept(self):
        """
        returns the intercept of the line
        y = mx+b
        """
        return self.y1 - self.get_slope() * self.x1

    def get_points_on_line(self):
        """ """
        return np.linspace([self.x1, self.y1], [self.x2, self.y2], self.steps)

    def draw(self):
        self.turtle.penup()
        points = self.get_points_on_line()
        self.turtle.goto(points[0][0], points[0][1])
        self.coordinates[0] = Point2D(points[0][0], points[0][1])
        self.turtle.pendown()
        for num, point in enumerate(points[1:]):
            x, y = point[0], point[1]
            self.coordinates[num + 1] = Point2D(x, y)
            self.turtle.goto(x, y)

    def change_end_points(self, x2, y2):
        """
        change the end point of the line while
        keeping start point the same.
        """
        self.x2 = x2
        self.y2 = y2

    def swap_start_end(self):
        """
        changes the start of the line to the previous end of the line.
        """
        self.x1 = self.x2
        self.y1 = self.y2

    def translate_x(self, x):
        self.x1 += x
        self.x2 += x
        # update coordinates
        points = self.get_points_on_line()
        for step, point in enumerate(points):
            self.coordinates[step] = Point2D(point[0], point[1])

    def translate_y(self, y):
        self.y1 += y
        self.y2 += y
        # update coordinates
        points = self.get_points_on_line()
        for step, point in enumerate(points):
            self.coordinates[step] = Point2D(point[0], point[1])

    def translate_xy(self, x, y):
        self.x1 += x
        self.y1 += y
        self.x2 += x
        self.y2 += y
        points = self.get_points_on_line()
        for step, point in enumerate(points):
            self.coordinates[step] = Point2D(point[0], point[1])


class HorizontalLine(Line):
    """
    Same as Line, but
    y1 = y2
    """

    def __init__(self, turtle, x1, x2, y):
        super().__init__(turtle, x1, y, x2, y)


class VerticalLine(Line):
    """
    Same as Line, but
    x1 = x2
    """

    def __init__(self, turtle, y1, y2, x):
        super().__init__(turtle, x, y1, x, y2)


class HorizontalLineStack:
    """
    going to try and implement this object using concepts from
    a linked list
    """

    def __init__(self, turtle):
        self.lines = []
        self.turtle = turtle

    def is_empty(self):
        return self.lines == []

    def add(self, x1, x2, y):
        new_line = HorizontalLine(self.turtle, x1, x2, y)
        self.lines.append(new_line)

    def draw(self):
        for line in self.lines:
            line.draw()

    def clear(self):
        self.lines = []

    def get_lines(self):
        return self.lines


class VerticalLineStack:
    """
    going to try and implement this object using concepts from
    a linked list
    """

    def __init__(self, turtle):
        self.lines = []
        self.turtle = turtle

    def is_empty(self):
        return self.lines == []

    def add(self, y1, y2, x):
        new_line = VerticalLine(self.turtle, y1, y2, x)
        self.lines.append(new_line)

    def draw(self):
        for line in self.lines:
            line.draw()

    def clear(self):
        self.lines = []

    def get_lines(self):
        return self.lines

    def pop_line(self):
        return self.lines.pop()


if __name__ == "__main__":
    Line()
