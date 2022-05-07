"""
Docstring >:)
"""

import pygame
import os
from regex import E
from guns_bullets import *
from test_map import *
from abc import ABC, abstractmethod
from spike import *
from spike_map import *
import math

class Agent:
    """
    An agent in the spike rush game.    

    Attributes:
        location:
        current_health:
        color: 
        spike: A boolean representing whether the agent is currently carrying
            the spike or not.

    """
    def __init__(self, x_init, y_init):
        """
        Creates an instance of an agent.
        """
        self._location = [x_init, y_init]
        self._health = 100
        self._gun = gun()
        self._color = (192, 192, 192)   # Default circle is gray
        self._spike = True # If spike is true, it has not yet been planted
        # self._sprite = None

        self._frames_since_last_shot = 0
        self._frames_since_reload = 0
        
        self._is_shooting = False
        self._is_reloading = False

        #self._abilities = []

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

    @property
    def spike(self):
        """
        Returns true if the agent is currently holding the spike;
        otherwise, false.
        """
        return self._spike

    @property
    def gun(self):
      return self._gun

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

    def set_frames_since_last_shot(self, new_frames):
      self._frames_since_last_shot = new_frames

    def set_frames_since_reload(self, new_frames):
      self._frames_since_reload = new_frames

    def set_is_shooting(self, bool):
      self._is_shooting = bool

    def set_is_reloading(self, bool):
      self._is_reloading = bool

    @abstractmethod
    def use_ultimate(self):
        """
        Not implemented [yet].
        """
        pass

    def use_gun(self, mouse_x, mouse_y):
      self._gun.shoot(self.location[0], self.location[1], mouse_x, mouse_y)

    def reload_gun(self):
      # fix for private variable calls
      self._gun.update_clip(1)
      self._is_reloading = True
      self._frames_since_reload = 0

    def plant_spike(self, map_model):
        """
        aaa

        Returns:
            None.
        """
        # 4 seconds to plant
        if self._spike: # add that it must be in a plant zone
            # create new spike object @ current location
            pass
            
    def defuse_spike(self, spike):
        """
        aaa

        Args:
            spike: The spike object being defused.
        Returns:
            None.
        """
        # 3.5 seconds to half; 7 seconds to defuse fully
        spike.defuse()

    def pickup_orb(self):
        """
        Not implementing [yet]
        """
        # Only implementing if time
        pass


class Brimstone(Agent):
    """
    Brimmy w/o da stimmy
    """
    
    def __init__(self):
        self._name = "Brimstone"
        self._color = (185, 147, 104)
        self._sprite = "" 

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
        self._sprite = ""
   
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
        saved_location = self._location
        
        self.update_health(100)

class Reyna(Agent):
    """
    Toxic instalocker
    """

    def __init__(self):
        self._name = "Reyna"
        self._sprite = ""

    def use_ultimate(self):
        """
        Uses Reyna's ultimate when the "X" key is pressed.

        Reyna's ultimate ability puts her into a 30s frenzy which increases her
        firing speed by 15% and increases her reload speed by 25%.
        """
        pass
    
class AgentView():
    """
    Displays an agent on the map.
    """
    bullet_width = 6

    def __init__(self, agent):
        self._agent = agent

        #self._sprite = self._agent._sprite

        # initiate sprite stuff
        pygame.sprite.Sprite.__init__(self)  # initiate pygame sprite
        # image for sprite representation
        self._sprites = [os.path.join('images', 'sprites', 'test_sprite.png')]
        # currently only using one image, scaling size down
        self._sprite = \
            pygame.transform.scale(pygame.image.load(os.path.join(
                'images', 'sprites', 'test_sprite.png')).convert_alpha(),
                (50, 50))
        self.rect = self._sprite.get_rect()
        self.rect.x = self._agent.location[0]
        self.rect.y = self._agent.location[1]


    @property
    def agent(self):
        return self._agent

    def draw_agent(self, surface):
        self.rect.x = self.agent.location[0]
        self.rect.y = self.agent.location[1]

        # draw sprite on to surface
        surface.blit(self._sprite, (self.rect.x, self.rect.y))

    def draw_bullets(self, surface):
      global bullet_dictionary
      for bullet in bullet_dictionary.values():
        bullet_rectangle = pygame.Rect(math.floor(bullet.pos_x - self.bullet_width/2), \
                                      math.floor(bullet.pos_y + self.bullet_width/2), \
                                       self.bullet_width, self.bullet_width)
        pygame.draw.rect(surface, (0, 0, 0), bullet_rectangle)
    

