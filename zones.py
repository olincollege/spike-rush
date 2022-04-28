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
        self._top_left = [x_0, y_0]
        self._width = x_dim
        self._height = y_dim

    def initialize_zone(self):
        pass

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
    