import math
from random import randint, randrange
import pygame
from run_game import frame_rate
# pylint:skip-file
# Old file.
#don't wworryy about this
class player_test():

    health = 100
    #red circle
    color = (255,0,255) #purple
    circle_x_y = (100,50)
    border_width = 0

    #are you currently moving in a direction
    xstate = 0
    ystate = 0

    frames_since_last_shot = 0
    frames_since_reload = 0

    is_shooting = False
    is_reloading = False




    def __init__(self,x_init,y_init,radius,gun):
        self.xpos = x_init
        self.ypos = y_init
        self.radius = radius
        #instance of the gun class
        self.gun = gun

        self.rect = pygame.Rect(math.floor(self.xpos - self.radius), \
            math.floor(self.ypos + self.radius),self.radius,\
            self.radius)


    #draw an updated circle
    def update_pos(self,delta_x,delta_y):

        self.xpos += delta_x
        self.ypos += delta_y

        
        self.rect = pygame.Rect(math.floor(self.xpos - self.radius), \
            math.floor(self.ypos + self.radius),self.radius,\
            self.radius)
    
    #this method is entirely insufficient and only being used for testing atm
    #should probably be robustly defined in controller class
    def update_health(self,damage):
        self.health -= damage
    
    #DRAW IT
    def draw_circ(self,game_map):
        pygame.draw.circle(game_map.window, self.color, (self.xpos,self.ypos), self.radius, self.border_width)


