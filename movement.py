"""
Creates a controller to provide movement for agents
"""

import pygame
import os

# import test map
# test map dimensions: 1500 x 500 pixels
from spike_map import split_model, split_view


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
        self.position = self._spawn  # set to spawn initially
        self._movement_check = 0  # initially not moving
        self._frame = 0  # count frames


# trying to use sprite module to represent a character


class character_view(pygame.sprite.Sprite):
    """
    Displays the character on the map. Redraw the sprite when it moves.

    Attributes:
        _sprites: A list containing sprites that represent the character.
        _sprite: An image representing the character
    """

    def __init__(self, character):
        # get attributes from character_model
        self.character = character

        # initiate sprite stuff
        pygame.sprite.Sprite.__init__(self)  # initiate pygame sprite
        # image for sprite representation
        self._sprites = [os.path.join('images', 'sprites', 'test_sprite.png')]
        # currently only using one image, scaling size down
        self._sprite = \
            pygame.transform.scale(pygame.image.load(os.path.join(
                'images', 'sprites', 'test_sprite.png')).convert_alpha(),
                (50, 50))
        self.rect = self._sprite.get_rect()
        self.rect.x = self.character.position[0]
        self.rect.y = self.character.position[1]

    def draw_sprite(self, surface):
        """
        Draws the current location of the character on the map.

        Arguments:
            surface: The map for the character to be drawn on
            position: a list representing the current coordinates of the
            character.
        """
        self.rect.x = self.character.position[0]
        self.rect.y = self.character.position[1]

        # draw sprite on to surface
        surface.blit(self._sprite, (self.rect.x, self.rect.y))


class character_controller:
    """
    Control the test character.

    Attributes:
        character = Attributes from the character_model class.
        view = Attributes from the character_view class.
    """
    # create a controller to move character
    # character should move smoothly with WASD
    # have camera follow character?

    def __init__(self, character, view):
        self.character = character  # from character_model
        self.view = view  # from character_view

    def move(self, speed, keys, walls):
        """
        Moves the character through the map. Detects pressed keys and moves
        the character correspondingly. Also detects collisions with walls and
        prevents character movement

        Arguments:
            speed: An integer representing the number of pixels a character
            moves per frame.
            keys: A list containing which keys are currently pressed.
            walls: A sprite group of all walls on the map.
        """
        xchange = 0
        ychange = 0

        # searches for arrow keys and WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # left
            xchange = -speed
            self.character.position[0] -= speed
            self.view.rect.x = self.character.position[0]

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # right
            self.character.position[0] += speed
            xchange = speed
            self.view.rect.x = self.character.position[0]

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view, walls, False)
        for wall in collision_list:
            # reset position
            if xchange > 0:
                self.view.rect.right = wall.rect.left
                self.character.position[0] = self.view.rect.left
            elif xchange < 0:
                self.view.rect.left = wall.rect.right
                self.character.position[0] = self.view.rect.left

        if keys[pygame.K_UP] or keys[pygame.K_w]:  # up
            self.character.position[1] -= speed
            ychange = -speed
            self.view.rect.y = self.character.position[1]

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # down
            self.character.position[1] += speed
            ychange = speed
            self.view.rect.y = self.character.position[1]

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view, walls, False)
        for wall in collision_list:
            # reset position
            if ychange > 0:
                self.view.rect.bottom = wall.rect.top
                self.character.position[1] = self.view.rect.top
            elif ychange < 0:
                self.view.rect.top = wall.rect.bottom
                self.character.position[1] = self.view.rect.top


# test code down here


def movement_test():
    """
    Tests movement code with a test character.
    """
    pygame.init()  # initialize pygame
    map_model = split_model()
    map_view = split_view(map_model)  # initialize map
    clock = pygame.time.Clock()  # to keep track of time in-game
    character_speed = 10

    # create instances of classes
    character = character_model()  # include parentheses when creating instance
    view = character_view(character)
    controller = character_controller(character, view)

    # main loop
    run = True
    while run:

        # sense inputs (get events)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                run = False

        # update states
        # create entities
        # detect interactions

        # movement
        # check which keys are currently pressed
        keys = pygame.key.get_pressed()
        # if no collisions are detected, move character
        controller.move(character_speed, keys, map_model._wall_list)

        # update stuff
        map_view.draw_map()
        map_view.draw_walls()

        # draw character
        view.draw_sprite(map_view._window)

        pygame.display.flip()  # update entire display
        clock.tick(30)  # reduce framerate to 30

    # print(map_view._window.get_rect()) #check window dimensions
    pygame.quit()  # after main loop has finished
