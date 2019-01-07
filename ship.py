#############################################################
# FILE : ship.py
# WRITERS : shaked_weitz , shaked.weitz , 206093403
# yarden_tal, yardental , 203730700
# EXERCISE : intro2cs ex9 2016-2017
# DESCRIPTION: a class of a ship in a asteroids game
#############################################################
############################################################
# Imports
############################################################
import random
import math


class Ship:
    DEFAULT_HEADING = 0
    DEFAULT_SPEED = 0
    DEFAULT_RADIUS = 1
    DEFAULT_LIFE = 3

    def __init__(self, screen):
        self.__x = (random.randrange(screen.SCREEN_MAX_X), self.DEFAULT_SPEED)
        self.__y = (random.randrange(screen.SCREEN_MAX_Y), self.DEFAULT_SPEED)
        self.__heading = self.DEFAULT_HEADING
        self.__screen = screen
        self.__radius = self.DEFAULT_RADIUS
        self.__life = self.DEFAULT_LIFE

    def draw(self):
        """
        draws ship on screen
        """
        self.__screen.draw_ship(self.__x[0], self.__y[0], self.__heading)

    def get_x(self):
        """:returns a tuple, x values"""
        return self.__x

    def get_y(self):
        """:returns a tuple, y values"""
        return self.__y

    def get_heading(self):
        """:returns ship heading in degrees"""
        return self.__heading

    def change_coord_x(self, x):
        """receives a tuple and updates x values"""
        self.__x = x, self.__x[1]

    def change_coord_y(self, y):
        """receives a tuple and updates y values"""
        self.__y = y, self.__y[1]

    def change_heading(self, direction):
        """
        changes heading of ship on pressed key
        """
        new_heading = self. __heading + direction
        if new_heading <= 0:
            new_heading += 360
        elif new_heading > 360:
            new_heading -= 360
        self.__heading = new_heading

    def new_speed(self):
        """update speed """
        new_speed_x = (self.__x[1] + math.cos(math.radians(self.__heading)))
        new_speed_y = (self.__y[1] + math.sin(math.radians(self.__heading)))
        self.__x = self.__x[0], new_speed_x
        self.__y = self.__y[0], new_speed_y

    def get_radius(self):
        """returns ship radius"""
        return self.__radius


    def get_life(self):
        """returns ship life"""
        return self.__life

    def reduce_life(self):
        """updates and returns ship life"""
        self.__life -= 1
        return self.__life
