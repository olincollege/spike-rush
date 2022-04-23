import math
import pygame
from pyparsing import match_previous_expr

#don't wworryy about this
class player_test():

    health = 10
    #red circle
    color = (255,0,255) #purple
    circle_x_y = (100,50)
    border_width = 0

    #are you currently moving in a direction
    xstate = 0
    ystate = 0

    gun = "classic"

    def __init__(self,x_init,y_init,radius,gun):
        self.xpos = x_init
        self.ypos = y_init
        self.radius = radius
        #instance of the gun class
        self.gun = gun

    #draw an updated circle
    def update_pos(self,delta_x,delta_y):

        self.xpos += delta_x
        self.ypos += delta_y
    
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_presses[0]:
                self.player.gun.shoot(self.player.xpos,self.player.ypos,mouse_x,mouse_y)


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

#global bc GLBOAL fsduckjscajkajsdajk; 

#... would not recomend unglobaling. wait, not how global vars work, fixing

#initialize an empty dictionary that will store all bullets
bullet_dictionary = {}
#initialize a counter for bullets
bullet_counter = 0 
#bullets to delete, fixes deleting during iteration issue
bullet_delete_dictionary = {}

#GUN
class gun():
    #gun should have name and defined damage value
    damage = 2
    #upon further consideration, it doesn't make much sense to keep track of these things
    #if we're not updating the gun's position as we go, we should probably implement that tho

    def __init__(self,x_pos,y_pos):
        self.player_x =x_pos
        self.player_y = y_pos
    
    def shoot(self,player_x,player_y,mouse_x,mouse_y):
        #defining bullet heading
        norm_value = ((mouse_x -player_x)**2 + (mouse_y -player_y)**2)**.5
        x_increment = (mouse_x -player_x)/norm_value
        y_increment = (mouse_y -player_y)/norm_value

        bullet_start_x = player_x + math.floor(15*x_increment)
        bullet_start_y = player_y + math.floor(15*y_increment)
        #create a new bullet and add it to the dictionary of bullets
        global bullet_counter
        bullet_counter += 1
        new_bullet = bullet(bullet_start_x,bullet_start_y,x_increment,y_increment,self.damage)
        
        #print(new_bullet)
        #print(new_bullet.name)
        update_dict = {new_bullet.name:new_bullet}
        #print(update_dict)
        bullet_dictionary.update(update_dict)


class bullet():

    speed_per_tick = 7
    bullet_width = 3

    def __init__(self, pos_x, pos_y,incr_x,incr_y,damage):
        
        #things necessary for calculating heading
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.incr_x = incr_x
        self.incr_y = incr_y
        #define bullet damage (based on gun stats)
        self.damage = damage
        #make a visualizable and moveable rectangle for the bullet

        #rectangle is gonna be invisible until it isn't
        self.bullet_rectangle = pygame.Rect(self.pos_x - self.bullet_width/2, \
            self.pos_y + self.bullet_width/2,self.bullet_width,\
            self.bullet_width)

        #print("made it to bullet creation")
        global bullet_counter
        self.name = f"bullet_{bullet_counter}"

    #kind of update positions (but not really())
    def bullet_move(self):
        #to be done in 1/60 of a second
        #floor because why the hell would you move by half a pixel
        delta_x = math.floor(self.incr_x * self.speed_per_tick)
        delta_y = math.floor(self.incr_y * self.speed_per_tick)
        #set the things. RECTANGLE
        self.update_position(delta_x,delta_y)
    
    #update positions
    def update_position(self,delta_x,delta_y):

        self.pos_x += delta_x
        self.pos_y += delta_y
        #move the rectangle
        self.bullet_rectangle = pygame.Rect.move(self.bullet_rectangle,delta_x,delta_y)
    
    def draw_bullet(self,game_map):
        #surface,color,rectangle
        pygame.draw.rect(game_map.window,(0,0,0),self.bullet_rectangle)
    
    def delete_bullet(self):
        #delete a bullet from the list of bullets, might stop it from existing... probably
        global bullet_dictionary
        global bullet_delete_dictionary

        bullet_delete_dictionary.update({self.name:bullet_dictionary[self.name]})
        print("made it to bullet deletion")
    
    #check if 2 rectangles are hitting each other. basic, doesn't need changing probably
    #we can do space partitioning outside of this class structure
    def check_basic_collision(self,wall_rectangle):
        #wall rectangle is a RECTANGLE OBJECT WOW *sparkles

        if pygame.Rect.colliderect(self.bullet_rectangle,wall_rectangle) == True:
            print("collision detected")
            return True
        else:
            return False
    def bullet_main(self, delete_check_list=[]):
        #the main things a bullet does each frame. crazy
        #delete_check_list is a list of walls to check collision with for every bullet
        #delete_check list should be generated elsewhere, probably in the main loop 
        #with another function.

        self.bullet_move()
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

def update_bullets_for_guns_test(rectangle_object):
    global bullet_dictionary
    global bullet_delete_dictionary
    for bullet in bullet_dictionary.values():
        bullet.bullet_main([rectangle_object])
    for bullet_name in bullet_delete_dictionary.keys():
        
        del bullet_dictionary[bullet_name]
    bullet_delete_dictionary.clear()
    

#vizualize all bullets from the dictionary
def draw_bullets(game_map):
    global bullet_dictionary
    for bullet in bullet_dictionary.values():
        bullet.draw_bullet(game_map)





