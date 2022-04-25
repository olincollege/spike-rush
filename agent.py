"""
Docstring >:)
"""

import pygame
from regex import E
from players_guns_bullets import *
from game_map import *
from abc import ABC, abstractmethod

class Agent:
    """
    Class docstring
    """
    def __init__(self, x_init, y_init, agent_name):
        self._location = [x_init, y_init]
        self._current_health = 100
        self._gun = gun(x_init, y_init)
        self._speed = 10
        self._color = (192, 192, 192)   # Default circle is gray

        #self._character_token = []
        #self._abilities = []
        #self._name = []

    @property
    def health(self):
        """
        Returns the agent's heatlh.

        Returns: An integer representing the agent's current health.
        """
        return self._health
    
    @property
    def location(self):
        """
        Returns the agent's location.

        Returns: A list containing the x & y coordinates of the agent.
        """
        return self._location

    def move(self, x_position, y_position):
        """
        Go brr
        """
        # Not abstract bc all of them move the same
        self._location = [x_position, y_position]

    def update_health(self, new_health):
        self._health = new_health

    @abstractmethod
    def use_ultimate(self):
        pass

    def use_gun(self):
        """
        Pew pew
        """
        self._gun.shoot()
    
    def reload_gun(self):
        # Pass until reload gun method is defined
        pass

    def pickup_orb(self):
        # Only implementing if time
        pass


class Brimstone(Agent):
    """
    Brimmy w/o da stimmy
    """
    
    def __init__(self):
        self._name = "Brimstone"
        self._color = (185, 147, 104)

        # Generate character token
        # Gray circle

    def use_ultimate(self):
        # Region of the map that does ~39 dps, lasts 15s, 
        # takes 3s after fire to start damage
        pass


class Phoenix(Agent):
    """
    Trash in meta rn, but cool ult for spike rush
    """

    def __init__(self):
        self._name = "Phoenix"

        # Generate character token
        # orange circle
    
    def use_ultimate(self):
        """
        Uses Phoenix's ultimate when the "X" key is pressed.

        Phoenix's ultimate ability saves his location on the X key being
        pressed & leaves a marker there. After 10 seconds (or when he is
        killed, if that happens sooner), he returns to the marked location
        at full health.
        """
        # Save Phoenix's location on press
        # After 10s or when killed, returns to location w full health

        self.update_health(100)

class Reyna(Agent):
    """
    Toxic instalocker
    """

    def __init__(self):
        self._name = "Reyna"

        # Generate character token
        # Purple circle

    def use_ultimate(self):
        """
        Uses Reyna's ultimate when the "X" key is pressed.

        Reyna's ultimate ability puts her into a 30s frenzy which increases her
        firing speed by 15% and increases her reload speed by 25%.
        """
        pass
    