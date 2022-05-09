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
    vandal,
    guardian,
    bullet_counter,
    bullet_dictionary,
    bullet_delete_dictionary

)


#gun and bullet test cases


update_clip_cases = [
    #basic reload
    (1,20),
    #arbitrarily large input reload
    (1234,20),
    #single bullet clip decrease
    (-1,19),
    #large clip decrease
    (-5,15),
    #no bullet fired
    (0,20),
    #clip can't go negative
    (-25,0)
]

#testing shoot functionality

shoot_ammo_cases = [
    #default position and angle
    (0,0,0),
    #positive angles
    (1,5,10),
    #negative positions and >360 degree angle
    (-5,-10,3*math.pi),
]

bullet_creation_cases = [
    #firing one shot
    (0,0,0,1),
    #firing ten shots
    (0,0,0,10),
    #firing 2 shots with arbitrary heading and start location
    (15,-15,math.pi,2),

]

bullet_move_cases = [

    #horizontal movement
    (1,0),
    #no movement
    (0,0),
    #vertical movement
    (0,1),
    #arbitrary angle
    (2,1),
    #negative heading angles
    (-2,-1)

]

#I can't do this one
bullet_hit_cases = [

]

@pytest.mark.parametrize("input_value,output_clip",\
    update_clip_cases)
def test_update_clip(input_value,output_clip):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    the_gun = gun()
    the_gun.update_clip(input_value)
    assert the_gun.current_clip == output_clip

@pytest.mark.parametrize("player_x,player_y,theta",\
    shoot_ammo_cases)
def test_ammo_decrement(player_x,player_y,theta):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    the_gun = gun()
    the_gun.shoot(player_x,player_y,theta)
    assert the_gun.current_clip == 19

@pytest.mark.parametrize("player_x,player_y,theta,shots_fired",\
    bullet_creation_cases)
def test_bullet_creation(player_x,player_y,theta,shots_fired):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    


    the_gun = gun()
    for _ in range(shots_fired):
        the_gun.shoot(player_x,player_y,theta)
    
    assert len(the_gun.bullet_dict) == shots_fired

@pytest.mark.parametrize("incr_x,incr_y",\
    bullet_move_cases)
def test_move_bullet(incr_x,incr_y):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    the_bullet = bullet(0,0,incr_x,incr_y,10)

    the_bullet.update_position()

    location = [the_bullet.pos_x,the_bullet.pos_y]
    assert location == [incr_x*the_bullet.speed_per_tick,\
        incr_y*the_bullet.speed_per_tick]



@pytest.mark.parametrize("incr_x,incr_y",\
    bullet_move_cases)
def test_bullet_hit(incr_x,incr_y):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    
    pass




#agent test cases

set_location_cases = [
    
    #x location, y location

    #positive coordinates
    (100,100),
    #origin
    (0,0),
    #negative coordinates
    (-1,-59999),
    #mixed coordinates
    (1235,-60),
]

@pytest.mark.parametrize("x_coord,y_coord",\
    set_location_cases)
def test_set_location(x_coord,y_coord):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """
    
    player = Agent(0,0,"attack")

    player.set_x_coord(x_coord)
    player.set_y_coord(y_coord)

    location = [x_coord,y_coord]

    assert location == player.location



set_health_cases = [

 (0,),
 (1,),
 (5,),
 (-5,),
]

@pytest.mark.parametrize("health_update",\
    set_health_cases)
def test_set_health(health_update):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """

    player = Agent(0,0,"attack")
    player.update_health(health_update)

    assert health_update == player.health

#tests cases for set_is shooting, set_is reloading, and kill()
#these inputs do not affect each other at all and thus combinations do
#not need to be tested
set_boolean_cases = [

    (True,False,False),
    (False,True,False),
    (False,False,True),
    (True,True,True)

]

@pytest.mark.parametrize("shooting,reloading,killing",\
    set_boolean_cases)
def test_set_booleans(shooting,reloading,killing):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """

    player = Agent(0,0,"attack")
    player.set_is_shooting(shooting)
    player.set_is_reloading(reloading)

    if killing:
        player.kill()

    bool_list = [player._is_shooting,player._is_reloading,player.alive]

    assert bool_list == [shooting,reloading,not killing]


#for frames since last shot,reload
set_frames_since_cases = [
    #0 frames
    (0,0),
    #small, positive frames
    (1,5),
    #large number of frames
    (200,500),

]

@pytest.mark.parametrize("last_shot,reloading",\
    set_frames_since_cases)
def test_set_frames(last_shot,reloading):
    """
    Check that find_most_frequent outputs correctly ordered dictionaries

    Args:
        freq_input_dict: A dictionary with strings as keys and positive
            integers as values.
        freq_input_int: An integer determining how many value ordered items to
            output.
        output_dict: A value ordered dictionary with strings as
            keys and integers as values.
    """

    player = Agent(0,0,"attack")
    player.set_frames_since_last_shot(last_shot)
    player.set_frames_since_reload(reloading)


    frames_list = [player._frames_since_last_shot,player._frames_since_reload]

    assert frames_list == [last_shot,reloading]

    