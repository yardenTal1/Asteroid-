############################################################
# FILE : torpedo.py
# WRITERS : shaked_weitz , shaked.weitz , 206093403
# yarden_tal, yardental , 203730700
# EXERCISE : intro2cs ex9 2016-2017
# DESCRIPTION: a class of a torpedo in a asteroids game
#############################################################
############################################################
# Imports
############################################################
import math


class Torpedo:
    """
    Initializes a torpedo
    x and y are tuples with place and speed
    torpedo heading
    """
    ACCELERATION_FACTOR = 2
    RADIUS = 4
    TORPEDO_LIFE = 200

    def __init__(self, x, y, heading):
        self.__x = x
        self.__y = y
        self.__heading = heading
        self.speed()
        self.__radius = self.RADIUS
        self.__life = self.TORPEDO_LIFE

    def draw(self, screen):
        """
        draws torpedo on screen
        """
        screen.draw_torpedo(self, self.__x[0], self.__y[0], self.__heading)

    def get_radius(self):
        """returns torpedo radius"""
        return self.__radius

    def get_x(self):
        """:returns a tuple, x values"""
        return self.__x

    def get_y(self):
        """:returns a tuple, y values"""
        return self.__y

    def change_coord_x(self, x):
        """receives a tuple and updates x values"""
        self.__x = x, self.__x[1]

    def change_coord_y(self, y):
        """receives a tuple and updates y values"""
        self.__y = y, self.__y[1]

    def speed(self):
        """sets torpedo speed"""
        new_speed_x = self.__x[1] + self.ACCELERATION_FACTOR * math.cos(math.radians(self.__heading))
        new_speed_y = self.__y[1] + self.ACCELERATION_FACTOR * math.sin(math.radians(self.__heading))
        self.__x = (self.__x[0], new_speed_x)
        self.__y = (self.__y[0], new_speed_y)

    def reduce_life(self):
        """updates and returns torpedo life"""
        self.__life -= 1
        return self.__life

    def get_life(self):
        """returns torpedo life"""
        return self.__life




