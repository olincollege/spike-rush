"""
Model for the Spike.
"""

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
        """
        Returns the location of the Spike.

        Returns:
            A string of integers representing the Spike's location.
        """
        return self._location

    @property
    def status(self):
        """
        Returns the status of the Spike.

        Returns:
            A boolean representing whether the spike has been planted or not.
            True if defused; otherwise, False.
        """
        return self._status

    def blowup(self):
        """
        Returns whether the Spike reaches an explotion.

        Returns:
            A boolean representing whether the Spike explodes.
            True if it explodes; otherwise, False.
        """
        return self.frames_since_plant == self.frames_to_explode

    def set_status(self, new_status):
        """
        Sets a new status of the bomb.

        Args:
            new_status = A boolean representing the updated status of the
                spike.
        Returns:
            None.
        """
        self._status = new_status

    def defuse(self):
        """
        Defuses the spike.

        Returns:
            None.
        """
        self._status = True
        self.frames_since_plant = 0
