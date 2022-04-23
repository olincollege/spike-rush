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

    the_gun = gun(50,50)
    red_circ = player_test(100,50,12,the_gun)
    red_circ_controller = player_test_controller(red_circ)



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
            player_test_controller.check_shoot(event)


        red_circ_controller.still_moving()
        #make screen white
        game_map.fill_screen((255,255,255))
        #draw the red circle
        red_circ.draw_circ(game_map)
        #draw rectangle
        pygame.draw.rect(game_map.window,(100,100,0),example_rectangle)
        update_bullets(bullet_dictionary)
        draw_bullets(bullet_dictionary)
        #update window
        game_map.update_visual()
    pygame.quit()
