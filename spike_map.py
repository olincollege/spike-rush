"""
Creating the main map for the game.
"""
import os
import pygame
from zones import SpawnZone, PlantZone

# create walls class


class Wall(pygame.sprite.Sprite):  # pylint:disable=R0903
    # Useful class to have for the sprite even if there aren't
    # a high number of public methods.
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

        # set wall spawn coordinates to xpos and ypos
        self.rect = self._wall.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @property
    def wall(self):
        """
        Returns the wall.

        Returns:
            A Sprite representing a wall.
        """
        return self._wall

# creating split map


class SplitModel():
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
        self._wall_list.add(Wall((63, 21), 1450, 3))
        self._wall_list.add(Wall((64, 21), 3, 358))

        # top
        self._wall_list.add(Wall((346, 21), 123, 162))
        self._wall_list.add(Wall((759, 21), 120, 96))
        self._wall_list.add(Wall((1160, 21), 196, 104))

        # right
        self._wall_list.add(Wall((1515, 21), 3, 765))

        # bottom
        self._wall_list.add(Wall((400, 788), 1130, 3))
        self._wall_list.add(Wall((1110, 709), 77, 85))
        self._wall_list.add(Wall((708, 737), 269, 55))
        self._wall_list.add(Wall((21, 737), 587, 55))

        # left
        self._wall_list.add(Wall((21, 470), 3, 267))
        self._wall_list.add(Wall((21, 379), 260, 91))

        # inner walls
        self._wall_list.add(Wall((151, 566), 68, 74))
        self._wall_list.add(Wall((810, 579), 95, 74))
        self._wall_list.add(Wall((890, 365), 218, 100))
        self._wall_list.add(Wall((1274, 230), 82, 295))

        # the t shaped one
        self._wall_list.add(Wall((442, 365), 256, 76))
        self._wall_list.add(Wall((530, 441), 168, 24))
        self._wall_list.add(Wall((530, 441), 78, 112))

        # Attacker spawn zone
        # Zone(250.08, 28.27, 283.10, 155.12)
        self._attacker_spawn = SpawnZone(64, 21, 283, 155)

        # Defender spawn zone
        # Zone(1542.59, 229.73, 158.95, 295.83)
        self._defender_spawn = SpawnZone(1356, 226, 158, 295)

        # Spike plant zone
        # Zone(794.23, 464.98, 499.48, 318.22)
        self._a_site = PlantZone(608, 465, 499, 318)

    @property
    def wall_list(self):
        """
        Returns a list of walls present on the map.

        Return: A Sprite group representing all of the walls on Split.
        """
        return self._wall_list

    @property
    def attacker_spawn(self):
        """
        Returns the attacker spawn zone.

        Returns:
            A SpawnZone representing the attacker spawn location on Split.
        """
        return self._attacker_spawn

    @property
    def defender_spawn(self):
        """
        Returns the defender spawn zone.

        Returns:
            A SpawnZone representing the defender spawn location on Split.
        """
        return self._defender_spawn

    @property
    def a_site(self):
        """
        Returns the plant location on Split A site map.

        Returns:
            A PlantZone representing the plant area on Split.
        """
        return self._a_site

    @property
    def map_dimensions(self):
        """
        Returns the dimensions of the map.

        Returns:
            A Tuple containing the dimensions of the map.
        """
        return self._map_dimensions


class SplitView:
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
        self._window = pygame.display.set_mode(self.model.map_dimensions)

        # add window caption
        pygame.display.set_caption("Spike Rush")

        self._backdrop = \
            pygame.transform.scale(pygame.image.load
                                   (os.path.join('images',
                                                 'map',
                                                 'split_color.png')).convert(),
                                   self.model.map_dimensions)

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
        for wall in self.model.wall_list:
            self._window.blit(wall.wall, (wall.rect.x, wall.rect.y))

    def draw_other_screen(self, image):
        """
        Draws full screens other than the main game map.

        Arguments:
            image: A string representing the image to be blitted.
            surface: The surface to blit the screen on to.
        Returns:
            None.
        """
        screen = \
            pygame.transform.scale(pygame.image.load
                                   (os.path.join('images',
                                                 'other_screens',
                                                 image)).convert(),
                                   (1536, 864))

        self._window.blit(screen, self._window.get_rect())
