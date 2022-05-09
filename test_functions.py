"""
Test library functions to find and identify protein-coding genes in DNA.
"""
import pytest
import math
import pygame
from agent import (
    Agent,
    AgentController
)
from guns_bullets import (
    bullet,
    gun,
)


# gun and bullet test cases


update_clip_cases = [
    # basic reload
    (1, 20),
    # arbitrarily large input reload
    (1234, 20),
    # single bullet clip decrease
    (-1, 19),
    # large clip decrease
    (-5, 15),
    # no bullet fired
    (0, 20),
    # clip can't go negative
    (-25, 0)
]

# testing shoot functionality

shoot_ammo_cases = [
    # default position and angle
    (0, 0, 0),
    # positive angles
    (1, 5, 10),
    # negative positions and >360 degree angle
    (-5, -10, 3*math.pi),
]

bullet_creation_cases = [
    # firing one shot
    (0, 0, 0, 1),
    # firing ten shots
    (0, 0, 0, 10),
    # firing 2 shots with arbitrary heading and start location
    (15, -15, math.pi, 2),

]

bullet_move_cases = [

    # horizontal movement
    (1, 0),
    # no movement
    (0, 0),
    # vertical movement
    (0, 1),
    # arbitrary angle
    (2, 1),
    # negative heading angles
    (-2, -1)

]

# I can't do this one
bullet_hit_cases = [

]


@pytest.mark.parametrize("input_value,output_clip",
                         update_clip_cases)
def test_update_clip(input_value, output_clip):
    """
    Check that updating the clip works properly

    Args:
        input value: An integer
        output_clip: An integer representing the expected number of bullets
            in a gun's clip after updating it.
    """
    the_gun = gun()
    the_gun.update_clip(input_value)
    assert the_gun.current_clip == output_clip


@pytest.mark.parametrize("player_x,player_y,theta",
                         shoot_ammo_cases)
def test_ammo_decrement(player_x, player_y, theta):
    """
    Test that the amount of ammo in a clip decreases when a bullet is shot

    Args:
        player_x: An integer representing the x coordinate of a player
        player_y: An integer representing the y coordinate of a player
        theta: An integer or float representing the aim angle of the player
    """
    the_gun = gun()
    the_gun.shoot(player_x, player_y, theta)
    assert the_gun.current_clip == 19


@pytest.mark.parametrize("player_x,player_y,theta,shots_fired",
                         bullet_creation_cases)
def test_bullet_creation(player_x, player_y, theta, shots_fired):
    """
    Test that when a gun is fired that the right number of bullets are created

    Args:
        player_x: An integer representing the x coordinate of a player
        player_y: An integer representing the y coordinate of a player
        theta: An integer or float representing the aim angle of the player
        shots_fired: An integer representing the number of bullets to shoot
    """

    the_gun = gun()
    for _ in range(shots_fired):
        the_gun.shoot(player_x, player_y, theta)

    assert len(the_gun._bullet_dict) == shots_fired


@pytest.mark.parametrize("incr_x,incr_y",
                         bullet_move_cases)
def test_move_bullet(incr_x, incr_y):
    """
    Test that bullets move through space as expected

    Args:
        incr_x: the heading of the bullet in the x direction, a float
        incr_y: the heading of the bullet in the y direction, a float
    """
    the_bullet = bullet(0, 0, incr_x, incr_y, 10)

    the_bullet.update_position()

    location = [the_bullet._pos_x, the_bullet._pos_y]
    assert location == [incr_x*the_bullet._speed_per_tick,
                        incr_y*the_bullet._speed_per_tick]


@pytest.mark.parametrize("incr_x,incr_y",
                         bullet_move_cases)
def test_bullet_hit(incr_x, incr_y):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.                                       @ADITI IASDFIJASPDFP%!$)_#!%I@!#)I@!I_#(%!#U(_%_!$#JOEPRW!$PTWEQMKF))
    """

    pass


# agent test cases
set_location_cases = [

    # x location, y location

    # positive coordinates
    (100, 100),
    # origin
    (0, 0),
    # negative coordinates
    (-1, -59999),
    # mixed coordinates
    (1235, -60),
]


@pytest.mark.parametrize("x_coord,y_coord",
                         set_location_cases)
def test_set_location(x_coord, y_coord):
    """
    Check that setting player location works correctly

    Args:
        x_coord: an integer representing the x coordinate to set for the
            player
        y_coord: an integer representing the y coordinate to set for the
            player
    """

    player = Agent(0, 0, "attack")

    player.set_x_coord(x_coord)
    player.set_y_coord(y_coord)

    location = [x_coord, y_coord]

    assert location == player.location


set_health_cases = [

    (0,),
    (1,),
    (5,),
    (-5,),
]


@pytest.mark.parametrize("health_update",
                         set_health_cases)
def test_set_health(health_update):
    """
    Check that setting the health of the player works as intended

    Args:
        health_update: an integer representing the amount of health to give
            the player
    """

    player = Agent(0, 0, "attack")
    player.update_health(health_update)

    assert health_update == player.health


# tests cases for set_is shooting, set_win, set_is reloading, and kill()
# these inputs do not affect each other at all and thus combinations do
# not need to be tested
set_boolean_cases = [

    # One true, rest false
    (True, False, False, False),
    (False, True, False, False),
    (False, False, True, False),
    (False, False, False, True),
    # All true
    (True, True, True, True)

]


@pytest.mark.parametrize("shooting,reloading,winning,killing",
                         set_boolean_cases)
def test_set_booleans(shooting, reloading, winning, killing):
    """
    Check that set boolean functions work as intended

    Args:
        shooting: a boolean representing if the player is shooting
        reloading: a boolean representing if the player is reloading
        winning: a boolean representing if the player has won
        killing: a boolean representing if the player is dead
    """

    player = Agent(0, 0, "attack")
    player.set_is_shooting(shooting)
    player.set_is_reloading(reloading)
    if winning:
        player.set_win()

    if killing:
        player.kill()

    bool_list = [player._is_shooting, player._is_reloading, player.win,
                 player.alive]

    assert bool_list == [shooting, reloading, winning, not killing]


# for frames since last shot,reload
set_frames_since_cases = [
    # 0 frames
    (0, 0),
    # small, positive frames
    (1, 5),
    # large number of frames
    (200, 500),

]


@pytest.mark.parametrize("last_shot,reloading",
                         set_frames_since_cases)
def test_set_frames(last_shot, reloading):
    """
    Check that functions setting the number of frames since some event work
    as intended.

    Args:
        last_shot: An integer representing the number of frames since a player
            shot their last shot
        reloading: An integer representing the number of frames since a player
            initiated a reload


    """

    player = Agent(0, 0, "attack")
    player.set_frames_since_last_shot(last_shot)
    player.set_frames_since_reload(reloading)

    frames_list = [player._frames_since_last_shot, player._frames_since_reload]

    assert frames_list == [last_shot, reloading]

    # Below. put test functions for Spike                                    @ADITI !O#@$_@!($#@!_)$)@#!)$@#!$)@#!$()_!%@#%I$@#!()#@!$(2143)
    # , hud if applicable, and anything else. unit test docstrings also need work
