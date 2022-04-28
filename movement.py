"""
Creates a controller to provide movement for agents
"""

import pygame
import os

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
        self.position = [100, 100]  # set to spawn initially
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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # initiate pygame sprite
        # image for sprite representation
        self._sprites = [os.path.join('sprites', 'test_sprite.png')]
        # currently only using one image, scaling size down
        self._sprite = \
            pygame.transform.scale(pygame.image.load(os.path.join(
                'sprites', 'test_sprite.png')).convert_alpha(), (75, 75))

    def draw_sprite(self, surface, position):
        """
        Draws the current location of the character on the map.

        Arguments:
            surface: The map for the character to be drawn on
            position: a list representing the current coordinates of the
            character.
        """
        surface.blit(self._sprite, position)


class character_controller:
    """
    Control the test character.
    """
    # create a controller to move character
    # character should move smoothly with WASD
    # have camera follow character?

    def __init__(self, character):
        self.character = character  # from character_model

    def move(self, event, speed):
        """
        Moves the character through the map. Takes a keypress and returns the
        corresponding direction.

        Attributes:
            event: An event representing a player input.
            speed: An integer representing the number of pixels a character
            moves per frame.
        """
        # searches for arrow keys and WASD
        if event.key == pygame.K_LEFT or event.key == ord('a'):
            self.character.position[0] -= speed
            print('left')
        if event.key == pygame.K_RIGHT or event.key == ord('d'):
            self.character.position[0] += speed
            print('right')
        if event.key == pygame.K_UP or event.key == ord('w'):
            self.character.position[1] -= speed
            print('up')
        if event.key == pygame.K_DOWN or event.key == ord('s'):
            self.character.position[1] += speed
            print('down')

    def stop_move(self, event):
        """
        Stops a character's movement, given a key release.

        Attributes:
            event: An event representing a player input.
        """
        pass


# test code down here


def movement_test():
    """
    Tests movement code with a test character.
    """
    pygame.init()  # initialize pygame
    map = spike_map()  # initialize map
    clock = pygame.time.Clock()  # to keep track of time in-game

    # create instances of classes
    character = character_model()  # include parentheses when creating instance
    view = character_view()
    controller = character_controller(character)

    # main loop
    run = True
    while run:
        # sense inputs (get events)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                run = False
            if event.type == pygame.KEYDOWN:  # check for a keypress
                # currently assuming all keypresses are movement related
                controller.move(event, 20)
            if event.type == pygame.KEYUP:
                controller.stop_move(event)
            # update states
            # create entities
            # detect interactions

        # update stuff
        map.fill_screen((120, 120, 120))  # make screen grey
        view.draw_sprite(map.window, character.position)
        pygame.display.flip()  # update entire display
        clock.tick(60)  # advance time, run game at 60 FPS

    pygame.quit()  # after main loop has finished
