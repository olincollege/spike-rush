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

    def __init__(self, x_0, y_0, x_dim, y_dim):
        self._color = (180, 180, 180) # random test color
        self._top = x_0
        self._left = y_0
        self._width = x_dim
        self._height = y_dim

    def initialize_zone(self, surface):
        pygame.draw.rect(surface, self._color,
            pygame.Rect(self._top, self._left, self._width, self._height))

    def in_zone(self, agent):
        if agent.location[0] < self._width:
            pass

class PlantZone(Zone):
    """
    Zone where the spike can be planted.
    """

class SpawnZone(Zone):
    """
    Zone where players can spawn.
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
