from typing import Dict
import numpy.typing as npt
import numpy as np

from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D


class Arc(Shape):
    Radian = float
    Coordinates = Dict[int, Point2D]

    def __init__(
        self,
        turtle,
        steps,
        color,
        coordinates,
        center: Point2D,
        radius: float,
        start_theta: Radian = 0,
        end_theta: Radian = ((2 * np.pi) / 8),
    ):
        super().__init__(turtle, steps, color, coordinates)
        self.center = center
        self.radius = radius
        self.start_theta = start_theta
        self.end_theta = end_theta

    def draw(self):
        pass

    def _get_radians_lin_split(self) -> npt.NDArray:
        """
        returns evenly spaced self.steps number of values over theta_range.
        """
        full_circle_lin_split = np.linspace(
            start=0,
            # self.theta_start,
            stop=2 * np.pi,
            # self.theta_range,
            num=self.steps,
        )
        # want to filter values so that all arcs and circles share
        # common radian mappings ( as opposed to using self.theta_start
        # and self.theta_range in start and stop.
        arc_lin_split = [
            theta
            for theta in full_circle_lin_split
            if theta >= self.theta_start and theta <= self.theta_range
        ]
        return arc_lin_split

    def translate_x(self, x_shift) -> None:
        """
        adds x_shift to x_coordinate of center to translate circle.
        a distance along x-axis x_shift length.
        """
        x_cent, y_cent = self.center
        self.center = (x_cent + x_shift, y_cor)
        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_radians_lin_split()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def translate_y(self, y_shift) -> None:
        """
        adds y_shift to y_coordinate of center to translate circle
        a distance along y-axis y-shift length.
        """
        x_cor = self._get_x_coordinate_center()
        y_cor = self._get_y_coordinate_center()
        self.center = (x_cor, y_cor + y_shift)
        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_t_values()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def translate_xy(self, x_shift, y_shift) -> None:
        """
        shifts circle in both x and y direction.
        """
        x_cor = self._get_x_coordinate_center()
        y_cor = self._get_y_coordinate_center()
        self.center = (x_cor + x_shift, y_cor + y_shift)
        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_t_values()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)


class Circle(Arc):
    def __init__(self, turtle, color, center, radius):
        super().__init__(turtle, color, center, radius, 0, 360)
