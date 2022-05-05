"""
Creating the main map for the game.
"""

import pygame
import os

# create walls class


class wall(pygame.sprite.Sprite):
    """
    Creates a wall object that character can collide with.

    Attributes:
        _wall: A surface representing the wall.
        _rect: Represents the spawn coordinates for the wall.
    """

    def __init__(self, pos, width, height):
        pygame.sprite.Sprite.__init__(self)  # initiate pygame sprite
        self._wall = pygame.Surface([width, height])  # create wall surface
        # to test, start with making the walls red
        self._wall.fill((255, 0, 0))

        # set wall spawn coordinates to xpos and ypos
        self._rect = self._wall.get_rect()
        self._rect.x = pos[0]
        self._rect.y = pos[1]

# creating split map


class split_model(wall):
    """
    Tracks the attributes of the Split map.

    Attributes:
        _map_dimensions: A list containing the dimensions of the screen window.
        _backdrop: An image containing the background of Split.
        _wall_list: A group of all walls on the map.
    """

    def __init__(self):
        # to account for standard Windows 125% display scaling
        # actual dimensions come out to 1536 x 864
        self._map_dimensions = (1920/1.25, 1080/1.25)
        # create empty wall group
        self._wall_list = pygame.sprite.Group()
        # add test walls
        self._wall_list.add(wall((300, 400), 200, 200))
        self._wall_list.add(wall((1000, 500), 400, 300))


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
        # draw the backdrop
        self._window.blit(self._backdrop, self._window.get_rect())

    def draw_walls(self):
        """
        Draw the map's walls.

        Attributes:
            surface: The window for the walls to be drawn on
        """
        # draw the walls
        for wall in self.model._wall_list:
            self._window.blit(wall._wall, (wall._rect.x, wall._rect.y))
