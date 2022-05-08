"""
Test library functions to find and identify protein-coding genes in DNA.
"""
import pytest
import math
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
    

    starting_bullet_count = 0

    the_gun = gun()
    for _ in range(shots_fired):
        the_gun.shoot(player_x,player_y,theta)
    
    global bullet_dictionary
    name = f"bullet_{shots_fired}"
    assert bullet_dictionary[name]

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


