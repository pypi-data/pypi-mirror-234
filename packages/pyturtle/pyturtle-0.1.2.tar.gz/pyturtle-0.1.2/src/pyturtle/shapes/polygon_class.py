"""
Class to create a polygon of any size with any number of sides
"""


class Polygon:
    """
    used to create a polygon with any number of sides
    """

    def __init__(self, turt, side_len, n_sides, direction="right"):
        """
        Parameters
        ------------
        side_len: int
            the length of the side of the polygon

        n_sides: int
            the number of sides of the polygon
            3 will give you a triange
            4 will give you a square
            5 will give you a pentagon
        """

        self.side_len = side_len
        self.n_sides = n_sides
        self.direction = direction

    def draw(self):
        interior_angle = 360 / self.n_sides
        if self.direction == "left":
            for x in range(self.n_sides):
                self.t.forward(self.side_len)
                self.t.left(interior_angle)
        else:
            for x in range(self.n_sides):
                self.t.forward(self.side_len)
                self.t.right(interior_angle)
