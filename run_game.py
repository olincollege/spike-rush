"""
Run the game
"""
import pygame
from players_guns_bullets import *
from test_map import *
import random

frame_rate = 60

def guns_test():

    
    pygame.init()
    # initialize our map
    game_map = test_map()

    the_gun = random.choice(gun_list)
    red_circ = player_test(100, 50, 12, the_gun)
    red_circ_controller = player_test_controller(red_circ)

    # initialize clock so it doesn't go infinitely
    clock = pygame.time.Clock()

    # make screen white
    game_map.fill_screen((255, 255, 255))

    # rectangle test
    example_rectangle = pygame.Rect(600, 200, 60, 60)

    top_rect = pygame.Rect(0, 0, 1500, 3)
    bottom_rect = pygame.Rect(0, 497, 1500, 3)
    left_rect = pygame.Rect(0, 0, 3, 500)
    right_rect = pygame.Rect(1497, 0, 3, 500)
    collision_checks = [example_rectangle,
                        bottom_rect, left_rect, top_rect, right_rect]
    run = True

    print("made it to run loop")

    while run:


        # ensure won't go above 60 FPS
        clock.tick(frame_rate)

        # quit the game if needed
        red_circ_controller.check_still_shooting()

        red_circ_controller.player.frames_since_last_shot += 1
        # blank for now but could be useful
        # if pygame.event.get() is None:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # check for keypress
            if event.type == pygame.KEYDOWN:
                # theres an if statement in this method, wont move indiscriminantly
                red_circ_controller.move(event)
            if event.type == pygame.KEYUP:
                red_circ_controller.stop_move(event)
           
            red_circ_controller.check_shoot(event)
            red_circ_controller.check_reload(event)

        # this should probably be in a function
        if red_circ_controller.player.is_reloading:
            red_circ_controller.player.frames_since_reload += 1

        red_circ_controller.still_moving()
        # make screen white
        game_map.fill_screen((255, 255, 255))
        # draw the red circle
        red_circ.draw_circ(game_map)
        # draw rectangle

        for rectangle in collision_checks:
            pygame.draw.rect(game_map.window, (0, 150, 0), rectangle)

        update_bullets_for_guns_test(collision_checks)
        draw_bullets(game_map)
        # update window
        game_map.update_visual()
    pygame.quit()
