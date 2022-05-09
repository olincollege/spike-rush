"""
Various zones on the map including spawn, plant, and AOE areas.
"""
# Pylint disables & justifications.

# pylint:disable=R0913
# Reasonable number of arguments used for this function given the
# number of dimensions being kept track of. Furthermore, modifying
# this would result in an objectively more convoluted solution.
from random import randint


class Zone:
    """
    Model for a zone on the map.

    Attributes:
        _left: An integer representing the left bound of the zone.
        _top: An integer representing the top bound of the zone.
        _width: An integer represending the width of the zone.
        _height: An integer representing the height of the zone.
        _type: A string containing the name of the type of zone.
    """

    def __init__(self, x_0, y_0, x_dim, y_dim, form):
        self._left = x_0
        self._top = y_0
        self._width = x_dim
        self._height = y_dim
        self._type = form

    @property
    def get_type(self):
        """
        Returns the type of zone.

        Returns:
            A string representing the type of zone.
        """
        return self._type

    def in_zone(self, agent):
        """
        Determines whether a given agent is in the zone or not.

        Args:
            agent: An Agent model representing the agent to check the location
                of.
        Returns:
            True if the agent is in the zone; otherwise, False.
        """
        return agent.location[0] > self._left


class SpawnZone(Zone):
    """
    Zone where players can spawn.
    """

    def __init__(self, x_0, y_0, x_dim, y_dim):
        Zone.__init__(self, x_0, y_0, x_dim, y_dim, "spawn")

    def set_spawns(self, agents):
        """
        Sets the spawn locations of the agents randomly within the spawn zones.

        Args:
            Agents: A list of Agents to generate spawn locations for.
        Returns:
            None.
        """
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
        """
        Determines whether the given agent is within a defusal range of the
        given spike.

        Args:
            agent: An Agent model representing the agent attempting to defuse.
            spike: A Spike model representing the location of the planted
                spike.
        Returns:
            True if the agent is within defusal range; otherwise, False.
        """
        return self.in_zone(agent) and agent.location[0] < \
            spike.location[0]+50 and agent.location[0] > \
            spike.location[0]-50 and agent.location[1] < \
            spike.location[1]+50 and agent.location[1] > \
            spike.location[1]-50


class DamageZone(Zone):
    """
    Zone where players take damage
    """

    def __init__(self, x_0, y_0, x_dim, y_dim):
        Zone.__init__(self, x_0, y_0, x_dim, y_dim, "damage")

    def damage_agents(self, agents):
        """
        Damages all given agents if they are in the zone.

        Args:
            agents: A list of all of the agents currently in the game.
        Returns:
            None.
        """
        # Incomplete implementation; for "future implementation"
        for agent in agents:
            # temporary health loss only 10 dmg
            if self.in_zone(agent):
                agent.update_health(agent.health-10)
