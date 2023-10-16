"""
This will define a circle object
"""
import random
import math
import turtle
from turtle import Screen, Turtle
from typing import List, Dict, Any, Tuple, TypedDict

import numpy as np


class Point2D(TypedDict):
    """
    point on cartesian coordinate system in 2D space
    """

    x: int
    y: int


class PolarCircle:
    """
    object that represents Circle
    """

    # coordinates map a t_value (evenly spaced radians/steps)...
    # basically some weird fraction of a degree...
    # on the circle to a 2d point on cartesian coordinate system.
    T_value = float
    Coordinates = Dict[T_value, Point2D]

    def __init__(
        self,
        turtle: Turtle,
        radius: float,
        steps: int = 1000,
        theta_start: float = 0.0,
        theta_range: float = 2 * np.pi,
        center: Tuple[int, int] = (0, 0),
        amplitude: float = 0.0,
        wavelengths: float = 0.0,
    ):
        """
        params
        ----------
        turtle: python Turtle object
        radius: radius of circle
        steps: the number of coordinate points for plotting circle.
               the greater the number the smoother the curve
        start: starting point of circle. should be radian.
        theta_range: range of circle in radians. 2pi rads = full circle.
        center: center of the circle in cartesian coordinate system.
        """
        self.turtle = turtle
        self.radius = radius
        self.steps = steps
        self.theta_start = theta_start
        self.theta_range = theta_range
        self.center = center
        self.coordinates: Coordinates = {}
        self.rotation = 0
        self.amplitude = amplitude
        self.wavelengths = wavelengths

        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_t_values()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def draw(self, pen_up, random_pen_up=False, num_steps_up=0) -> None:
        """
        Draws circle
        random_pen_up: Boolean
            Decides whether or not the pen will be lifted during the drawing
            of the circle.
        num_steps_up: int
            the number of steps that the pen will be lifted upwards.
        """
        if random_pen_up:
            # at a random step along the circle, the pen will be lifted.
            random_step = random.randint(0, len(t_values) + 1)
            num_steps_lifted = math.floor(len(t_values))

        if pen_up:
            self.turtle.penup()
        for step, (t, point_2d) in enumerate(self.coordinates.items()):
            if step == 0:
                self.turtle.penup()
            if random_pen_up:
                if step in range(random_step, num_steps_up):
                    self.turtle.penup()

            x_cor = self.coordinates[t]["x"]
            y_cor = self.coordinates[t]["y"]
            self.turtle.goto(x_cor, y_cor)
            if not pen_up:
                self.turtle.pendown()

    def _get_x_coordinate(self, t) -> float:
        """
        converts polar to cartesian, returns x coordinate of turtle
        """
        return self.radius * np.cos(t + self.rotation) + self._get_x_coordinate_center()

    def _get_y_coordinate(self, t) -> float:
        """
        convert polar to cartesian, returns y coordinate of turtle
        """
        return self.radius * np.sin(t + self.rotation) + self._get_y_coordinate_center()

    def _get_x_coordinate_center(self) -> float:
        return self.center[0]

    def _get_y_coordinate_center(self) -> float:
        return self.center[1]

    def _get_t_values(self) -> npt.NDArray:
        """
        returns evenly spaced self.steps number of values over theta_range.
        """
        full_circle = np.linspace(
            start=0,
            # self.theta_start,
            stop=2 * np.pi,
            # self.theta_range,
            num=self.steps,
        )
        # want to filter values so that all arcs and circles share
        # common radian mappings ( as opposed to using self.theta_start
        # and self.theta_range in start and stop.
        filtered = [
            theta
            for theta in full_circle
            if theta >= self.theta_start and theta <= self.theta_range
        ]
        return filtered

    def _update_coordinates(self, step, x_cor, y_cor) -> None:
        """
        Parameters
        -------------
        step: int
            The step the turtle is at as he is drawing the circle.
        x_cor: float
            The x coordinate of the turtle at step int.
        y_cor: float
            the y coodinate of the turtle at step int.

        Notes:
            Recording the step will allow me to use simple logic, without
            math, to connect opposing points on the circle.

        updates coordinates of the turtle.
        """
        self.coordinates[step] = {"x": x_cor, "y": y_cor}

    def get_turtle(self) -> turtle.Turtle():
        return self.turtle

    def get_coordinates(self) -> Dict[int, Dict[float, float]]:
        return self.coordinates

    def translate_x(self, x_shift) -> None:
        """
        adds x_shift to x_coordinate of center to translate circle.
        a distance along x-axis x_shift length.
        """
        x_cor = self._get_x_coordinate_center()
        y_cor = self._get_y_coordinate_center()
        self.center = (x_cor + x_shift, y_cor)
        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_t_values()):
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

    # TODO: IF we keep this then this should use the line class
    # and instantiate a Line Object...
    def fill_with_horizontal_lines(self, gap) -> None:
        """
        gap determines how many lines to draw, bigger gap, less lines
        """

        def draw_horizontal_lines(steps_one, steps_two, coordinates):
            """
            does the actual drawing.
            """
            for step_one, step_two in list(zip(steps_one, steps_two)):
                x_one = coordinates[step_one]["x"]
                y_one = coordinates[step_one]["y"]
                x_two = coordinates[step_two]["x"]
                y_two = coordinates[step_two]["y"]
                self.turtle.penup()
                self.turtle.goto(x_one, y_one)
                self.turtle.pendown()
                self.turtle.goto(x_two, y_two)

        # fill the top half of circlce (connect 0 and 500, 1 and 499, 2 ...)
        # steps = [step for step in range(0, int(self.steps/2)+1, gap)]
        # teps_reversed = steps[::-1]
        t_vals = self._get_t_values()[: int(self.steps / 2) + 1 : gap]

        t_vals_reversed = t_vals[::-1]
        draw_horizontal_lines(t_vals, t_vals_reversed, self.coordinates)
        # fill the bottom half of circle (connect 500 and 1000, 499 and 999..)
        # steps = [step for step in range(int(self.steps/2), self.steps+1, gap)]
        # steps_reversed = steps[::-1]

        t_vals = self._get_t_values()[int(self.steps / 2) : self.steps + 1 : gap]
        t_vals_reversed = t_vals[::-1]
        draw_horizontal_lines(t_vals, t_vals_reversed, self.coordinates)

    # Again Use Line Class.
    def draw_chord(self, step_one, step_two):
        """
        draw a random chord in the circle.
        """
        x_one = self.coordinates[step_one]["x"]
        y_one = self.coordinates[step_one]["y"]
        x_two = self.coordinates[step_two]["x"]
        y_two = self.coordinates[step_two]["y"]
        self.turtle.penup()
        self.turtle.goto(x_one, y_one)
        self.turtle.pendown()
        self.turtle.goto(x_two, y_two)

    def draw_random_chord(self):
        rand_step_one = random.randint(0, self.steps)
        rand_step_two = random.randint(0, self.steps)
        return self.draw_chord(rand_step_one, rand_step_two)

    #    def get_random_arc_coordinates(self)-> Dict[int, Point2D]:
    #        """
    #        gets a subset of coordinates from the current circles coordinates
    #        """
    #        random_arc_coordinates = {}
    #        rand_step_one = random.randint(0, self.steps-2)
    #        rand_step_two = random.randint(rand_step_one, self.steps-2)
    #        if rand_step_one == rand_step_two:
    #            rand_step_two = rand_step_two+2
    #
    #        for num, t in enumerate(self._get_t_values()):
    #            if num > rand_step_one and num < rand_step_two:
    #                random_arc_coordinates[t] = {
    #                    'x': self.coordinates[t]['x'],
    #                    'y': self.coordinates[t]['y']
    #                                            }
    #        return random_arc_coordinates

    def get_arc_coordinates(self, step_num_one, step_num_two):
        arc_coordinates = {}
        for t in self._get_t_values():
            if t >= step_num_one and t <= step_num_two:
                arc_coordinates[t] = {
                    "x": self.coordinates[t]["x"],
                    "y": self.coordinates[t]["y"],
                }
        return arc_coordinates

    @staticmethod
    def generate_random_t_values():
        rand_step_one = random.uniform(0, 2 * np.pi)
        rand_step_two = random.uniform(rand_step_one, 2 * np.pi)
        return rand_step_one, rand_step_two

    def get_random_arc_coordinates(self) -> Dict[int, Point2D]:
        """
        gets a subset of coordinates from the current circles coordinates
        """
        rand_step_one, rand_step_two = self.generate_random_t_values()
        # if rand_step_two - rand_step_one < (2*np.pi/50):
        #    return self.get_random_arc_coordinates()
        return self.get_arc_coordinates(rand_step_one, rand_step_two)

    def set_center(self, x, y):
        self.center = (x, y)

    def set_radius(self, r):
        self.radius = r
        # update coordinates for every step in the circle.
        for step, t in enumerate(self._get_t_values()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

    def rotate(self, theta_rotation):
        """ """
        new_coordinates = {}
        self.rotation += theta_rotation
        for step, t in enumerate(self._get_t_values()):
            x_cor = self._get_x_coordinate(t)
            y_cor = self._get_y_coordinate(t)
            self._update_coordinates(t, x_cor, y_cor)

        # assume positive rotation
        # new_origin = 0 + step_rotation # new 0
        # new_end = 1000 - step_rotation # new 1000

        # for step, cord_dict in self.coordinates.items():
        #    new_coordinates[new_origin] = self.coordinates[step]
        #    new_origin+=1
        #    if new_origin == 1001:
        #        new_origin = 0

        # self.coordinates = new_coordinates


class PolarCircleSine(PolarCircle):
    """
    Defines new x and y coordinates to produce a wavy circle, or sine
    wave that follows the circumference of a circle.
    """

    def __init__(
        self,
        turtle,
        radius,
        steps,
        theta_start,
        theta_range,
        center,
        amplitude,
        wavelengths,
    ):
        """
        Parameters
        ----------
        turtle: python turtle object
        radius: float
            radius of circle
        steps: int
            the number of coordinate points to plot the circle.
            the greater the number the smoother the curve
        theta_range: float
            the range, defined in radians, of a circle.
            default is 2pi radians for a full circle.
        """
        super().__init__(
            turtle,
            radius,
            steps,
            theta_start,
            theta_range,
            center,
            amplitude,
            wavelengths,
        )
        # self.amplitude = amplitude
        # self.wavelengths = wavelengths

    def _get_x_coordinate(self, t):
        """
        converts polar to cartesian, returns x coordinate of turtle
        """
        new_radius = self.radius + (self.amplitude * np.sin(self.wavelengths * t))
        return (new_radius) * np.cos(t) + self._get_x_coordinate_center()

    def _get_y_coordinate(self, t):
        """
        convert polar to cartesian, returns y coordinate of turtle
        """

        new_radius = self.radius + (self.amplitude * np.sin(self.wavelengths * t))
        return (new_radius) * np.sin(t) + self._get_y_coordinate_center()


if __name__ == "__main__":
    pass
