"""
Run the game
"""
import pygame
from players_guns_bullets import *
from game_map import *

def guns_test():
    pygame.init()
    #initialize our map
    game_map = spike_map()

    the_gun = gun()
    red_circ = player_test(100,50,12,the_gun)
    red_circ_controller = player_test_controller(red_circ)



    #initialize clock so it doesn't go infinitely
    clock = pygame.time.Clock()

    #make screen white
    game_map.fill_screen((255,255,255))
    
    #rectangle test
    example_rectangle = pygame.Rect(600,200,60,60)
    
    top_rect = pygame.Rect(0,0,1500,3)
    bottom_rect = pygame.Rect(0,497,1500,3)
    left_rect = pygame.Rect(0,0,3,500)
    right_rect = pygame.Rect(1497,0,3,500)
    collision_checks = [example_rectangle,bottom_rect,left_rect,top_rect,right_rect]
    run = True
    
    print("made it to run loop")
    while run:
        #ensure won't go above 60 FPS
        clock.tick(60)

        #quit the game if needed
        red_circ_controller.check_still_shooting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #check for keypress
            if event.type == pygame.KEYDOWN:
                #theres an if statement in this method, wont move indiscriminantly
                red_circ_controller.move(event)
            if event.type == pygame.KEYUP:
                red_circ_controller.stop_move(event)
            #print("made it to check shoot")
            red_circ_controller.check_shoot(event)


        red_circ_controller.still_moving()
        #make screen white
        game_map.fill_screen((255,255,255))
        #draw the red circle
        red_circ.draw_circ(game_map)
        #draw rectangle
        #print("made it to draw example rectangle")
        
        
        for rectangle in collision_checks:
            pygame.draw.rect(game_map.window,(0,150,0),rectangle)

        update_bullets_for_guns_test(collision_checks)
        draw_bullets(game_map)
        #print("made it to draw bullets")
        #update window
        game_map.update_visual()
    pygame.quit()
