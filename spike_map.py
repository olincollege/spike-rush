"""
Creating the main map for the game.
"""

import pygame
import os
from zones import *

# create walls class


class wall(pygame.sprite.Sprite):
    """
    Creates a wall object that character can collide with.

    Attributes:
        _wall: A surface representing the wall.
        rect: Represents the spawn coordinates for the wall.
    """

    def __init__(self, pos, width, height):
        pygame.sprite.Sprite.__init__(self)  # initiate pygame sprite
        self._wall = pygame.Surface([width, height])  # create wall surface
        # to test, start with making the walls red
        self._wall.fill((255, 0, 0))

        # set wall spawn coordinates to xpos and ypos
        self.rect = self._wall.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

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
        # to account for standard Windows 125% display scaling, divide
        # dimensions by 1.25

        # actual dimensions come out to 1536 x 864
        self._map_dimensions = (1920/1.25, 1080/1.25)

        # create empty wall group
        self._wall_list = pygame.sprite.Group()

        # add Split map walls (position (x, y), width, height)

        # top left
        self._wall_list.add(wall((63, 21), 1450, 3))
        self._wall_list.add(wall((64, 21), 3, 358))

        # top
        self._wall_list.add(wall((346, 21), 123, 162))
        self._wall_list.add(wall((759, 21), 120, 96))
        self._wall_list.add(wall((1160, 21), 196, 104))

        # right
        self._wall_list.add(wall((1515, 21), 3, 765))

        # bottom
        self._wall_list.add(wall((400, 788), 1130, 3))
        self._wall_list.add(wall((1110, 709), 77, 85))
        self._wall_list.add(wall((708, 737), 269, 55))
        self._wall_list.add(wall((21, 737), 587, 55))

        # left
        self._wall_list.add(wall((21, 470), 3, 267))
        self._wall_list.add(wall((21, 379), 260, 91))

        # inner walls
        self._wall_list.add(wall((151, 566), 68, 74))
        self._wall_list.add(wall((810, 579), 95, 74))
        self._wall_list.add(wall((890, 365), 218, 100))
        self._wall_list.add(wall((1274, 230), 82, 295))

        # the t shaped one
        self._wall_list.add(wall((442, 365), 256, 76))
        self._wall_list.add(wall((530, 441), 168, 24))
        self._wall_list.add(wall((530, 441), 78, 112))

        # Attacker spawn zone
        self._attacker_spawn = SpawnZone(64, 21, 283, 155) # Zone(250.08, 28.27, 283.10, 155.12)

        # Defender spawn zone
        self._defender_spawn = SpawnZone(1356, 226, 158, 295) # Zone(1542.59, 229.73, 158.95, 295.83)

        # Spike plant zone
        self._a_site = PlantZone(794, 465, 499, 318) # Zone(794.23, 464.98, 499.48, 318.22)
    @property
    def attacker_spawn(self):
        return self._attacker_spawn

    @property
    def defender_spawn(self):
        return self._defender_spawn

    @property
    def a_site(self):
        return self._a_site
    



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
        self._window = pygame.display.set_mode(self.model._map_dimensions)

        # add window caption
        pygame.display.set_caption("Spike Rush")

        self._backdrop = \
            pygame.transform.scale(pygame.image.load
                                   (os.path.join('images',
                                                 'map',
                                                 'split_color.png')).convert(),
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
            self._window.blit(wall._wall, (wall.rect.x, wall.rect.y))