class player_test_controller():
    """
    contrller for red circle
    """
    #pixels to move
    move_incr = 10
    def __init__(self,player):
        
        #our red circle
        self.player = player

    def move(self,event):
        
        #the event we are reacting to. will look something like "pygame.K_left", event must be passed in as event.type,
        #should only be checked if a key is pressed
        if event.key == pygame.K_UP or event.key == ord("w"):
            self.player.update_pos(0,-self.move_incr)
            #basically stores that this key is being pressed
            self.player.ystate = 1
        if event.key == pygame.K_LEFT or event.key == ord("a"):
            self.player.update_pos(-self.move_incr,0)
            self.player.xstate = 1
        if event.key == pygame.K_DOWN or event.key == ord("s"):
            self.player.update_pos(0,self.move_incr)
            self.player.ystate = -1
        if event.key == pygame.K_RIGHT or event.key == ord("d"):
            self.player.update_pos(self.move_incr,0)
            self.player.xstate = -1

    def check_shoot(self,event):
        """
        Check if a player has begun or stopped shooting a weapon, shooting the 
        weapon accordingly.


        Several factors are checked before allowing a gun to fire: if a player
        is reloading, has no bullets in their clip, or has fired too recently
        then the gun will not fire at all. This method is designed to be run
        once for every pygame event in a given frame, but the actual content of
        the method can only be run once per frame.
        
        Several values are also updated in this function that require
        tracking continuity in game state (rather than being calculated in each
        discrete timestep):
            self.player.is_shooting: A boolean representing whether or not
                a player's automatic weapon is firing.
            self.player.is_reloading: A boolean representing whether or not
                a player is currently reloading a weapon.
            self.player.frames_since_last_shot: a positive integer representing
                the number of frames a bullet has been last shot
            self.player.gun.consecutive_bullets: a positive integer
                representing how many bullets have been fired at the shortest
                time between shots. Used for calculating bullet spread for
                automatic weapons.
            self.player.gun.current_clip: a positive integer representing
                the number of bullets in a gun's clip.
            
        
        Args:
            event: a pygame event type object representing some player input
            such as a keypress or mouse click.

        """

        #if reloading, don't fire

        if self.player.frames_since_reload < self.player.gun.frames_for_reload \
            and self.player.is_reloading:
            return
        elif self.player.is_reloading:
            self.player.is_reloading = False


        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()
            #left mouse button check, ammo check, frames before next shot check
            if event.button ==1 and self.player.frames_since_last_shot >= \
                self.player.gun.frames_before_shot and self.player.gun.current_clip != 0:
                #if no bullets, pass
                

                
                self.player.gun.shoot(self.player.xpos,self.player.ypos,mouse_x,mouse_y)
                #if this is true, activate automatic fire
                if self.player.gun.automatic:
                    self.player.is_shooting = True

                self.player.frames_since_last_shot = 0
                self.player.gun.consecutive_bullets = 1
                
                #for automatic fire
                self.player.frames_since_last_shot += 1
        
        #stop automatic fire
        if event.type == pygame.MOUSEBUTTONUP:

            mouse_presses = pygame.mouse.get_pressed()
            if not mouse_presses[0]:
                self.player.is_shooting = False
        

    
    def check_still_shooting(self):
        """
        Check if an automatic weapon is still being fired, and keep firing it
        accordingly.

        This method performs a similar function to the check_shoot() method,
        but is meant instead to enable continuous fire of automatic weapons and
        should only be run once per frame.
        
        """
        
        #if no bullets, pass

        if self.player.frames_since_reload < self.player.gun.frames_for_reload \
            and self.player.is_reloading:
            return
        elif self.player.is_reloading:
            self.player.is_reloading = False
            print("reloaded")
            print(self.player.gun.current_clip)
        
        
        #check if automatic firing, check frame till next shot, check ammo
        if self.player.is_shooting and self.player.frames_since_last_shot >= \
            self.player.gun.frames_before_shot and self.player.gun.current_clip != 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.player.gun.shoot(self.player.xpos,self.player.ypos,mouse_x,mouse_y)
            self.player.frames_since_last_shot = 0

            #update consecutive bullet count, for calculating spread,
            #only do for automatic fire
            self.player.gun.consecutive_bullets += 1
        elif not self.player.is_shooting:
            self.player.gun.consecutive_bullets = 0


    #if a key is unpressed stop motion
    def stop_move(self,event):
        
        if event.key == pygame.K_UP or event.key == ord("w"):
            #says that the keys are not still being pressed
            self.player.ystate = 0
        if event.key == pygame.K_LEFT or event.key == ord("a"):
            self.player.xstate = 0
        if event.key == pygame.K_DOWN or event.key == ord("s"):
            self.player.ystate = 0
        if event.key == pygame.K_RIGHT or event.key == ord("d"):
            self.player.xstate = 0
    def still_moving(self):
        
        #if a key is still being pressed, unpress
        if self.player.xstate != 0:
            self.player.update_pos(self.player.xstate *-self.move_incr,0)
        if self.player.ystate != 0:
            self.player.update_pos(0,self.player.ystate *-self.move_incr)
    
    def check_reload(self,event):
        """
        Check if a player has initiated a reload, and start reloading the gun
        accordingly.

        Args:
            event: a pygame event type object representing some player input
                such as a keypress or mouse click.
        
        """
        if event.type == pygame.KEYDOWN:
            if event.key == ord("r"):
                #this could be any non 0 positive integer, will do the same thing
                self.player.gun.update_clip(1)
                self.player.is_reloading = True
                self.player.frames_since_reload = 0
                print("start reload")



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
    """
    A general instance of a shootable gun.
    
    Attributes:
        damage: an integer representing the amount of health that a bullet
            shot from this gun takes away from the player.
        max_spread: the maximum amount of pixels per thousand, perpindicular
            to the shooting direction vector that a bullet shot from this gun
            can travel per pixel. A dimensionless float.
        min_spread: the minimum amount of pixels per thousand, perpindicular
            to the shooting direction vector that a bullet shot from this gun
            can travel per pixel. A dimensionless float.
        shots_for_full_spread: the number of consecutive bullets that need to
            be fired by an automatic weapon for a bullet to achieve the gun's
            max spread threshold. An integer.
        frames_before_shot: an integer representing the number of frames that
            a player must wait after shooting the gun before shooting the gun
            again.
        consecutive_bullets: an integer representing the number of bullets that
            have been fired consecutively by a gun. Updated in the main game
            loop.
        clip_size: an integer representing maximum number of bullets that can
            be fired from a weapon before needing to reload.
        frames_for_reload: an integer representing the number of frames that
            a player must wait after reloading the gun before being able to
            perform other actions.
        current_clip: an integer representing the number of bullets that a gun
            can fire before requiring a reload. Updated in the main game loop.
        automatic: a boolean representing whether or not a weapon is an 
            automatic weapon or not.

        
    """
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
        """
        Initialize an instance of the gun class.
        """
        self.automatic = True

    def update_clip(self,clip_update):
        """
        Update the number of bullets in a gun's clip.

        Args:
            clip_update: an integer either representing how many bullets to
                subtract from a clip or an indication to reload.
        """

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
        


    
    def shoot(self,player_x,player_y,mouse_x,mouse_y):
        """
        Shoot the gun
        """
        
        #defining bullet heading
        norm_value = ((mouse_x -player_x)**2 + (mouse_y -player_y)**2)**.5
        x_increment = (mouse_x -player_x)/norm_value
        y_increment = (mouse_y -player_y)/norm_value

        #doing spread
        perp_vector = [-y_increment,x_increment]
        
        #account for 0 division
        if self.shots_for_full_spread != 0:
            this_bullet_max_spread = self.max_spread*self.consecutive_bullets/self.shots_for_full_spread
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

        bullet_start_x = player_x + math.floor(15*x_increment)
        bullet_start_y = player_y + math.floor(15*y_increment)
        #create a new bullet and add it to the dictionary of bullets
        global bullet_counter
        bullet_counter += 1
        new_bullet = bullet(bullet_start_x,bullet_start_y,x_increment,y_increment,self.damage)

        update_dict = {new_bullet.name:new_bullet}

        bullet_dictionary.update(update_dict)

        #decrease clip size by 1
        self.update_clip(-1)

