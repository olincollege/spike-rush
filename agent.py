"""
Docstring >:)
"""

from numpy import angle
import pygame
import os
from regex import E
from guns_bullets import *
from test_map import *
from abc import ABC, abstractmethod
from spike import *
from spike_map import *
import math
from hud import display_model, display_view


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

    def __init__(self, x_init, y_init, side):
        """
        Creates an instance of an agent.
        """
        self._location = [x_init, y_init]
        self._health = 100
        self._gun = vandal()
        self._color = (192, 192, 192)   # Default circle is gray
        self._spike = True  # If spike is true, it has not yet been planted
        self._spike_object = None
        self._side = side

        self._frames_since_last_shot = 0
        self._frames_since_reload = 0

        self._frames_since_last_spike_interaction = 0

        self._is_shooting = False
        self._is_reloading = False
        #self.is_defusing = False

        self._turn_speed = .15*frame_rate/30
        self._angle = 0
        
         #player starts as alive
        self._alive = True

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
    def angle(self):
        """
        Returns the agent's shoot angle

        Returns:
            a float representing the shooting angle of an agent in radians
        """
        return self._angle

    @property
    def spike(self):
        """
        Returns true if the agent is currently holding the spike;
        otherwise, false.
        """
        return self._spike

    @property
    def spike_object(self):
        return self._spike_object

    @property
    def gun(self):
        return self._gun

    @property
    def side(self):
        return self._side

    @property
    def alive(self):
        return self._alive


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

    def set_angle(self, angle):
        self._angle = angle

    def set_frames_since_last_spike_interaction(self, new_frames):
        self._frames_since_last_spike_interaction = new_frames

    def kill(self):
        self._alive = False

    @abstractmethod
    def use_ultimate(self):
        """
        Not implemented [yet].
        """
        pass

    def use_gun(self):
        self._gun.shoot(self.location[0], self.location[1], self._angle)

    def reload_gun(self):
      # fix for private variable calls
      self._gun.update_clip(1)
      self.set_is_reloading(True)
      self._frames_since_reload = 0

    def plant_spike(self, map_model):
        """
        aaa

        Returns:
            None.
        """
        self._spike = False
        self._spike_object = Spike(self.location[0], self.location[1])
      
    def defuse_spike(self, spike):
        """
        aaa

        Args:
            spike: The spike object being defused.
        Returns:
            None.
        """
        spike.defuse()

    def set_spike_object(self, new_spike):
      self._spike_object = new_spike

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

    Attributes:
        agent: attributes from the agent class.
        _sprite: A string representing the image to use as the sprite for the
        agent.
    """
    bullet_width = 6

    def __init__(self, agent_model, image_path):
        self._agent = agent_model
        self._img_path = image_path
        #self._agent = agent
        #self._sprite = sprite
        #self._bullet_sprites = []
        #self.bullet_group = None

        #self._sprite = self._agent._sprite

        # initiate sprite stuff
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
        return self._agent

def dot_sight(self, surface):

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
                              math.floor(dot_y + dot_width/2), dot_width, dot_width)

        pygame.draw.rect(surface, (255, 0, 0), red_dot)

    def draw_agent(self, surface):
        self.agent_sprite.rect.x = self.agent.location[0]
        self.agent_sprite.rect.y = self.agent.location[1]

        # draw sprite on to surface
        surface.blit(self.agent_sprite.image, (self.agent_sprite.rect))

    def draw_bullets(self, surface):
        #global bullet_dictionary
        for bullet in self._agent._gun.bullet_dict.values():
            bullet_sprite = pygame.sprite.Sprite()
            bullet_sprite.image = pygame.Surface((self.bullet_width, self.bullet_width))
            bullet_sprite.image.fill((0, 0, 0))
            bullet_x = math.floor(bullet.pos_x - self.bullet_width/2)
            bullet_y = math.floor(bullet.pos_y + self.bullet_width/2)
            bullet_sprite.rect = pygame.Rect(bullet_x, bullet_y, self.bullet_width, self.bullet_width)
            #self._bullet_sprites.add(bullet_sprite)
            bullet.set_sprite(bullet_sprite)
            surface.blit(bullet_sprite.image, bullet_sprite.rect)
            
            #pygame.draw.rect(surface, (0, 0, 0), bullet_rectangle)
    def draw_spike(self, surface):
        spike = self._agent.spike_object
        if spike is not None:
          spike_width = 20
          spike_sprite = pygame.sprite.Sprite()
          spike_sprite.image = pygame.Surface((spike_width, spike_width))
          spike_sprite.image.fill((100, 100, 100))
          spike_sprite.rect = pygame.Rect(self._agent.spike_object.location[0], self._agent.spike_object.location[1], spike_width, spike_width)

          surface.blit(spike_sprite.image, spike_sprite.rect)
        


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
            control_list = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, \
                pygame.K_c, pygame.K_v]

        if input_type == "Arrow":
            control_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,
                            pygame.K_RIGHT, pygame.K_COMMA, \
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
            theta_change = self.agent._turn_speed
            self.agent.set_angle(self.agent.angle + theta_change)
        
        if keys[control_list[4]]:  # turn counter clockwise
            theta_change = self.agent._turn_speed
            self.agent.set_angle(self.agent.angle - theta_change)

        # did we hit something?
        collision_list = \
            pygame.sprite.spritecollide(self.view.agent_sprite, walls, False)
        for wall in collision_list:
            # reset position
            if xchange > 0:
                self._view.agent_sprite.rect.right = wall.rect.left
                self.agent.location[0] = self._view.agent_sprite.rect.left
            elif xchange < 0:
                self._view.agent_sprite.rect.left = wall.rect.right
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
        for wall in collision_list:
            # reset position
            if ychange > 0:
                self._view.agent_sprite.rect.bottom = wall.rect.top
                self.agent.location[1] = self._view.agent_sprite.rect.top
            elif ychange < 0:
                self._view.agent_sprite.rect.top = wall.rect.bottom
                self.agent.location[1] = self._view.agent_sprite.rect.top

    # gun controls
    def check_shoot(self, keys, input_type):
        """
        aaa
        """

        # if reloading, don't fire
        if self.agent._frames_since_reload < self.agent.gun.frames_for_reload \
                and self.agent._is_reloading:
            self.agent._gun.consective_bullets = 0
            return
        elif self.agent._is_reloading:
            self.agent.set_is_reloading(False)
            # print("reloaded")
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.agent.set_frames_since_last_shot(self.agent._frames_since_last_shot +1)
        # consecutive fire


        if (input_type == "WASD" and keys[pygame.K_x]) or (input_type == \
             "Arrow" and keys[pygame.K_m]):
            
            if self.agent._is_shooting and not self.agent._gun.automatic:
                self.agent._gun.consecutive_bullets = 0
                return


            if self.agent._frames_since_last_shot < \
                self.agent._gun.frames_before_shot:
                return
            
            # if the weapon is semi auto, don't shoot it uatomatically


            if self.agent._gun.current_clip > 0:
            # If no bullets, pass
                self.agent.use_gun()
  
              # automatic fire activation
            # if self.agent.gun.automatic:
                if self.agent._is_shooting:
                    self.agent._gun.consecutive_bullets += 1
                else:
                    self.agent._gun.consecutive_bullets = 1
                
                # print(self.agent._gun.consecutive_bullets)
                self.agent.set_is_shooting(True)
            
                self.agent.set_frames_since_last_shot(0)
                

                # automatic fire activation
                if self.agent.gun.automatic:
                    self.agent.set_is_shooting(True)
            else:
                self.agent._gun.consecutive_bullets = 0
                self.agent.set_is_shooting(False)

            
        else:
            self.agent.set_is_shooting(False)
            self.agent._gun.consecutive_bullets = 0

         # if keys[pygame.MOUSEBUTTONUP]:
           # mouse_presses = pygame.mouse.get_pressed()
            # f not mouse_presses[0]:
            #self.agent._is_shooting = False

    def check_still_shooting(self):
        """
        aaa
        """
        # If reloading, dont fire
        if self.agent._frames_since_reload < self.agent.gun._frames_for_reload \
                and self.agent._is_reloading:
            return
        # no longer reloading, stop reload status
        elif self.agent._is_reloading:
            self.agent.set_is_reloading(False)
            # print("reloaded")
            # (self.agent.gun.current_clip)

        # check if automatic firing, check frame till next shot, check ammo
        if self.agent._is_shooting and self.agent._frames_since_last_shot >= \
            self.agent.gun._frames_before_shot and self.agent.gun.current_clip \
                 > 0:

            self.agent.use_gun()
            self.agent.set_frames_since_last_shot(0)

            # update consecutive bullet count, for calculating spread,
            # only do for automatic fire
            self.agent.gun.consecutive_bullets += 1
        elif not self.agent._is_shooting:
            self.agent.gun.consecutive_bullets = 0

    def check_reload(self, keys, input_type):
        
        if input_type == "Arrow" and keys[pygame.K_l]:
          
          self.agent.reload_gun()

        if input_type == "WASD" and keys[pygame.K_r]:
          
          self.agent.reload_gun()
        
        if self.agent._is_reloading:
          self.agent.set_frames_since_reload(self.agent._frames_since_reload + 1)

    # bullet controlls

    def update_bullets_test(self, walls, players, other_agent):
        #global bullet_dictionary
        #global bullet_delete_dictionary
        for bullet in self._agent._gun.bullet_dict.values():
            self.bullet_main(bullet, walls, players, other_agent)
        # actually delete the bullet
        for bullet_name in self._agent._gun.bullet_delete_dict.keys():
            del self._agent._gun.bullet_dict[bullet_name]
        self._agent._gun.bullet_delete_dict.clear()

    def bullet_collision(self, bullet, walls, players, other_agent):
      if bullet.bullet_sprite is not None:
        wall_collision_list = \
            pygame.sprite.spritecollide(bullet.bullet_sprite, walls, False)
        agent_collision_list = \
            pygame.sprite.spritecollide(bullet.bullet_sprite, players, False)
        for wall in wall_collision_list:
            self._agent._gun.delete_bullet(bullet)
        for index, agent in enumerate(agent_collision_list):
            # the way this is implemented will not work in 2+v2+ games
            self._agent._gun.delete_bullet(bullet)  
            other_agent.update_health(other_agent.health - 10)
            
            if other_agent.health <= 0:
              other_agent.kill()
           # agent.die
  
    def bullet_main(self, bullet, walls, players, other_agent):
        # the main things a bullet does each frame. crazy
        # delete_check_list is a list of walls to check collision with for every bullet
        # delete_check list should be generated elsewhere, probably in the main loop
        # with another function.
        bullet.update_position()
        self.bullet_collision(bullet, walls, players, other_agent)
        # for collision in walls:
        # if bullet.check_basic_collision(collision):
        # check to make sure that deleting a key value pair from a dictionary
        # you're iterating through doesn't mess everything up
        # bullet.delete_bullet()
        # if theres a player, damage them, again this should be done through
        # a controller, but we're testing rn so whatever.
        # if type(collide_possible) is player_test:
        #    collide_possible.update_health(self.damage)
        # break

    def spike_plant(self, keys, map_model, input_type, hud_model):
        frames_to_plant = 125 # 4 seconds @ 30 fps
        if self._agent.side != "attack":
          return
        if map_model.a_site.in_zone(self._agent):
            if (input_type == "WASD" and keys[pygame.K_4] or \
             input_type == "Arrow" and keys[pygame.K_SEMICOLON]):
              if self._agent.spike and self._agent._frames_since_last_spike_interaction == \
              frames_to_plant:
                print("Planted")
                self._agent.plant_spike(map_model)
                hud_model.timer = 45
              elif self._agent.spike:
                self._agent.set_frames_since_last_spike_interaction( \
                self._agent._frames_since_last_spike_interaction + 1)
            else: 
              self._agent.set_frames_since_last_spike_interaction(0)
    
    def spike_defuse(self, keys, map_model, input_type, other_agent, hud_model):
        if self._agent.side != "defense":
          return
        frames_to_defuse = 225 # 7 seconds @ 30 fps
        spike = other_agent.spike_object

        if spike is not None and \
      map_model.a_site.within_defuse_range(self._agent, spike):
          if (input_type == "WASD" and keys[pygame.K_4] or \
             input_type == "Arrow" and keys[pygame.K_SEMICOLON]):
            if not spike.status and \
            self._agent._frames_since_last_spike_interaction == \
            frames_to_defuse and spike.frames_since_plant < \
            spike.frames_to_explode:
              print("Defused")
              self._agent.defuse_spike(other_agent.spike_object)
              hud_model.timer = 0
              other_agent.set_spike_object(None)
            elif not spike.status:
              self._agent.set_frames_since_last_spike_interaction( \
                self._agent._frames_since_last_spike_interaction + 1)
          else: 
              self._agent.set_frames_since_last_spike_interaction(0)
          #else:
          #  if self._agent._frames_since_last_spike_interaction < \
          #  frames_to_diffuse and :
          #    print("Defuse")
          #    self._agent.defuse_spike()
          #self._agent.set_frames_since_last_spike_interaction( \

        


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

    track_second = pygame.USEREVENT  # using ID 24

    # trigger event every second
    pygame.time.set_timer(track_second, 1000)

    # initialize HUD
    hud_model = display_model()
    hud_view = display_view(hud_model)

    # Player 1 instance
    character_model_1 = Agent(0, 0, "attack")
    character_view_1 = AgentView(character_model_1, 'test_sprite.png')
    character_controller_1 = AgentController(
        character_model_1, character_view_1)

    # Player 2 instance
    character_model_2 = Agent(0, 0, "defense")
    character_view_2 = AgentView(character_model_2, 'test_sprite.png')
    character_controller_2 = AgentController(
        character_model_2, character_view_2)

    # Player list
    agents = [character_model_1, character_model_2]
    agent_list = pygame.sprite.Group()
    agent_list.add(character_view_1.agent_sprite)
    agent_list.add(character_view_2.agent_sprite)

    map_model.attacker_spawn.set_spawns([character_model_1])
    map_model.defender_spawn.set_spawns([character_model_2])



    # main loop
    run = True
    while run:

        # sense inputs (get events)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                run = False
                
            if event.type == track_second:
                # if a second has passed, reduce the timer
                if hud_model.timer != 0:
                    hud_model.timer -= 1

        # update states
        # create entities
        # detect interactions

        # movement
        # check which keys are currently pressed
        keys = pygame.key.get_pressed()
        # if no collisions are detected, move characters
        map_view.draw_map()

        print(character_model_1.alive)
        if character_model_1.alive:


            character_controller_1.move(
                character_speed, keys, "WASD", map_model._wall_list)
                    
            character_controller_1.check_shoot(keys,"WASD")
            character_controller_1.check_reload(keys,"WASD")

            character_view_1.draw_agent(map_view._window)
            character_view_1.dot_sight(map_view._window)
        
        print(character_model_2.alive)
        if character_model_2.alive:


            character_controller_2.move(
                character_speed, keys, "Arrow", map_model._wall_list)
            character_view_2.draw_agent(map_view._window)
            character_view_2.dot_sight(map_view._window)

        character_controller_1.check_shoot(keys,"WASD")
        character_controller_1.check_reload(keys,"WASD")

        character_controller_2.check_shoot(keys,"Arrow")
        character_controller_2.check_reload(keys,"Arrow")

        character_controller_1.spike_plant(keys, map_model, "WASD", hud_model)
        character_controller_2.spike_defuse(keys, map_model, "Arrow", agents[0], hud_model)

        # update stuff
        # draw backdrop
        map_view.draw_map()

        # walls will still have collision even if not drawn
        # map_view.draw_walls()

        # draw HUD updates

        hud_view.draw_player_updates(
            character_model_1, character_model_2, map_view._window)
        hud_view.draw_game_timer(map_view._window)

        # draw spike
        character_view_1.draw_spike(map_view._window)
        character_view_2.draw_spike(map_view._window)

        # draw characters
        character_view_1.draw_agent(map_view._window)
        character_view_2.draw_agent(map_view._window)

        character_controller_2.update_bullets_test(map_model._wall_list, \
                                                   agent_list, agents[0])
        character_view_2.draw_bullets(map_view._window)
        character_controller_1.update_bullets_test(map_model._wall_list, \
                                                   agent_list, agents[1]
                                                  )
        character_view_1.draw_bullets(map_view._window)

        pygame.display.flip()  # update entire display
        clock.tick(30)  # reduce framerate to 30

    # print(map_view._window.get_rect()) #check window dimensions
    pygame.quit()  # after main loop has finished
