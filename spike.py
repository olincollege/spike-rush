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
    
    def countdown(self):
        if self._status == False:
            # Start subtracting from timer at each second
            # If timer hits 0, go boom
            pass
    
    def blowup(self):
        if self._status == False and self._timer == 0:
            pass

    def defuse(self):
        self._status = True


