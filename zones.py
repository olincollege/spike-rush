"""
Various zones on the map including spawn, plant, and AOE areas.
"""
import pygame
import os
from agent import *
from random import randint


class Zone:
    """
    Class docstring
    """

    def __init__(self, x_0, y_0, x_dim, y_dim, type):
        self._color = (180, 180, 180)  # random test color
        self._left = x_0
        self._top = y_0
        self._width = x_dim
        self._height = y_dim
        self._type = type

        self._area = pygame.Surface([self._width, self._height])

        # set wall spawn coordinates to xpos and ypos
        self.rect = self._area.get_rect()
        self.rect.x = x_0
        self.rect.y = y_0

    @property
    def get_type(self):
        return self._type

    def in_zone(self, agent):
        return agent.location[0] > self._left


class SpawnZone(Zone):
    """
    Zone where players can spawn.
    """

    def __init__(self, x_0, y_0, x_dim, y_dim):
        Zone.__init__(self, x_0, y_0, x_dim, y_dim, "spawn")

    def set_spawns(self, agents):
        for agent in agents:
            spawn_x = randint(self._left+50,
                              self._left+self._width-50)
            spawn_y = randint(self._top+50,
                              self._top+self._height-50)
            agent.set_location(spawn_x, spawn_y)


class PlantZone(Zone):
    """
    Zone where the spike can be planted.
    """

    def __init__(self, x_0, y_0, x_dim, y_dim):
        Zone.__init__(self, x_0, y_0, x_dim, y_dim, "plant")

    def within_defuse_range(self, agent, spike):
        return agent.location[0] < spike.location[0]+50 and \
            agent.location[0] > spike.location[0]-50 and \
            agent.location[1] < spike.location[1]+50 and \
            agent.location[1] > spike.location[1]-50


class DamageZone(Zone):
    """
    Zone where players take damage
    """

    def __init__(self, x_0, y_0, x_dim, y_dim):
        Zone.__init__(self, x_0, y_0, x_dim, y_dim, "damage")

    def damage_agents(self, agents):
        """
        agents = list of all agents currently in the game
        """
        for agent in agents:
            # temporary health loss only 10 dmg
            agent.update_health(agent.health-10)
