"""
Docstring >:)
"""

import pygame
import os
from regex import E
from players_guns_bullets import *
from test_map import *
from abc import ABC, abstractmethod
from spike import *
from spike_map import *

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
        self._current_health = 100
        self._gun = classic()
        self._color = (192, 192, 192)   # Default circle is gray
        self._spike = True # If spike is true, it has not yet been planted
        # self._sprite = None

        # Is agent currently moving in a direction
        self._xstate = 0
        self._ystate = 0

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

    @abstractmethod
    def use_ultimate(self):
        """
        Not implemented [yet].
        """
        pass

    def use_gun(self):
        """
        Pew pew
        """
        self._gun.shoot()
    
    def reload_gun(self):
        # Pass until reload gun method is defined
        self._gun.reload()

    def plant_spike(self):
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

    def draw_bullets(game_map):
      global bullet_dictionary
      for bullet in bullet_dictionary.values():
        bullet.draw_bullet(game_map)
    

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

    def move(self, speed, keys, walls):
        """
        Moves the character through the map. Detects pressed keys and moves
        the character correspondingly. Also detects collisions with walls and
        prevents character movement

        Arguments:
            speed: An integer representing the number of pixels a character
            moves per frame.
            keys: A list containing which keys are currently pressed.
            walls: A sprite group of all walls on the map.
        """
        current_pos = self.agent.location
        xchange = 0
        ychange = 0

        # searches for arrow keys and WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # left
            xchange = -speed
            self.agent.set_x_coord(current_pos[0]-speed)
            self._view.rect.x = self.agent.location[0]

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # right
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

        if keys[pygame.K_UP] or keys[pygame.K_w]:  # up
            ychange = -speed
            self.agent.set_y_coord(current_pos[1]-speed)
            self._view.rect.y = self.agent.location[1]

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # down
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

    def check_shoot(self, event):
        """
        aaa
        """
        #if reloading, don't fire
        if self.agent.frames_since_reload < self.agent.gun.frames_for_reload \
            and self.agent.is_reloading:
            return
        elif self.agent.is_reloading:
            self.agent.is_reloading = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            #left mouse button check, ammo check, frames before next shot check
            if event.button == 1 and self.agent.frames_since_last_shot >= \
                self.agent.gun.frames_before_shot and self.agent.gun.current_clip != 0:
                #if no bullets, pass                
                self.agent.gun.shoot(self.agent.location[0], \
                    self.agent.location[1], mouse_x, mouse_y)

                #if this is true, activate automatic fire
                if self.agent.gun.automatic:
                    self.agent.is_shooting = True

                self.agent.frames_since_last_shot = 0
                self.agent.gun.consecutive_bullets = 1
                
                #for automatic fire
                self.agent.frames_since_last_shot += 1
        
        #stop automatic fire
        if event.type == pygame.MOUSEBUTTONUP:

            mouse_presses = pygame.mouse.get_pressed()
            if not mouse_presses[0]:
                self.agent.is_shooting = False
        

    
    def check_still_shooting(self):
        """
        aaa
        """
        # If no bullets, pass
        if self.agent.frames_since_reload < self.agent.gun.frames_for_reload \
            and self.agent.is_reloading:
            return
        elif self.agent.is_reloading:
            self.agent.is_reloading = False
            # print("reloaded")
            # print(self.agent.gun.current_clip)
        
        
        #check if automatic firing, check frame till next shot, check ammo
        if self.agent.is_shooting and self.agent.frames_since_last_shot >= \
            self.agent.gun.frames_before_shot and self.agent.gun.current_clip \
                 != 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.agent.gun.shoot(self.agent.location[0], \
                self.agent.location[1], mouse_x ,mouse_y)
            self.agent.frames_since_last_shot = 0

            #update consecutive bullet count, for calculating spread,
            #only do for automatic fire
            self.agent.gun.consecutive_bullets += 1
        elif not self.agent.is_shooting:
            self.agent.gun.consecutive_bullets = 0

    def check_reload(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == ord("r"):
                #this could be any non 0 positive integer, will do the same thing
                self.agent.gun.update_clip(1)
                self.agent.is_reloading = True
                self.agent.frames_since_reload = 0
                # print("start reload")

    def spike_interaction(self, event):
        # Hold down 4 to plant & to defuse
        if self._agent.spike and  event.key == ord('4'):
            # Add in thing to track time; 4 seconds for plant
            self._agent.plant_spike()
        elif not self._agent.spike and event.key == ord('4'):
            # Add in thing to track time; 7 seconds for defuse
            # 3.5s for half
            self._agent.defuse_spike()
        
    def orb_interaction(self, event):
        # Not implementing rn
        pass

def agent_test():
    """
    Tests movement code with a test character.
    """
    pygame.init()  # initialize pygame
    map_model = split_model()
    map_view = split_view(map_model)  # initialize map
    clock = pygame.time.Clock()  # to keep track of time in-game
    character_speed = 10

    # create instances of classes
    character = Agent(205-25, 99-25)  # include parentheses when creating instance
    view = AgentView(character)
    controller = AgentController(character, view)

    # main loop
    run = True
    while run:

        # sense inputs (get events)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                run = False

        # update states
        # create entities
        # detect interactions

        # movement
        # check which keys are currently pressed
        keys = pygame.key.get_pressed()
        # if no collisions are detected, move character
        controller.move(character_speed, keys, map_model._wall_list)

        # update stuff
        # draw backdrop
        map_view.draw_map()

        # walls will still have collision even if not drawn
        # map_view.draw_walls()

        # draw character
        view.draw_agent(map_view._window)

        pygame.display.flip()  # update entire display
        clock.tick(30)  # reduce framerate to 30

    # print(map_view._window.get_rect()) #check window dimensions
    pygame.quit()  # after main loop has finished