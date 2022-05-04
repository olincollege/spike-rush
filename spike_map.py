"""
Creating the main map for the game.
"""

import pygame
import os

# creating split map


class split_model:
    """
    Tracks the attributes of the Split map.

    Attributes:
        _map_dimensions: A list containing the dimensions of the screen window.
        _backdrop: An image containing the background of Split.
    """

    def __init__(self):
        # to account for standard Windows 125% display scaling
        # actual dimensions come out to 1536 x 864
        self._map_dimensions = (1920/1.25, 1080/1.25)


class split_view:
    """
    Displays the Split map on the pygame window.

    Attributes:
        model = Attributes from the split_model class.
        _window = The game window the map is drawn to.
        _backdrop: An image containing the background of Split.
    """

    def __init__(self, model):
        self.model = model  # from split_model
        # set 1920x1080 full screen window
        self._window = pygame.display.set_mode(self.model._map_dimensions,
                                               pygame.FULLSCREEN)
        self._backdrop = \
            pygame.transform.scale(pygame.image.load
                                   (os.path.join('images',
                                                 'map',
                                                 'split_layout.png')).convert(),
                                   self.model._map_dimensions)

    def draw_map(self):
        """
        Redraws the map.

        Attributes:
            surface: The window for the map to be drawn on
        """
        self._window.blit(self._backdrop, self._window.get_rect())