class bullet():
    """
    Define a bullet created by a gun, moving through space.

    Attributes:
        speed_per_tick: An integer representing the number of pixels that a
            bullet can travel per frame.
        bullet_width: An even, positive integer representing the width and
            height of a bullet.
        pos_x: a float representing the current x location of a bullet in
            pixels
        pos_y: a float representing the current y location of a bullet in
            pixels
        incr_x: a float representing the heading of a bullet in the x
            direction
        incr_y: a float representing the heading of a bullet in the y
            direction.
        damage: the amount of a health that a bullet takes from a player or
            enemy on hit. An integer.
        delta_x: a float representing the amount of distance that a bullet
            travels every frame in the x direction in pixels.
        delta_y: a float representing the amount of distance that a bullet
            travels every frame in the y direction in pixels.
        bullet_rectangle: a pygame rectangle object representing the location
            and size of a bullet on any given frame. Used for visualization and
            object collision detection.
        name: a string representing the name of a specific bullet. Useful for
            referencing a specific bullet in the global bullet dictionary.
        
    """

    speed_per_tick = math.ceil(frame_rate *20/60)
    #number needs to be even
    bullet_width = 6

    def __init__(self, pos_x, pos_y,incr_x,incr_y,damage):
        """
        Initialize an instance of the bullet class.

        Args:
            peed_per_tick: An integer representing the number of pixels that a
                bullet can travel per frame.
            bullet_width: An even, positive integer representing the width and
                height of a bullet.
            pos_x: a float representing the current x location of a bullet in
                pixels
            pos_y: a float representing the current y location of a bullet in
                pixels
            incr_x: a float representing the heading of a bullet in the x
                direction
            incr_y: a float representing the heading of a bullet in the y
                direction.
            damage: the amount of a health that a bullet takes from a player or
                enemy on hit. An integer.
        """
        
        #things necessary for calculating heading
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.incr_x = incr_x
        self.incr_y = incr_y
        #define bullet damage (based on gun stats)
        self.damage = damage
        #make a visualizable and moveable rectangle for the bullet

        self.delta_x = self.incr_x * self.speed_per_tick
        self.delta_y = self.incr_y * self.speed_per_tick

        #rectangle is gonna be invisible until it isn't
        self.bullet_rectangle = pygame.Rect(self.pos_x - self.bullet_width/2, \
            self.pos_y + self.bullet_width/2,self.bullet_width,\
            self.bullet_width)

        global bullet_counter
        self.name = f"bullet_{bullet_counter}"

    
    #update positions
    def update_position(self):
        """
        Update the position of a bullet for the next frame based on its movement
        attributes. 
        """

        self.pos_x += self.delta_x
        self.pos_y += self.delta_y
        #move the rectangle
        self.bullet_rectangle = pygame.Rect(math.floor(self.pos_x - self.bullet_width/2), \
            math.floor(self.pos_y + self.bullet_width/2),self.bullet_width,\
            self.bullet_width)
    
    def draw_bullet(self,game_map):
        """
        Draw a bullet onto a pygame window.

        Args:
            game_map: a pygame window
        """
        #surface,color,rectangle
        pygame.draw.rect(game_map.window,(0,0,0),self.bullet_rectangle)
    
    def delete_bullet(self):
        """
        Add this bullet to a dictionary of bullets to later be deleted.
        """
        #delete a bullet from the list of bullets, might stop it from existing... probably
        global bullet_dictionary
        global bullet_delete_dictionary

        bullet_delete_dictionary.update({self.name:bullet_dictionary[self.name]})
    
    #check if 2 rectangles are hitting each other. basic, doesn't need changing probably
    #we can do space partitioning outside of this class structure
    def check_basic_collision(self,wall_rectangle):
        """
        Check collision between this bullet and another rectangle.

        Args:
            wall_rectangle: a rectangle type pygame object representing some
                possible wall or obstacle for the bullet.
        Returns:
            a boolean representing whether or not the bullet and rectangle
                actually collide.
        """
        #wall rectangle is a RECTANGLE OBJECT WOW *sparkles

        if pygame.Rect.colliderect(self.bullet_rectangle,wall_rectangle) == True:
            return True
        else:
            return False
    def bullet_main(self, delete_check_list=[]):
        """
        Update a bullets position and check for any possible collisions in
        the new position.

        Args:
            delete_check_list: a list of rectangle objects to check against
                a bullet for collision


        """
        #the main things a bullet does each frame. crazy
        #delete_check_list is a list of walls to check collision with for every bullet
        #delete_check list should be generated elsewhere, probably in the main loop 
        #with another function.

        self.update_position()
        for collide_possible in delete_check_list:
            if self.check_basic_collision(collide_possible):
                #check to make sure that deleting a key value pair from a dictionary
                #you're iterating through doesn't mess everything up
                self.delete_bullet()
                #if theres a player, damage them, again this should be done through
                #a controller, but we're testing rn so whatever.
                if type(collide_possible) is player_test:
                    collide_possible.update_health(self.damage)
                break









#the following functions should be used for updating bullet states

def update_bullets():
    global bullet_dictionary
    for bullet in bullet_dictionary.values():
        bullet.bullet_main()

def update_bullets_for_guns_test(rectangle_object_list):
    global bullet_dictionary
    global bullet_delete_dictionary
    for bullet in bullet_dictionary.values():
        bullet.bullet_main(rectangle_object_list)
    #actually delete the bullet
    for bullet_name in bullet_delete_dictionary.keys():
        
        del bullet_dictionary[bullet_name]
    bullet_delete_dictionary.clear()
    

#vizualize all bullets from the dictionary
def draw_bullets(game_map):
    global bullet_dictionary
    for bullet in bullet_dictionary.values():
        bullet.draw_bullet(game_map)


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



