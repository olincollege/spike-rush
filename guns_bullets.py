import math
from random import randint, randrange
import pygame
#from run_game import frame_rate

frame_rate = 30

#global bc GLBOAL fsduckjscajkajsdajk; 

#... would not recomend unglobaling. wait, not how global vars work, fixing

#fixed, these 3 things should always be referred to as global
#initialize an empty dictionary that will store all bullets
bullet_dictionary = {}
#initialize a counter for bullets
bullet_counter = 0 
#bullets to delete, fixes deleting during iteration issue
bullet_delete_dictionary = {}

#GUN
class gun():
    #gun should have name and defined damage value
    damage = 20

    max_spread = math.ceil(frame_rate * 40/60)
    min_spread = 0
    shots_for_full_spread = 7
    frames_before_shot = math.ceil(frame_rate*15/60)

    #the consecutive number of bullets automatically fire(for calculating spread)
    consecutive_bullets = 0

    clip_size = 20
    frames_for_reload = math.ceil(frame_rate*120/60) # 2 seconds

    current_clip = 20

    #upon further consideration, it doesn't make much sense to keep track of these things
    #if we're not updating the gun's position as we go, we should probably implement that tho

    def __init__(self):
        self.automatic = True

    def update_clip(self,clip_update):


        #function handles reloading and decreasing clip from shooting
        #a negative integer means a shot has been fired, decrease clip
        if clip_update <= 0:
            self.current_clip += clip_update
            #if clip is negative
            if self.current_clip < 0:
                self.current_clip = 0
        
        #otherwise reload 
        else:
            self.current_clip = self.clip_size

    
    def shoot(self, player_x, player_y, theta):    
        #defining bullet heading
        #norm_value = ((mouse_x -player_x)**2 + (mouse_y -player_y)**2)**.5
        #x_increment = (mouse_x -player_x)/norm_value
        #y_increment = (mouse_y -player_y)/norm_value
        
        #theta in radians
        x_increment = math.cos(theta)
        y_increment = math.sin(theta)

        #doing spread
        perp_vector = [-y_increment,x_increment]
        
        #account for 0 division
        if self.shots_for_full_spread != 0:
            this_bullet_max_spread = self.max_spread*self.consecutive_bullets \
          / self.shots_for_full_spread
        else:
            this_bullet_max_spread = self.max_spread
        spread_factor = self.min_spread
        if self.min_spread < math.ceil(this_bullet_max_spread):
            spread_factor = randint(self.min_spread,math.ceil(this_bullet_max_spread))

        actual_spread_x = perp_vector[0] * spread_factor * (-1)**(randint(0,1))
        actual_spread_y = perp_vector[1] * spread_factor * (-1)**(randint(0,1))

        #if you increase this by a factor of 10, increase the max spread by a factor of 10 too
        #basically will just allow you more spread angles :)
        x_increment += actual_spread_x/1000
        y_increment += actual_spread_y/1000

        bullet_start_x = player_x + math.floor(30*x_increment) +25
        bullet_start_y = player_y + math.floor(30*y_increment) + 25
      
        #create a new bullet and add it to the dictionary of bullets
        global bullet_counter
        bullet_counter += 1
        new_bullet = bullet(bullet_start_x, bullet_start_y, x_increment, \
                            y_increment, self.damage)

        update_dict = {new_bullet.name:new_bullet}

        bullet_dictionary.update(update_dict)

        #decrease clip size by 1
        self.update_clip(-1)

class bullet():
    speed_per_tick = math.ceil(frame_rate *20/60)
    #number needs to be even

    def __init__(self, pos_x, pos_y, incr_x, incr_y, damage):
        #things necessary for calculating heading
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.incr_x = incr_x
        self.incr_y = incr_y
        #define bullet damage (based on gun stats)
        self.damage = damage

        self.delta_x = self.incr_x * self.speed_per_tick
        self.delta_y = self.incr_y * self.speed_per_tick

        global bullet_counter
        self.name = f"bullet_{bullet_counter}"

    
    #update positions
    def update_position(self):
        self.pos_x += self.delta_x
        self.pos_y += self.delta_y

    def delete_bullet(self):
        #delete a bullet from the list of bullets, might stop it from existing... probably
        global bullet_dictionary
        global bullet_delete_dictionary

        bullet_delete_dictionary.update({self.name:bullet_dictionary[self.name]})

#defining general gun classes

class classic(gun):
    """
    a gun that emulates the classic
    """
    damage = 22
    max_spread = math.ceil(frame_rate * 50/60)
    min_spread = 0
    shots_for_full_spread = 7
    frames_before_shot = math.ceil(frame_rate*10/60)
    
    consecutive_bullets = 0
    clip_size = 12
    current_clip = 12
    frames_for_reload = math.ceil(frame_rate*105/60)


    def __init__(self):
        self.automatic = False

class spectre(gun):
    """
    a gun that emulates the classic
    """
    damage = 22
    max_spread = math.ceil(frame_rate*70/60)
    min_spread = 0
    shots_for_full_spread = 9
    frames_before_shot = math.ceil(frame_rate*5/60)
    
    consecutive_bullets = 0
    clip_size = 30
    current_clip = 30
    frames_for_reload = math.ceil(frame_rate*135/60)


    def __init__(self):
        self.automatic = True

class guardian(gun):
    """
    a gun that emulates the classic
    """
    damage = 65
    max_spread = math.ceil(frame_rate*40/60)
    min_spread = 0
    shots_for_full_spread = 9
    frames_before_shot = math.ceil(frame_rate*10/60)
    
    consecutive_bullets = 0
    clip_size = 12
    current_clip = 12
    frames_for_reload = math.ceil(frame_rate*135/60)

    def __init__(self):
        self.automatic = False

class vandal(gun):
    """
    a gun that emulates the classic
    """
    damage = 40
    max_spread = math.ceil(frame_rate*120/60)
    min_spread = math.ceil(frame_rate*10/60)
    shots_for_full_spread = 8
    frames_before_shot = math.ceil(frame_rate*6/60)
    
    consecutive_bullets = 0
    clip_size = 25
    current_clip = 25
    frames_for_reload = math.ceil(frame_rate*150/60)

    def __init__(self):
        self.automatic = True

#this one is special. ill get to it later
class operator(gun):
    """
    a gun that emulates the operator
    
    have to put in alt fire before this + other stuff
    
    """
    damage = 150
    max_spread = math.ceil(frame_rate*40/60)
    min_spread = 0
    shots_for_full_spread = 9
    frames_before_shot = math.ceil(frame_rate*80/60)
    
    consecutive_bullets = 0
    clip_size = 5
    current_clip = 5
    frames_for_reload = math.ceil(frame_rate*222/60)


    def __init__(self):
        self.automatic = False
    
    pass

gun_list =[classic(),spectre(),guardian(),vandal()]



