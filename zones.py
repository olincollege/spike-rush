"""
Various zones on the map including spawn, plant, and AOE areas.
"""
import pygame
import os
from agent import *

class Zone:
    """
    Class docstring
    """

    def __init__(self,x_0, y_0, x_dim, y_dim):
        self._color = (180, 180, 180) # random test color
        self._top = x_0
        self._left = y_0
        self._width = x_dim
        self._height = y_dim

        self._area = pygame.Surface([self._width, self._height])

        # set wall spawn coordinates to xpos and ypos
        self.rect = self._area.get_rect()
        self.rect.x = x_0
        self.rect.y = y_0

    def in_zone(self, agent):
        if agent.location[0] < self._width:
            pass

class SpawnZone(Zone):
    """
    Zone where players can spawn.
    """
    def __init__(self):
        Zone.__init__(self, )

class PlantZone(Zone):
    """
    Zone where the spike can be planted.
    """

class DamageZone(Zone):
    """
    Zone where players take damage
    """

    def damage_agents(self, agents):
        """
        agents = list of all agents currently in the game
        """
        for agent in agents:
            # temporary health loss only 10 dmg
            agent.update_health(agent.health-10)
