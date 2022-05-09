"""
Runs the spike rush game.
"""
# Pylint disables & justifications.

# pylint:disable=E1101
# Pylint is misunderstanding how pygame works & is blatantly wrong here.
# Pygame has an init function & represents keys presses with pygame.[Key],
# These are not attributes.

# pylint:disable = R0912, R0914, R0915
# The overall game loop requries updating of many variables meaning that
# it can't resolve for having "too many"
# Additoinally, it cannot avoid having so many branches and statements for the
# same reason.

import pygame
from spike_map import SplitModel, SplitView
from agent import Agent, AgentController, AgentView, check_win
from hud import DisplayModel, DisplayView

FRAME_RATE = 30

def agent_test():
    """
    Runs the game loop.

    Returns:
        None.
    """
    pygame.init()  # initialize pygame
    map_model = SplitModel()
    map_view = SplitView(map_model)  # initialize map

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
                    return
                if event.type == pygame.KEYDOWN:
                    display = False
            map_view.draw_other_screen(screen)

            pygame.display.flip()  # update entire display
            clock.tick(FRAME_RATE)  # reduce framerate to 30

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
                return

            if event.type == track_second:
                # if a second has passed, reduce the timer
                if hud_model.timer != 0:
                    hud_model.set_timer(hud_model.timer-1)


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
                character_speed, keys, "WASD", map_model.wall_list)

            character_controller_1.check_shoot(keys, "WASD")
            character_controller_1.check_reload(keys, "WASD")

            character_view_1.draw_agent(map_view.window)
            character_view_1.dot_sight(map_view.window)

            character_controller_1.spike_plant(
                keys, map_model, "WASD", hud_model)

        # print(character_model_2.alive)
        if character_model_2.alive:

            character_controller_2.move(
                character_speed, keys, "Arrow", map_model.wall_list)

            character_controller_2.check_shoot(keys, "Arrow")
            character_controller_2.check_reload(keys, "Arrow")

            character_view_2.draw_agent(map_view.window)
            character_view_2.dot_sight(map_view.window)

            character_controller_2.spike_defuse(
                keys, map_model, "Arrow", agents[0])

        # update stuff
        # draw backdrop

        # walls will still have collision even if not drawn
        # map_view.draw_walls()

        # draw HUD updates

        hud_view.draw_player_updates(
            character_model_1, character_model_2, map_view.window)
        hud_view.draw_game_timer(map_view.window)

        # draw spike
        character_view_1.draw_spike(map_view.window)
        character_view_2.draw_spike(map_view.window)

        character_controller_2.update_bullets_test(map_model.wall_list,
                                                   agent_list, agents[0])
        character_view_2.draw_bullets(map_view.window)
        character_controller_1.update_bullets_test(map_model.wall_list,
                                                   agent_list, agents[1]
                                                   )
        character_view_1.draw_bullets(map_view.window)

        # bring up controls screen if H key is pressed
        if keys[pygame.K_h]:
            map_view.draw_other_screen("controls.png")

        pygame.display.flip()  # update entire display
        clock.tick(FRAME_RATE)  # reduce framerate to 30

    # Trigger win screen
    display = True
    while display:
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # quit the game, stop the loop
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                display = False
        if character_model_1.win:
            map_view.draw_other_screen("attack_win.png")
        elif character_model_2.win:
            map_view.draw_other_screen("defend_win.png")
        pygame.display.flip()  # update entire display
        clock.tick(FRAME_RATE)  # reduce framerate to 30

    pygame.quit()


agent_test()