class AgentController: 
    """
    Controls an agent on the map.
    """

    def __init__(self, agent, view):
        self._agent = agent
        self._view = view

    @property
    def agent(self):
        return self._agent

    @property
    def view(self):
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
            control_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]

        if input_type == "Arrow":
            control_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,
                            pygame.K_RIGHT]

        # searches for arrow keys and WASD
        if keys[control_list[2]]:  # left
            xchange = -speed
            self.agent.set_x_coord(current_pos[0]-speed)
            self._view.rect.x = self.agent.location[0]

        if keys[control_list[3]]:  # right
            xchange = speed
            self.agent.set_x_coord(current_pos[0]+speed)
            self._view.rect.x = self.agent.location[0]

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view, walls, False)
        for wall in collision_list:
            # reset position
            if xchange > 0:
                self._view.rect.right = wall.rect.left
                self.agent.location[0] = self._view.rect.left
            elif xchange < 0:
                self._view.rect.left = wall.rect.right
                self.agent.location[0] = self._view.rect.left

        if keys[control_list[0]]:  # up
            ychange = -speed
            self.agent.set_y_coord(current_pos[1]-speed)
            self._view.rect.y = self.agent.location[1]

        if keys[control_list[1]]:  # down
            ychange = speed
            self.agent.set_y_coord(current_pos[1]+speed)
            self._view.rect.y = self.agent.location[1]

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view, walls, False)
        for wall in collision_list:
            # reset position
            if ychange > 0:
                self._view.rect.bottom = wall.rect.top
                self.agent.location[1] = self._view.rect.top
            elif ychange < 0:
                self._view.rect.top = wall.rect.bottom
                self.agent.location[1] = self._view.rect.top
              
    # gun controls
    def check_shoot(self, keys):
        """
        aaa
        """
        #if reloading, don't fire
        if self.agent._frames_since_reload < self.agent.gun.frames_for_reload \
      and self.agent._is_reloading:
          return
        elif self.agent._is_reloading:
            self.agent.set_is_reloading(False)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if keys[pygame.K_z]:
          # self.agent._frames_since_last_shot >= \
          #self.agent.gun.frames_before_shot and 
          if self.agent.gun.current_clip != 0:
            # If no bullets, pass
            self.agent.use_gun(mouse_x, mouse_y)
  
              # automatic fire activation
            if self.agent.gun.automatic:
              self.agent.set_is_shooting(True)
            
            self.agent.set_frames_since_last_shot(0)
            self.agent.gun.conseuctive_bullets = 1

            # for automatic fire

            self.agent.set_frames_since_last_shot(self.agent._frames_since_last_shot +1)
        else:
          
          self.agent.set_is_shooting(False)

       # if keys[pygame.MOUSEBUTTONUP]:
         # mouse_presses = pygame.mouse.get_pressed()
          #f not mouse_presses[0]:
            #self.agent._is_shooting = False
    
    def check_still_shooting(self):
        """
        aaa
        """
        # If no bullets, pass
        if self.agent._frames_since_reload < self.agent.gun._frames_for_reload \
            and self.agent._is_reloading:
            return
        elif self.agent._is_reloading:
            self.agent.set_is_reloading(False)
            # print("reloaded")
            # (self.agent.gun.current_clip)
        
        #check if automatic firing, check frame till next shot, check ammo
        if self.agent._is_shooting and self.agent._frames_since_last_shot >= \
            self.agent.gun._frames_before_shot and self.agent.gun.current_clip \
                 != 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.agent.use_gun(mouse_x ,mouse_y)
            self.agent.set_frames_since_last_shot(0)

            #update consecutive bullet count, for calculating spread,
            #only do for automatic fire
            self.agent.gun.consecutive_bullets += 1
        elif not self.agent._is_shooting:
            self.agent.gun.consecutive_bullets = 0

    def check_reload(self, keys):
        if keys[pygame.K_r]:
          #this could be any non 0 positive integer, will do the same thing
          self.agent.reload_gun()
          #print("start reload")
        if self.agent._is_reloading:
          self.agent.set_frames_since_reload(self.agent._frames_since_reload + 1)
          
    # bullet controlls

    def update_bullets_test(self, walls):
      global bullet_dictionary
      global bullet_delete_dictionary
      for bullet in bullet_dictionary.values():
        self.bullet_main(bullet, walls)
      #actually delete the bullet
      for bullet_name in bullet_delete_dictionary.keys():
        del bullet_dictionary[bullet_name]
      bullet_delete_dictionary.clear()

    def bullet_main(self, bullet, walls):
        #the main things a bullet does each frame. crazy
        #delete_check_list is a list of walls to check collision with for every bullet
        #delete_check list should be generated elsewhere, probably in the main loop 
        #with another function.
        bullet.update_position()
        #for collision in walls:
           # if bullet.check_basic_collision(collision):
                #check to make sure that deleting a key value pair from a dictionary
                #you're iterating through doesn't mess everything up
               # bullet.delete_bullet()
            #if theres a player, damage them, again this should be done through
              #a controller, but we're testing rn so whatever.
              #if type(collide_possible) is player_test:
              #    collide_possible.update_health(self.damage)
              #break


    def spike_interaction(self, keys, map_model):
        # Hold down 4 to plant & to defuse
        if self._agent.spike and keys[pygame.K_4] and map_model.a_site:
            # Add in thing to track time; 4 seconds for plant
            self._agent.plant_spike()
        elif not self._agent.spike and keys[pygame.K_4]:
            # Add in thing to track time; 7 seconds for defuse
            # 3.5s for half
            self._agent.defuse_spike()
        
    def orb_interaction(self, event):
        # Not implementing rn
        pass
