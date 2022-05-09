"""
Model, View, Controller architecture and functions for an Agent in spike rush
"""
# Pylint disables & justifications.

# This warning has to be disabled becuase it doesn't make any sense
# the Agent must store its attributes and there isn't a good way to make the
# Agent have less without making the code more convoluted
# pylint:disable=R0902

# There currently is no way to resolve for too many arguments without making
# the code significantly more convoluted & all of the arguments in question
# are currently being used.
# pylint:disable=R0913

# The high number of branches in the move function are due to the high
# number of potential key inputs and combinations that it handles.
# pylint:disable=R0912

# Disabled because all of the public functions are used and we have not
# yet properly learned private functions.
# pylint:disable=R0904

# pylint:disable=E1101
# Disabled because this is how keys are checked via pygame - it's not trying
# to access a K_[key] attribute from pygame.

# pylint:disable=W0611
# These have to be disabled because the type of is random meaning that it
# might think it's an unused class when it is not.

from abc import abstractmethod
import math
import os
import pygame
from guns_bullets import Bullet, Classic, Spectre, Guardian, Vandal, gun_list
from spike import Spike

FRAME_RATE = 30


class Agent:
    """
    An agent in the spike rush game.

    Attributes:
        _location: A list containing integers representing the x and y position
            of the Agent.
        _health: An integer representing the current health of the agent.
        _color: A tuple containing 3 integers. Used for non sprite agents.
            Generally unused.
        _spike: A boolean representing whether the agent is currently carrying
            the spike or not.
        _spike_object: An instance of a Spike representing the spike planted by
            the agent.
        _side: A string representing whether the player is attacking or
            defending.
        frames_since_last_shot: An integer representing the number of frames
            since the player last shot a weapon.
        _gun: A class representing the type of gun the player is holding.
            The specific class will be some arbitrary class inherited from the
            general gun class.
        frames_since_reload: An integer representing the number of frames
            since the player started a reload.
        frames_since_last_spike_interaction: An integer representing the number
            of frames since the player started a spike interaction.
        is_shooting: A boolean representing whether or not a player is
            currently shooting.
        is_reloading: A boolean representing whether or not a player is
            currently reloading.
        _angle = An integer or float representing the angle the player is
            looking in radians.
        _turn_speed: A float representing how much to update the player angle
            each time an angle update is qeued.
        _alive: A boolean representing whether or not the player is alive.
        _win: a boolean representing if a player has won
    """
    _health = 100
    _color = (192, 192, 192)   # Default circle is gray
    _spike = True  # If spike is true, it has not yet been planted
    _spike_object = None

    frames_since_last_shot = 0
    frames_since_reload = 0

    frames_since_last_spike_interaction = 0

    is_shooting = False
    is_reloading = False
    #self.is_defusing = False

    _turn_speed = .15*FRAME_RATE/30
    _angle = 0

    # player starts as alive
    _alive = True
    _win = False

    #self._abilities = []

    def __init__(self, x_init, y_init, side):
        """
        Creates an instance of an agent.
        """
        self._location = [x_init, y_init]

        self._side = side
        self._gun = Vandal()

    @property
    def health(self):
        """
        Returns the agent's heatlh.

        Returns: An integer representing the agent's current health.
        """
        return self._health

    @property
    def win(self):
        """
        Return if an agent has won

        Returns:
            _win: a boolean representing if a player has won.

        """

        return self._win

    @property
    def location(self):
        """
        Returns the agent's location.

        Returns: A list containing the x & y coordinates of the agent.
        """
        return self._location

    @property
    def angle(self):
        """
        Returns the agent's shooting angle.

        Returns:
            A float representing the shooting angle of an agent in radians.
        """
        return self._angle

    @property
    def spike(self):
        """
        Returns true if the agent is currently holding the spike;
        otherwise, false.

        Returns:
            A boolean representing whether the player is holding the spike.
        """
        return self._spike

    @property
    def spike_object(self):
        """
        Returns the spike object that has been planted by the agent;
        returns None if the agent has not planted a spike.

        Returns:
            A Spike representing a Spike that has been planted.
        """
        return self._spike_object

    @property
    def gun(self):
        """
        Returns the agent's gun object.

        Returns:
            The specific instance of a player's gun object.
        """
        return self._gun

    @property
    def side(self):
        """
        Return what side the agent is currently playing.

        Returns:
            A string representing what side the agent is on.
        """
        return self._side

    @property
    def alive(self):
        """
        Returns the alive or dead status of the player.

        Returns:
            A boolean representing whether a player is alive or dead.
        """
        return self._alive

    @property
    def turn_speed(self):
        """
        Returns the agent's turn speed.

        Returns:
            An integer representing the agent's turning speed.
        """
        return self._turn_speed

    def set_location(self, x_position, y_position):
        """
        Updates the agent's location on the map to a new position.

        Args:
            x_position: An integer representing the x coordinate of the agent's
                new position.
            y_position: An integer representing the y coordinate of the agent's
                new position.
        Returns:
            None.
        """
        # Not abstract bc all of them move the same
        self._location = [x_position, y_position]

    def set_win(self):
        """
        Set a player's win status to True
        """
        self._win = True

    def set_x_coord(self, x_position):
        """
        Updates the agent's x coordinate on the map to a new position.

        Args:
            x_position: An integer representing the x coordinate of the agent's
                new position.
        Returns:
            None.
        """
        self._location[0] = x_position

    def set_y_coord(self, y_position):
        """
        Updates the agent's y coordinate on the map to a new position.

        Args:
            y_position: An integer representing the y coordinate of the agent's
                new position.
        Returns:
            None.
        """
        self._location[1] = y_position

    def update_health(self, new_health):
        """
        Updates the agent's health.

        Args:
            new_health: An integer representing the agent's new health.
        Returns:
            None.
        """
        self._health = new_health

    def set_angle(self, angle):
        """
        Update the view angle of the player.

        Args:
            angle: an integer or float representing the new view angle.
        Returns:
            None.
        """
        self._angle = angle

    def kill(self):
        """
        Kill the player.

        Returns:
            None.
        """
        self._alive = False

    @abstractmethod
    def use_ultimate(self):
        """
        Uses the agent's ultimate ability; abstract method because it depends
        on the type of agent.

        Returns:
            None.
        """

    def use_gun(self):
        """
        Shoot a gun from the player's location, at the look angle.

        Returns:
            None.
        """
        self._gun.shoot(self.location[0], self.location[1], self._angle)

    def reload_gun(self):
        """
        Reload the player's gun.

        Returns:
            None.
        """
        # fix for private variable calls
        self._gun.update_clip(1)
        self.is_reloading = True
        self.frames_since_reload = 0

    def plant_spike(self):
        """
        Plants the spike by creating a new Spike obejct at the agent's current
        location.

        Returns:
            None.
        """
        self._spike = False
        self._spike_object = Spike(self.location[0], self.location[1])

    def set_spike_object(self, new_spike):
        """
        Sets the agent's Spike to a new Spike object; primarily used to reset
        the spike to None.

        Args:
            new_spike: The new spike for the Agent.
        Returns:
            None.
        """
        self._spike_object = new_spike


class Brimstone(Agent):
    """
    Brimmy w/o da stimmy
    """

    def __init__(self, x_init, y_init, side):
        Agent.__init__(self, x_init, y_init, side)
        self._name = "Brimstone"

    def use_ultimate(self):
        # Region of the map that does ~39 dps, lasts 15s,
        # takes 3s after fire to start damage
        pass


class Phoenix(Agent):
    """
    Trash in meta rn, but cool ult for spike rush
    """

    def __init__(self, x_init, y_init, side):
        Agent.__init__(self, x_init, y_init, side)
        self._name = "Phoenix"

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
        #saved_location = self._location

        self.update_health(100)


class Reyna(Agent):
    """
    Toxic instalocker
    """

    def __init__(self, x_init, y_init, side):
        Agent.__init__(self, x_init, y_init, side)
        self._name = "Reyna"

    def use_ultimate(self):
        """
        Uses Reyna's ultimate when the "X" key is pressed.

        Reyna's ultimate ability puts her into a 30s frenzy which increases her
        firing speed by 15% and increases her reload speed by 25%.
        """


class AgentView():
    """
    Displays an agent and other visuals controlled by the agent
    (bullets & the spike) on the map.

    Attributes:
        _agent: An Agent representing the model for the agent.
        agent_sprite: A string representing the image to use as the sprite for
            the agent.




    """
    _bullet_width = 6

    def __init__(self, agent_model, image_path):
        self._agent = agent_model
        self._img_path = image_path

        # Initialize the agent's sprite
        self.agent_sprite = pygame.sprite.Sprite()
        self.image = [os.path.join('image', 'sprites', self._img_path)]
        self.agent_sprite.image = \
            pygame.transform.scale(pygame.image.load(os.path.join(
                'images', 'sprites', self._img_path)).convert_alpha(),
                (50, 50))
        self.agent_sprite.rect = self.agent_sprite.image.get_rect()
        self.agent_sprite.rect.x = self._agent.location[0]
        self.agent_sprite.rect.y = self._agent.location[1]

    @property
    def agent(self):
        """
        Returns the view's agent.

        Returns:
            An Agent representing the agent that the view is for.
        """
        return self._agent

    def dot_sight(self, surface):
        """
        Displays a red dot next to the agent sprite indicating the
        direction the agent will currently shoot in.

        Args:
            surface: A Surface where the game takes place and all visuals are
                displayed.
        Returns:
            None.
        """
        # make a view a red dot sight
        dot_width = 6

        angle = self.agent.angle

        x_heading = math.cos(angle)
        y_heading = math.sin(angle)

        player_x = self.agent.location[0]
        player_y = self.agent.location[1]

        # x and y coordinates of the red dot sight
        dot_x = player_x + math.floor(60*x_heading) + 25
        dot_y = player_y + math.floor(60*y_heading) + 25

        red_dot = pygame.Rect(math.floor(dot_x - dot_width/2),
                              math.floor(dot_y + dot_width/2), \
                                  dot_width, dot_width)

        pygame.draw.rect(surface, (255, 0, 0), red_dot)

    def draw_agent(self, surface):
        """
        Displays the agent in the game.

        Args:
            surface: A Surface where the game takes place and all visuals are
                displayed.
        Returns:
            None.
        """
        self.agent_sprite.rect.x = self.agent.location[0]
        self.agent_sprite.rect.y = self.agent.location[1]

        # draw sprite on to surface
        surface.blit(self.agent_sprite.image, \
            (self.agent_sprite.rect))

    def draw_bullets(self, surface):
        """
        Displays bullets in the game.

        Args:
            surface: A Surface where the game takes place and all visuals are
                displayed.
        Returns:
            None.
        """
        #global bullet_dictionary
        for the_bullet in self._agent.gun.bullet_dict.values():
            bullet_sprite = pygame.sprite.Sprite()
            bullet_sprite.image = pygame.Surface(
                (self._bullet_width, self._bullet_width))
            bullet_sprite.image.fill((0, 0, 0))
            bullet_x = math.floor(the_bullet.pos_x - self._bullet_width/2)
            bullet_y = math.floor(the_bullet.pos_y + self._bullet_width/2)
            bullet_sprite.rect = pygame.Rect(
                bullet_x, bullet_y, self._bullet_width, self._bullet_width)
            # self._bullet_sprites.add(bullet_sprite)
            the_bullet.set_sprite(bullet_sprite)
            surface.blit(bullet_sprite.image, bullet_sprite.rect)

            #pygame.draw.rect(surface, (0, 0, 0), bullet_rectangle)
    def draw_spike(self, surface):
        """
        Displays the Spike on the map only after it has been planted.

        surface: A Surface where the game takes place and all visuals are
                displayed.
        Returns:
            None.
        """
        spike = self._agent.spike_object
        if spike is not None:
            spike_width = 20
            spike_sprite = pygame.sprite.Sprite()
            spike_sprite.image = pygame.Surface((spike_width, spike_width))
            spike_sprite.image.fill((100, 100, 100))
            spike_sprite.rect = pygame.Rect(
                self._agent.spike_object.location[0],
                self._agent.spike_object.location[1], spike_width, spike_width)

            surface.blit(spike_sprite.image, spike_sprite.rect)


class AgentController:
    """
    Controls an agent on the map.

    Attributes:
        _agent: An Agent representing the model for the agent.
        _view: An AgentView representing the view for the agent.
    """

    def __init__(self, agent, view):
        """
        Initialize an instance of the AgentController class
        """
        self._agent = agent
        self._view = view

    @property
    def agent(self):
        """
        Return the controller's agent.

        Returns:
            _agent: An instance of the Agent class.
        """
        return self._agent

    @property
    def view(self):
        """
        Return the controller's view.

        Returns:
            _view: An instance of the AgentView class.

        """
        return self._view

    def move(self, speed, keys, input_type, walls):
        """
        Moves the character through the map. Detects pressed keys and moves
        the character correspondingly. Also detects collisions with walls and
        prevents character movement

        Arguments:
            speed: An integer representing the number of pixels a character
            moves per frame.
            keys: A list containing which keys are currently pressed.
            input_type: A string representing which set of controls will be
            used.
            walls: A sprite group of all walls on the map.
        """
        current_pos = self.agent.location
        xchange = 0
        ychange = 0
        control_list = []

        # up, down, left, right
        if input_type == "WASD":
            control_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,
                            pygame.K_c, pygame.K_v]

        if input_type == "Arrow":
            control_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,
                            pygame.K_RIGHT, pygame.K_COMMA,
                            pygame.K_PERIOD]

        # searches for arrow keys and WASD
        if keys[control_list[2]]:  # left
            xchange = -speed
            self.agent.set_x_coord(current_pos[0]-speed)
            self._view.agent_sprite.rect.x = self.agent.location[0]

        if keys[control_list[3]]:  # right
            xchange = speed
            self.agent.set_x_coord(current_pos[0]+speed)
            self._view.agent_sprite.rect.x = self.agent.location[0]

        if keys[control_list[5]]:  # turn counter clockwise
            theta_change = self.agent.turn_speed
            self.agent.set_angle(self.agent.angle + theta_change)

        if keys[control_list[4]]:  # turn counter clockwise
            theta_change = self.agent.turn_speed
            self.agent.set_angle(self.agent.angle - theta_change)

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view.agent_sprite, walls, False)
        for the_walls in collision_list:
            # reset position
            if xchange > 0:
                self._view.agent_sprite.rect.right = the_walls.rect.left
                self.agent.location[0] = self._view.agent_sprite.rect.left
            elif xchange < 0:
                self._view.agent_sprite.rect.left = the_walls.rect.right
                self.agent.location[0] = self._view.agent_sprite.rect.left

        if keys[control_list[0]]:  # up
            ychange = -speed
            self.agent.set_y_coord(current_pos[1]-speed)
            self._view.agent_sprite.rect.y = self.agent.location[1]

        if keys[control_list[1]]:  # down
            ychange = speed
            self.agent.set_y_coord(current_pos[1]+speed)
            self._view.agent_sprite.rect.y = self.agent.location[1]

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view.agent_sprite, walls, False)
        for the_wall in collision_list:
            # reset position
            if ychange > 0:
                self._view.agent_sprite.rect.bottom = the_wall.rect.top
                self.agent.location[1] = self._view.agent_sprite.rect.top
            elif ychange < 0:
                self._view.agent_sprite.rect.top = the_wall.rect.bottom
                self.agent.location[1] = self._view.agent_sprite.rect.top

    # gun controls
    def check_shoot(self, keys, input_type):
        """
        Checks if a player should be shooting a gun and if so, begin shooting.

        Args:
            keys: A list containing which keys are currently pressed.
            input_type: A string representing which set of controls will be
            used.
        Returns:
            None.
        """

        # if reloading, don't fire
        if self.agent.frames_since_reload < self.agent.gun.frames_for_reload \
                and self.agent.is_reloading:
            self.agent.gun.consective_bullets = 0
            return
        if self.agent.is_reloading:
            self.agent.setis_reloading(False)
            # print("reloaded")

        self.agent.frames_since_last_shot += 1
        # consecutive fire

        if (input_type == "WASD" and keys[pygame.K_x]) or \
            (input_type == "Arrow" and keys[pygame.K_m]):

            if self.agent.is_shooting and not self.agent.gun.automatic:
                return

            if self.agent.frames_since_last_shot < \
                    self.agent.gun.frames_before_shot:
                return

            # if the weapon is semi auto, don't shoot it automatically

            if self.agent.gun.current_clip > 0:
                # If no bullets, pass
                self.agent.use_gun()

              # automatic fire activation
            # if self.agent.gun.automatic:
                if self.agent.is_shooting:
                    self.agent.gun.consecutive_bullets += 1
                else:
                    self.agent.gun.consecutive_bullets = 1

                # print(self.agent._gun.consecutive_bullets)
                self.agent.is_shooting = True

                self.agent.frames_since_last_shot = 0

                # automatic fire activation
            else:
                self.agent.gun.consecutive_bullets = 0
                self.agent.is_shooting = False

        else:

            if self.agent.gun.automatic:
                self.agent.gun.consecutive_bullets = 0

            elif not self.agent.gun.automatic and\
                self.agent.frames_since_last_shot > \
                    self.agent.gun.frames_before_shot + 8:
                self.agent.gun.consecutive_bullets = 0
            self.agent.is_shooting = False

            self.agent.gun.consecutive_bullets = 0

    def check_reload(self, keys, input_type):
        """
        Reloads the agent's gun when the key to reload is pressed.

        Args:
            keys: A list containing which keys are currently pressed.
            input_type: A string representing which set of controls will be
            used.
        Returns:
            None.
        """
        if input_type == "Arrow" and keys[pygame.K_l]:

            self.agent.reload_gun()

        if input_type == "WASD" and keys[pygame.K_r]:

            self.agent.reload_gun()

        if self.agent.is_reloading:
            self.agent.frames_since_reload += 1

    # bullet controlls

    def update_bullets_test(self, walls, players, other_agent):
        """
        Goes through the agent's gun's dictionary of bullets and updates
        the position for all of them.

        Args:
            walls: A sprite group of all of the walls on the map.
            players: A sprite group of agents present in the current game.
            other_agent: An Agent model that is on the opposite side as the one
                this controller is for.

        Returns: None.
        """
        for the_bullet in self._agent.gun.bullet_dict.values():
            self.bullet_main(the_bullet, walls, players, other_agent)
        # actually delete the bullet
        for bullet_name in self._agent.gun.bullet_delete_dict.keys():
            del self._agent.gun.bullet_dict[bullet_name]
        self._agent.gun.bullet_delete_dict.clear()

    def bullet_collision(self, the_bullet, walls, players, other_agent):
        """
        Checks whether a bullet of them collides with walls or other players.

        If the bullets collide with walls, they are deleted; if they collide
        with players, the players' health is reduced.

        Args:
            bullet: A bullet to check the collisions for
            walls: A sprite group of all of the walls on the map.
            players: A sprite group of agents present in the current game.
            other_agent: An Agent model that is on the opposite side as the one
                this controller is for.
        Returns:
            None.
        """
        if the_bullet.bullet_sprite is not None:
            wall_collision_list = \
                pygame.sprite.spritecollide(the_bullet.bullet_sprite,
                                            walls, False)
            agent_collision_list = \
                pygame.sprite.spritecollide(
                    the_bullet.bullet_sprite, players, False)
            for _ in wall_collision_list:
                self._agent.gun.delete_bullet(the_bullet)
            for _ in agent_collision_list:
                # the way this is implemented will not work in 2+v2+ games
                self._agent.gun.delete_bullet(the_bullet)
                other_agent.update_health(other_agent.health - 10)
                # switch 10 to bullet.damage

                if other_agent.health <= 0:
                    other_agent.kill()

    def bullet_main(self, bullet, walls, players, other_agent):
        """
        Updates the position of a single bullet and then checks if it
        collides with any objcts.

        Args:
            bullet: A bullet to check the collisions for
            walls: A sprite group of all of the walls on the map.
            players: A sprite group of agents present in the current game.
            other_agent: An Agent model that is on the opposite side as the one
                this controller is for.
        Returns:
            None.
        """
        bullet.update_position()
        self.bullet_collision(bullet, walls, players, other_agent)

    def spike_plant(self, keys, map_model, input_type, hud_model):
        """
        Checks if the spike can be planted & then plants it.

        Preconditions to planting include being in the plant zone, holding the
        plant key for four seconds, and being on the attacking side.

        Args:
            keys: A list containing which keys are currently pressed.
            map_model: A Spike Map representing the map which the game is
                currently being played on.
            input_type: A string representing which set of controls will be
            used.
            hud_model:  A Hud representing the hud of the current game.
        Returns:
            None.
        """
        frames_to_plant = 125  # 4 seconds @ 30 fps
        if self._agent.side != "attack":
            return
        if map_model.a_site.in_zone(self._agent):
            if (input_type == "WASD" and keys[pygame.K_4] or
                    input_type == "Arrow" and keys[pygame.K_SEMICOLON]):
                if self._agent.spike and\
                    self._agent.frames_since_last_spike_interaction == \
                        frames_to_plant:
                    # print("Planted")
                    self._agent.plant_spike()
                    hud_model.set_timer(45)
                elif self._agent.spike:
                    self._agent.frames_since_last_spike_interaction += 1
            else:
                self._agent.frames_since_last_spike_interaction = 0

    def spike_defuse(self, keys, map_model, input_type, other_agent, hud_model):
        """
        Checks if the spike can be defused & defuses it.

        Preconditions to defusing include a Spike existing on the map,
        the agent being within a certain range of the Spike, holding the defuse
        key for seven seconds, and being on the defending side.

        Args:
            keys: A list containing which keys are currently pressed.
            map_model: A Spike Map representing the map which the game is
                currently being played on.
            input_type: A string representing which set of controls will be
            used.
            other_agent: An Agent model that is on the opposite side as the one
                this controller is for.
            hud_model: A Hud representing the hud of the current game.
        Returns:
            None.
        """
        if self._agent.side != "defense":
            return
        frames_to_defuse = 225  # 7 seconds @ 30 fps
        spike = other_agent.spike_object

        if spike is not None and \
                map_model.a_site.within_defuse_range(self._agent, spike):
            if (input_type == "WASD" and keys[pygame.K_4] or
               input_type == "Arrow" and keys[pygame.K_SEMICOLON]):
                if not spike.status and \
                        self._agent.frames_since_last_spike_interaction == \
                        frames_to_defuse and spike.frames_since_plant < \
                        spike.frames_to_explode:
                    # print("Defused")
                    defuse_spike(other_agent.spike_object)
                    hud_model.set_timer(0)
                    other_agent.set_spike_object(None)
                elif not spike.status:
                    self._agent.frames_since_last_spike_interaction += 1
            else:
                self._agent.frames_since_last_spike_interaction = 0

def defuse_spike(spike):
    """
    Defuses a the given Spike object.

    Args:
        spike: A spike representing the spike on the map to defuse.
    Returns:
        None.
    """
    spike.defuse()

def check_win(attacker, defender, hud_model):
    """
    Checks if either of the players has won and updates their
    attributes accordingly

    Args:
        attacker: an instance of the agent class representing the attacking
            player
        defender: an instance of the agent class representing the defending
            player
        hud_model: an instance of the HUD containing the game timer

    """

    spike_out = not attacker.spike

    # if the spike hasn't been planted
    if not spike_out:

        # if the defender dies
        if not defender.alive:
            attacker.set_win()
        if not attacker.alive:
            defender.set_win()

        # PUT HERE
        # if the timer runs out, defender wins
        if hud_model.timer == 0:
            defender.set_win()

    # if the spike has been planted
    else:

        if attacker.spike_object is not None:
            # if the spike blows up
            if hud_model.timer == 0:
                attacker.set_win()

            # if the spike is defused

            if attacker.spike_object.status:
                defender.set_win()

        # if defender dies while spike out
        if not defender.alive:
            attacker.set_win()
