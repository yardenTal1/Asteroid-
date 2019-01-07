#############################################################
# FILE : asteroids_main.py
# WRITERS : shaked_weitz , shaked.weitz , 206093403
# yarden_tal, yardental , 203730700
# EXERCISE : intro2cs ex9 2016-2017
# DESCRIPTION: runs a game of asteroids
#############################################################
############################################################
# Imports
############################################################
from screen import Screen
import sys
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import random

DEFAULT_ASTEROIDS_NUM = 3


class GameRunner:
    SPIN_LEFT = 7
    SPIN_RIGHT = -7
    DEFAULT_SCORE = 0
    WIN_MESSAGE = "you are the winner!!!"
    TITLE_WIN = "Game over!"
    STOP_GAME_MESSAGE = "goodbye!"
    TITLE_STOP_GAME = "Game is stopped"
    LOST_MESSAGE = "you lost... try again."
    TITLE_LOST = "Game over!"

    def __init__(self, asteroids_amnt):
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.__ship = Ship(self._screen)
        self.__torpedo = []
        self.__asteroid = []
        self.__score = self.DEFAULT_SCORE
        if asteroids_amnt == 0:
            asteroids_amnt = DEFAULT_ASTEROIDS_NUM
        for i in range(asteroids_amnt):
            asteroid = Asteroid(self._screen)
            self.__asteroid.append(asteroid)
            self._screen.register_asteroid(asteroid, asteroid.get_size())
        # checks starting position of asteroids an ship
        self.check_position()

    def move(self, obj):
        """ receives an object, changes it's coordinates according to their speed"""
        x, speed_x = obj.get_x()
        y, speed_y = obj.get_y()
        new_coord_x = ((speed_x + x - self.screen_min_x) % (self.screen_max_x - self.screen_min_x)) + self.screen_min_x
        new_coord_y = ((speed_y + y - self.screen_min_y) % (self.screen_max_y - self.screen_min_y)) + self.screen_min_y
        obj.change_coord_x(new_coord_x)
        obj.change_coord_y(new_coord_y)

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def check_position(self):
        """checks if ship and asteroids are in same place"""
        for asteroid in self.__asteroid:
            asteroid_x = asteroid.get_x()
            asteroid_y = asteroid.get_y()
            ship_x = self.__ship.get_x()
            ship_y = self.__ship.get_y()
            # if ship and an asteroid in same place
            while asteroid_x[0] == ship_x[0] and asteroid_y[0] == ship_y[0]:
                new_x = random.random(self._screen.SCREEN_MAX_X)
                new_y = random.random(self._screen.SCREEN_MAX_Y)
                asteroid.change_coord_x(new_x)
                asteroid.change_coord_y(new_y)
            asteroid.draw()

    def key(self):
        """
        checks if a keyboard key was pressed
        spins ship accordingly or shoots torpedo
        """
        if self._screen.is_right_pressed():
            self.__ship.change_heading(self.SPIN_RIGHT)
        elif self._screen.is_left_pressed():
            self.__ship.change_heading(self.SPIN_LEFT)
        elif self._screen.is_up_pressed():
            self.__ship.new_speed()
        elif self._screen.is_space_pressed() and len(self.__torpedo) <= 15:
            # shoot
            torpedo = Torpedo(self.__ship.get_x(), self.__ship.get_y(), self.__ship.get_heading())
            self._screen.register_torpedo(torpedo)
            self.__torpedo.append(torpedo)

    def update_torpedo(self):
        """
        updates torpedo life, moves or removes by current life
        """
        torpedo_to_remove = 0
        for torpedo in self.__torpedo:
            if torpedo.get_life() > 0:
                torpedo.draw(self._screen)
                self.move(torpedo)
                torpedo.reduce_life()
            else:
                torpedo_to_remove = torpedo
        if torpedo_to_remove != 0:
            self._screen.unregister_torpedo(torpedo_to_remove)
            self.__torpedo.remove(torpedo_to_remove)

    def _game_loop(self):
        """
        runs one loop in the game
        moves and draws all objects
        called end game when needed
        """
        self.__ship.draw()
        if not self.status_game():
            # key pressed
            self.key()
            # update torpedoes
            self.update_torpedo()
            # move asteroids
            for asteroid in self.__asteroid:
                self.move(asteroid)
                asteroid.draw()
            # move ship
            self.move(self.__ship)
            # check intersections
            self.intersection_asteroids()
            self.intersection_torpedo()
        else:
            self._screen.end_game()
            sys.exit()

    def intersection_asteroids(self):
        """
        checks if asteroids and ship have an intersection
        shows a message accordingly ,updates ship life
        removes asteroid from the game
        """
        for asteroid in self.__asteroid:
            if asteroid.has_intersection(self.__ship):
                asteroid_to_remove = asteroid
                self._screen.show_message('Intersection!', 'Life is reduced to your spaceship')
                self._screen.remove_life()
                self.__ship.reduce_life()
                self._screen.unregister_asteroid(asteroid)
                self.__asteroid.remove(asteroid_to_remove)
                break

    def intersection_torpedo(self):
        """
        checks if torpedo and asteroids have an intersection
        splits asteroid to two and removes hit one from the game
        """
        for asteroid in self.__asteroid:
            for torpedo in self.__torpedo:
                if asteroid.has_intersection(torpedo):
                    asteroid_to_remove = asteroid
                    self.score(asteroid)
                    # split asteroid
                    size = asteroid.get_size()
                    if size > 1:
                        new_1_x, new_1_y, new_2_x, new_2_y = asteroid.split(torpedo.get_x()[1], torpedo.get_y()[1])
                        # create new asteroids
                        asteroid1 = Asteroid(self._screen)
                        asteroid2 = Asteroid(self._screen)
                        asteroid1.set_asteroid(new_1_x, new_1_y, size-1)
                        asteroid2.set_asteroid(new_2_x, new_2_y, size-1)
                        self.__asteroid.append(asteroid1)
                        self.__asteroid.append(asteroid2)
                        self._screen.register_asteroid(asteroid1, size-1)
                        self._screen.register_asteroid(asteroid2, size - 1)
                    # unregister from screen
                    self._screen.unregister_torpedo(torpedo)
                    self._screen.unregister_asteroid(asteroid)
                    # remove from game
                    self.__torpedo.remove(torpedo)
                    self.__asteroid.remove(asteroid_to_remove)
                    break

    def score(self, asteroid):
        """updates game score by asteroid size"""
        # points
        size = asteroid.get_size
        if size == 3:
            self.__score += 20
        elif size == 2:
            self.__score += 50
        else:
            self.__score += 100
        self._screen.set_score(self.__score)

    def status_game(self):
        """:return True and print a end message to the screen if the game is over and False if its not"""
        bool_end_game = True
        # the player has won
        if len(self.__asteroid) == 0:
            self._screen.show_message(self.TITLE_WIN, self.WIN_MESSAGE)
        # the player has lost
        elif self.__ship.get_life() == 0:
            self._screen.show_message(self.TITLE_LOST, self.LOST_MESSAGE)
        # the player ask to end the play
        elif self._screen.should_end():
            self._screen.show_message(self.TITLE_STOP_GAME, self.STOP_GAME_MESSAGE)
        else:
            bool_end_game = False
        return bool_end_game


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )