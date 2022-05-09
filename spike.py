"""
Docstring
"""
import pygame


class Spike:
    """
    Spike/bomb; created only when the plant spike method is called by an agent.
    """

    def __init__(self, x_loc, y_loc):
        self._location = [x_loc, y_loc]
        self._status = False    # False means planted, True means defused
        self._timer = 45    # 45 seconds until spike go boom

        self.frames_to_explode = 125  # 1100 # 45 seconds @ 30fps
        self.frames_since_plant = 0

    @property
    def location(self):
        return self._location

    @property
    def status(self):
        return self._status

    def blowup(self):
        if self.frames_since_plant == self.frames_to_explode:
            return True

    def defuse(self):
        self._status = True
        self.frames_since_plant = 0
