
import pygame
from regex import E
from guns_bullets import *
from abc import ABC, abstractmethod
from spike import *
from spike_map import *
from agent import *
from hud import DisplayModel, DisplayView


def agent_test():
    """
    Runs the game loop.
    """
    pygame.init()  # initialize pygame
    FRAME_RATE = 30
    map_model = split_model()
    map_view = split_view(map_model)  # initialize map

    # initialize HUD
    hud_model = DisplayModel()
    hud_view = DisplayView(hud_model)

    clock = pygame.time.Clock()  # to keep track of time in-game

    # Intro screens here
    intro_screens = ["title.png", "instructions_1.png", "instructions_2.png",
                     "instructions_3.png"]
    for screen in intro_screens:
        display = True
        while display:
            for event in pygame.event.get():  # look for events
                if event.type == pygame.QUIT:  # quit the game, stop the loop
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    display = False
            hud_view.draw_other_screen(screen, map_view._window)

            pygame.display.flip()  # update entire display
            clock.tick(30)  # reduce framerate to 30

    character_speed = 10

    track_second = pygame.USEREVENT  # using ID 24

    # trigger event every second
    pygame.time.set_timer(track_second, 1000)

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

        check_win(character_controller_1.agent, character_controller_2.agent,
                  hud_model)

        if character_controller_1.agent.win:

            # do stuff if the attacker wins
            break

        if character_controller_2.agent.win:
            # do stuff if defender wins
            break

        # sense inputs (get events)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                pygame.quit()

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
        # map_view.draw_map()
        map_view.draw_map()

        # print(character_model_1.alive)
        if character_model_1.alive:

            character_controller_1.move(
                character_speed, keys, "WASD", map_model._wall_list)

            character_controller_1.check_shoot(keys, "WASD")
            character_controller_1.check_reload(keys, "WASD")

            character_view_1.draw_agent(map_view._window)
            character_view_1.dot_sight(map_view._window)

            character_controller_1.spike_plant(
                keys, map_model, "WASD", hud_model)

        # print(character_model_2.alive)
        if character_model_2.alive:

            character_controller_2.move(
                character_speed, keys, "Arrow", map_model._wall_list)

            character_controller_2.check_shoot(keys, "Arrow")
            character_controller_2.check_reload(keys, "Arrow")

            character_view_2.draw_agent(map_view._window)
            character_view_2.dot_sight(map_view._window)

            character_controller_2.spike_defuse(
                keys, map_model, "Arrow", agents[0], hud_model)

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
        clock.tick(FRAME_RATE)  # reduce framerate to 30

    # Trigger win screen
    display = True
    while display:
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                display = False
        if character_model_1.win == True:
            hud_view.draw_other_screen("attack_win.png", map_view._window)
        elif character_model_2.win == True:
            hud_view.draw_other_screen("defend_win.png", map_view._window)
        pygame.display.flip()  # update entire display
        clock.tick(FRAME_RATE)  # reduce framerate to 30

    pygame.quit()


agent_test()
