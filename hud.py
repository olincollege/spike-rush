"""
Creates heads-up display (HUD) elements to represent the status of the game and
players.
"""

import pygame


class DisplayModel:
    """
    Tracks various attributes to be displayed in game.

    Attributes:
        _font: the pygame font to be used in the HUD
        _timer: An integer representing the seconds remaining in the game
    """

    def __init__(self):
        self._font = pygame.font.SysFont(
            'bahnschrift', 50)  # looks like Valorant HUD font
        self._timer = 100  # start at 100 seconds

    @property
    def timer(self):
        """
        Returns the current value of the timer.

        Returns:
            An integer representing the current value of the timer.
        """
        return self._timer

    @property
    def font(self):
        """
        Returns the font used in the HUD.

        Returns: The font used in the HUD.
        """
        return self._font

    def set_timer(self, new_time):
        """
        Sets the timer's value to a new time.

        Args:
            new_time: An integer representing the new time.
        Returns:
            None.
        """
        self._timer = new_time


class DisplayView:
    """
    Displays HUD elements on to the game.

    Attributes:
        model: Attributes from the hud_model class.
    """

    def __init__(self, model):
        self.model = model  # from hud_model

    def draw_text(self, text, color, surface, position):
        """
        Draws the specified text on the screen.

        Arguments:
            text: A string representing the text to be drawn on the screen.
            color: A tuple representing the RGB values of the text color.
            surface: The surface to blit the text on to.
            position: A tuple representing the position of the text.
        """
        text_surface = self.model.font.render(text, 1, color)
        surface.blit(text_surface, position)

    def draw_player_updates(self, player_1, player_2, surface):
        """
        pull health/ammo updates from a specified player and draw it to the HUD.

        Arguments:
            player_1: An Agent to pull updates from.
            player_2: An Agent to pull updates from.
            surface: The surface to blit the text on to.
        """
        # pull & draw player 1 health update
        health_1 = player_1.health
        if player_1.health < 0:
            self.draw_text("0", (255, 255, 255), surface, (230, 800))
        else:
            self.draw_text(str(health_1), (255, 255, 255), surface, (230, 800))
        # pull & draw player 1 ammo update
        # pull ammo here
        ammo_1 = player_1.gun.current_clip
        self.draw_text(str(ammo_1), (255, 255, 255), surface, (400, 800))

        # pull & draw player 2 health update
        health_2 = player_2.health
        if player_2.health < 0:
            self.draw_text("0", (255, 255, 255), surface, (1238, 800))
        else:
            self.draw_text(str(health_2), (255, 255, 255),
                           surface, (1238, 800))
        # pull & draw player 2 ammo update
        # pull ammo here
        ammo_2 = player_2.gun.current_clip
        self.draw_text(str(ammo_2), (255, 255, 255), surface, (1412, 800))

    def draw_game_timer(self, surface):
        """
        Draws the current time of the game.

        Arguments:
            surface: The surface to blit the text on to.
        """
        self.draw_text(str(self.model.timer),
                       (255, 255, 255), surface, (800, 800))
