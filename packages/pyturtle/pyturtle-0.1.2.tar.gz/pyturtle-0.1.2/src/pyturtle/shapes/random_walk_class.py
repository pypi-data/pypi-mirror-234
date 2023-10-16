"""
Class to create a randomwalk object
"""
import random


class RandomWalk(object):
    """
    A 2D randomwalk object. Variables included in the random
    walk are in the __init__ function.
    """

    def __init__(self, turtle, steps, width, height, offsetx, offsety):
        """
        Parameters
        ----------
        turtle: turtle object

        steps: int
            number of steps for random walk to take.

        width: int
            the width of the random walk. can not go outside
            box defined by width length

        height: int
            the height of the random walk. cannot go outside
            box defined by height length.

        Returns
        ----------
        None
        """
        self.turtle = turtle
        # x is key, y is value.
        self.coordinates = {}
        self.steps = steps
        self.width = width
        self.height = height
        self.offsetx = offsetx
        self.offsety = offsety

    def draw_random_walk(self):
        """
        Parameters
        -------------
        self

        Returns
        -------------
        None

        This is the main function which executes the two
        functions below
        """
        for _ in range(self.steps):
            self.move()
            if not -300 / 2 < self.turtle.xcor() < 300 / 2:
                self.turtle.undo()
                self.turtle.setheading(180 - self.turtle.heading())
            elif not -300 / 2 < self.turtle.ycor() < 300 / 2:
                self.turtle.undo()
                self.turtle.setheading(360 - self.turtle.heading())

            elif (
                not -(self.width / 2 + abs(self.offsetx))
                < self.turtle.xcor()
                < (self.width / 2 + self.offsetx)
            ):
                print(self.turtle.xcor())
                print(self.offsetx + self.width / 2)
                self.turtle.undo()
                self.turtle.setheading(180 - self.turtle.heading())

            elif (
                not -(self.height / 2 + abs(self.offsety))
                < self.turtle.ycor()
                < (self.height / 2 + self.offsety)
            ):
                print(self.turtle.ycor())
                print(self.offsety + self.height / 2)
                self.turtle.undo()
                self.turtle.setheading(360 - self.turtle.heading())

            else:
                self.coordinates[self.turtle.xcor()] = self.turtle.ycor()
                self.turn()
                print(self.width / 2 + self.offsetx)

    def move(self, for_len=(1, 10), back_len=(1, 10), penup_prob=0):
        """
        Parameters
        ------------
        for_len_r: tuple containing ints --> (25, 50)
            the turtle will randomly choose a value
            between 25 and 50 and move forward that amount

        OR

        for_len_r: int
            turtle always moves forward this length

        ####################################################

        back_len_r: tuple containing ints --> (25, 50)
            the turtle will randomly choose an integer
            between 25 and 50 and move backward that amount

        OR

        back_len_r: int
            the turtle will always move backward this amount

        ####################################################

        penup_prob: int
            an number between 0 and 1 (0 inclusive 1 exclusive)
            0 means the turtle will never be lifted while the turtle
            draws .99 means the turtle will be lifted 99% of the time
            while the turtle draws. Higher number, less visible lines.

            no more than digits after decimal

        Returns
        --------------
        None

        this function moves the turtle forward half of the time and
        backward half of the time while drawing at least
        """

        def check_type(tuple_or_int):
            """
            Parameters
            -----------
            tuple_or_int: tuple or int
                if tuple generate random number in tuple range
                if int do nothin

            Returns
            ----------
            length: int
                the lenth the turtle will move
            """

            if isinstance(tuple_or_int, tuple):
                length = random.randrange(*tuple_or_int)
            elif isinstance(tuple_or_int, int):
                length = tuple_or_int
            else:
                raise ValueError("for_len must be of type tuple or int")

            return length

        switch = random.randint(0, 1)
        penup_switch = random.uniform(0, 1)
        for_len = check_type(for_len)
        back_len = check_type(back_len)

        if switch:
            if penup_switch < penup_prob:
                self.turtle.penup()
            self.turtle.forward(for_len)

        else:
            if penup_switch < penup_prob:
                self.turtle.penup()
            self.turtle.backward(back_len)

        self.turtle.pendown()

    def turn(self, right_angle=90, left_angle=90):
        """
        please the pylint gods
        """
        switch = random.randint(0, 1)

        if switch:
            self.turtle.right(right_angle)
        else:
            self.turtle.left(left_angle)

    def destroy(self):
        self.turtle.bye()

    def get_coordinates(self):
        return self.coordinates

    def get_turtle(self):
        return self.turtle
