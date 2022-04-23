"""
The map for the game
"""

from bitarray import test
import pygame
#import players_guns_bullets

class moveable_test():

    #red circle
    color = (255,0,0) #red
    circle_x_y = (100,50)
    border_width = 0

    #are you currently moving in a direction
    xstate = 0
    ystate = 0



    def __init__(self,x_init,y_init,radius):
        self.xpos = x_init
        self.ypos = y_init
        self.radius = radius

    #draw an updated circle
    def update_pos(self,delta_x,delta_y):

        self.xpos += delta_x
        self.ypos += delta_y
    
    def draw_circ(self,game_map):
        pygame.draw.circle(game_map.window, self.color, (self.xpos,self.ypos), self.radius, self.border_width)



class moveable_controller():
    """
    contrller for red circle
    """
    #pixels to move
    move_incr = 10
    def __init__(self,red_circ):
        
        #our red circle
        self.red_circ = red_circ

    def move(self,event):
        
        #the event we are reacting to. will look something like "pygame.K_left", event must be passed in as event.type,
        #should only be checked if a key is pressed
        if event.key == pygame.K_UP or event.key == ord("w"):
            self.red_circ.update_pos(0,-self.move_incr)
            #basically stores that this key is being pressed
            self.red_circ.ystate = 1
        if event.key == pygame.K_LEFT or event.key == ord("a"):
            self.red_circ.update_pos(-self.move_incr,0)
            self.red_circ.xstate = 1
        if event.key == pygame.K_DOWN or event.key == ord("s"):
            self.red_circ.update_pos(0,self.move_incr)
            self.red_circ.ystate = -1
        if event.key == pygame.K_RIGHT or event.key == ord("d"):
            self.red_circ.update_pos(self.move_incr,0)
            self.red_circ.xstate = -1

    #if a key is unpressed stop motion
    def stop_move(self,event):
        
        if event.key == pygame.K_UP or event.key == ord("w"):
            #says that the keys are not still being pressed
            self.red_circ.ystate = 0
        if event.key == pygame.K_LEFT or event.key == ord("a"):
            self.red_circ.xstate = 0
        if event.key == pygame.K_DOWN or event.key == ord("s"):
            self.red_circ.ystate = 0
        if event.key == pygame.K_RIGHT or event.key == ord("d"):
            self.red_circ.xstate = 0
    def still_moving(self):
        
        #if a key is still being pressed, unpress
        if self.red_circ.xstate != 0:
            self.red_circ.update_pos( self.red_circ.xstate *-self.move_incr,0)
        if self.red_circ.ystate != 0:
            self.red_circ.update_pos(0,self.red_circ.ystate *-self.move_incr)




class spike_map():
    """
    A viewable full scale map on which the game is played
    

    Attributes:
        _width: 
        _height: 
    """

    #origin of coordinate system is top left of window
    width, height = 1500, 500


    def __init__(self):

        self.window = pygame.display.set_mode((self.width,self.height))
        #the list of all objects to update for each draw cycle
        self.draw_list = []


    def fill_screen(self,rgb_tuple):
        self.window.fill(rgb_tuple)

    def update_visual(self):
        pygame.display.flip()

#example of a simple game
def map_test():
    pygame.init()
    #initialize our map
    game_map = spike_map()

    red_circ = moveable_test(100,50,12)
    red_circ_controller = moveable_controller(red_circ)



    #initialize clock so it doesn't go infinitely
    clock = pygame.time.Clock()

    #make screen white
    game_map.fill_screen((255,255,255))
    
    #rectangle test
    example_rectangle = pygame.Rect(600,200,60,60)
    
    run = True
    
    while run:
        #ensure won't go above 60 FPS
        clock.tick(60)

        #quit the game if needed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #check for keypress
            if event.type == pygame.KEYDOWN:
                #theres an if statement in this method, wont move indiscriminantly
                red_circ_controller.move(event)
            if event.type == pygame.KEYUP:
                red_circ_controller.stop_move(event)

        red_circ_controller.still_moving()
        #make screen white
        game_map.fill_screen((255,255,255))
        #draw the red circle
        red_circ.draw_circ(game_map)
        #draw rectangle
        pygame.draw.rect(game_map.window,(100,100,0),example_rectangle)
        #update window
        game_map.update_visual()
    pygame.quit()




