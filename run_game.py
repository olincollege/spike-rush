
import pygame
import os
from regex import E
from guns_bullets import *
from abc import ABC, abstractmethod
from spike import *
from spike_map import *
from agent import *
from hud import display_model, display_view

def agent_test():
    """
    Runs the game loop.
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
    character_view_1 = AgentView(character_model_1, 'blue_sprite.png')
    character_controller_1 = AgentController(
        character_model_1, character_view_1)

    # Player 2 instance
    character_model_2 = Agent(0, 0, "defense")
    character_view_2 = AgentView(character_model_2, 'red_sprite.png')
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

        check_win(character_controller_1.agent,character_controller_2.agent)


        if character_controller_1.agent.win:

            #do stuff if the attacker wins
            break
        
        if character_controller_2.agent.win:
            #do stuff if defender wins
            break



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
        #map_view.draw_map()
        map_view.draw_map()

        # print(character_model_1.alive)
        if character_model_1.alive:

            character_controller_1.move(
                character_speed, keys, "WASD", map_model._wall_list)

            character_controller_1.check_shoot(keys, "WASD")
            character_controller_1.check_reload(keys, "WASD")

            character_view_1.draw_agent(map_view._window)
            character_view_1.dot_sight(map_view._window)

            character_controller_1.spike_plant(keys, map_model, "WASD", hud_model)

        # print(character_model_2.alive)
        if character_model_2.alive:

            character_controller_2.move(
                character_speed, keys, "Arrow", map_model._wall_list)


            character_controller_2.check_shoot(keys,"Arrow")
            character_controller_2.check_reload(keys,"Arrow")

            character_view_2.draw_agent(map_view._window)
            character_view_2.dot_sight(map_view._window)

            character_controller_2.spike_defuse(keys, map_model, "Arrow", agents[0], hud_model)





        # update stuff
        # draw backdrop
    

        # walls will still have collision even if not drawn
        # map_view.draw_walls()

        # draw HUD updates

        hud_view.draw_player_updates(
            character_model_1, character_model_2, map_view._window)
        hud_view.draw_game_timer(map_view._window)

        # draw spike
        character_view_1.draw_spike(map_view._window)
        character_view_2.draw_spike(map_view._window)


        character_controller_2.update_bullets_test(map_model._wall_list,
                                                   agent_list, agents[0])
        character_view_2.draw_bullets(map_view._window)
        character_controller_1.update_bullets_test(map_model._wall_list,
                                                   agent_list, agents[1]
                                                   )
        character_view_1.draw_bullets(map_view._window)

        pygame.display.flip()  # update entire display
        clock.tick(30)  # reduce framerate to 30

    # print(map_view._window.get_rect()) #check window dimensions
    pygame.quit()  # after main loop has finished
