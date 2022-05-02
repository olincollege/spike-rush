"""
Creating the main map for the game.
"""

import pygame

# creating split map


class split_model:
    """
    Tracks the attributes of the Split map.

    Attributes:
        _map_dimensions: A list containing the dimensions of the screen window.
    """

    def __init__(self):
        self._map_dimensions = [1920, 1080]


class split_view:
    """
    Displays the Split map on the pygame window.

    Attributes:
        model = Attributes from the split_model class.
        _window = The game window the map is drawn to.
    """

    def __init__(self, model):
        self.model = model  # from split_model
        self._window = pygame.display.set_mode(model._map_dimensions)

    def display_map(self, color):
        """
        Redraws the map.

        Attributes:
            color: A list containing the integer RGB values of the map.
        """
        self._window.fill(color)
