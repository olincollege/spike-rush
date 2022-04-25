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
        self.spawn = [100, 100]
        self.position = [100, 100]  # set to spawn initially
        self.movement_check = 0  # initially not moving

    def move(self):
        """
        Moves the character through the map.
        """
        pass


class character_view:
    """
    Displays the character on the map. Redraw the sprite when it moves.

    Attributes:
        radius: A float representing the radius of the character.
        color: A list representing the RGB values of the character.

    """
    pass


class character_controller:
    """
    Control the test character.

    Attributes:

    """
    pass
    # create a controller to move character
    # character should move smoothly with WASD
    # have camera follow character?


# test code down here
def movement_test():
    """
    Tests movement code with a test character.
    """
    pass
