"""
Creates a controller to provide movement for agents
"""

import pygame

# import test map
# test map dimensions: 1500 x 500 pixels
from game_map import spike_map


# Starting with creating a test character to test movement
class character_model:
    """
    Tracks the status of the test character.

    Attributes:
        spawn: A list containing the coordinates of the spawn location on
        the map.
        position: A list containing the current coordinates of the character.
        movement_check: An integer that checks if the player is currently
        moving.
    """

    def __init__(self):
        """
        Spawn the character in the world.
        """
        self._spawn = [100, 100]
        self._position = [100, 100]  # set to spawn initially
        self._movement_check = 0  # initially not moving

# trying to use sprite module to represent a character


class character_view(pygame.sprite.Sprite):
    """
    Displays the character on the map. Redraw the sprite when it moves.

    Attributes:
        _radius: A float representing the radius of the character.
        _color: A list representing the RGB values of the character.
    """

    def __init__(self):
        self._radius = 2.5
        self._color = [255, 0, 0]  # red color

    def draw(self, surface, position):
        """
        Draws the current location of the character on the map.

        Arguments:
            surface: The map for the character to be drawn on
            position: a list representing the current coordinates of the
            character.
        """
        # character is currently a circle
        pygame.draw.circle(surface, self._color, position, self._radius)


class character_controller:
    """
    Control the test character.
    """
    # create a controller to move character
    # character should move smoothly with WASD
    # have camera follow character?

    def move(self):
        """
        Moves the character through the map.
        """
        pass

# test code down here


def movement_test():
    """
    Tests movement code with a test character.
    """
    pass
