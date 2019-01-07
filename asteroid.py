#############################################################
# FILE : asteroid.py
# WRITERS : shaked_weitz , shaked.weitz , 206093403
# yarden_tal, yardental , 203730700
# EXERCISE : intro2cs ex9 2016-2017
# DESCRIPTION: a class of asteroids
#############################################################
############################################################
# Imports
############################################################
import random
import math


class Asteroid:
    DEFAULT_SIZE = 3
    LARGE_COEFFICIENT = 10
    NORMALIZATION_FACTOR = -5
    SPEED_RANGE = 6

    def __init__(self, screen):
        self.__x = (random.randrange(screen.SCREEN_MAX_X), random.randrange(1, self.SPEED_RANGE))
        self.__y = (random.randrange(screen.SCREEN_MAX_Y), random.randrange(1, self.SPEED_RANGE))
        self.__size = self.DEFAULT_SIZE
        self.__screen = screen

    def draw(self):
        """
        draws asteroid on screen
        """
        self.__screen.draw_asteroid(self, self.__x[0], self.__y[0])

    def get_x(self):
        """:returns a tuple, x values"""
        return self.__x

    def get_y(self):
        """:returns a tuple, y values"""
        return self.__y

    def get_size(self):
        """:returns an int, asteroid size"""
        return self.__size

    def change_coord_x(self, x):
        """receives a tuple and updates x values"""
        self.__x = x, self.__x[1]

    def change_coord_y(self, y):
        """receives a tuple and updates y values"""
        self.__y = y, self.__x[1]

    def radius(self):
        """returns asteroid radius"""
        radius_asteroid = self.__size * self.LARGE_COEFFICIENT + self.NORMALIZATION_FACTOR
        return radius_asteroid

    def has_intersection(self, obj):
        """returns true if asteroid has intersection"""
        obj_x = obj.get_x()
        obj_y = obj.get_y()
        distance = math.sqrt((obj_x[0]-self.__x[0])**2 + (obj_y[0] - self.__y[0])**2)
        if distance <= (self.radius() + obj.get_radius()):
            return True
        return False

    def split(self, torpedo_speed_x, torpedo_speed_y):
        """receives torpedo speed and returns new speeds for split asteroid"""
        new_x = self.__x[0]
        new_y = self.__y[0]
        new_speed_x = (torpedo_speed_x + self.__x[1])/math.sqrt(self.__x[1]**2 + self.__y[1]**2)
        new_speed_y = (torpedo_speed_y + self.__y[1]) / math.sqrt(self.__x[1] ** 2 + self.__y[1] ** 2)
        new_1_x = new_x, new_speed_x
        new_1_y = new_y, new_speed_y
        new_2_x = new_x, -1*new_speed_x
        new_2_y = new_y, -1*new_speed_y
        return new_1_x, new_1_y, new_2_x, new_2_y

    def set_asteroid(self, x, y, size):
        """receives two tuples and an int, updates asteroid x,y and size"""
        self.__x = x
        self.__y = y
        self.__size = size
