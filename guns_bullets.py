import math
from random import randint, randrange
import pygame
#from run_game import frame_rate

frame_rate = 30

# global bc GLBOAL fsduckjscajkajsdajk;

# ... would not recomend unglobaling. wait, not how global vars work, fixing

# fixed, these 3 things should always be referred to as global
# initialize an empty dictionary that will store all bullets
bullet_dictionary = {}
# initialize a counter for bullets
bullet_counter = 0
# bullets to delete, fixes deleting during iteration issue
bullet_delete_dictionary = {}

# GUN


class gun():
    """
    A model for a gun.

    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.


    """
    #gun should have name and defined damage value
    _damage = 20

    _max_spread = math.ceil(frame_rate * 40/60)
    _min_spread = 0
    _shots_for_full_spread = 7
    _frames_before_shot = math.ceil(frame_rate*15/60)

    # the consecutive number of bullets automatically fire(for calculating spread)
    consecutive_bullets = 0

    _clip_size = 20
    _frames_for_reload = math.ceil(frame_rate*120/60) # 2 seconds

    current_clip = 20

    # upon further consideration, it doesn't make much sense to keep track of these things
    # if we're not updating the gun's position as we go, we should probably implement that tho

    def __init__(self):
        """
        Initialize an instance of the gun class
        """
        self._automatic = True
        self._bullet_dict = {}
        #self.bullet_count = 0
        self._bullet_delete_dict = {}

    def update_clip(self, clip_update):
        """
        Update the number of available bullet for a gun to fire

        Args:
            clip_update: An integer representing the number of bullets to
                subtract from the current clip if negative or if to reload
                if positive.
        Returns:
            None.
        """
        # function handles reloading and decreasing clip from shooting
        # a negative integer means a shot has been fired, decrease clip
        if clip_update <= 0:
            self.current_clip += clip_update
            # if clip is negative
            if self.current_clip < 0:
                self.current_clip = 0
        # otherwise reload
        else:
            self.current_clip = self._clip_size

    def shoot(self, player_x, player_y, theta):
        """
        Calculate a bullet's heading, add spread, and initialize a bullet's
        movement.

        Args:
            player_x: An integer representing the location of the player's
                x position.
            player_y: An integer representing the location of the player's
                y position.
            theta: An integer or float representing the current angle the 
                player is facing in radians.
        Returns:
            None.
        """
        #theta in radians
        x_increment = math.cos(theta)
        y_increment = math.sin(theta)
        
        #doing spread
        perp_vector = [-y_increment,x_increment]
        
        #account for 0 division
        if self._shots_for_full_spread != 0:
            this_bullet_max_spread = self._max_spread*self.consecutive_bullets \
          / self._shots_for_full_spread
        else:
            this_bullet_max_spread = self._max_spread
        spread_factor = self._min_spread
        if self._min_spread < math.ceil(this_bullet_max_spread):
            spread_factor = randint(self._min_spread,math.ceil(this_bullet_max_spread))

        actual_spread_x = perp_vector[0] * \
            spread_factor * (-1)**(randint(0, 1))
        actual_spread_y = perp_vector[1] * \
            spread_factor * (-1)**(randint(0, 1))

        # if you increase this by a factor of 10, increase the max spread by a factor of 10 too
        # basically will just allow you more spread angles :)
        x_increment += actual_spread_x/1000
        y_increment += actual_spread_y/1000

        bullet_start_x = player_x + math.floor(30*x_increment) + 25
        bullet_start_y = player_y + math.floor(30*y_increment) + 25

        # create a new bullet and add it to the dictionary of bullets
        global bullet_counter
        bullet_counter += 1
        new_bullet = bullet(bullet_start_x, bullet_start_y, x_increment, \
                            y_increment, self._damage)

        update_dict = {new_bullet.name: new_bullet}

        self._bullet_dict.update(update_dict)

        # decrease clip size by 1
        self.update_clip(-1)

    def delete_bullet(self, bullet):
        """
        Delete a bullet from the game.

        Args:
            bullet: An instance of the bullet class.
        """
        self._bullet_delete_dict.update({bullet.name:self._bullet_dict[bullet.name]})

class bullet():
    """
    A model for a bullet.

    Attributes:
        _pos_x: An integer representing the x position of a bullet.
        _pos_y: An integer representing the y position of a bullet.
        _incr_x: An float representing the x component of a bullet's heading.
        _incr_y: An float representing the y component of a bullet's heading.
        _damage: An integer representing how much a damage a bullet should do
            on hit.
        _delta_x: A float representing how much a bullet should move in the x
            direction per timestep.
        _delta_y: A float representing how much a bullet should move in the y
            direction per timestep.
        name: A string representing the name of a bullet.
        bullet_sprite: A Sprite representing the bullet's sprite in the view;
            initialized as none.
        _speed_per_tick: an integer representing the speed the bullet moves
    """
    _speed_per_tick = math.ceil(frame_rate *35/60) # was 20

    def __init__(self, pos_x, pos_y, incr_x, incr_y, damage):
        """
        Initialize an instance of the bullet class

        Args:
            _pos_x: An integer representing the x position of a bullet.
            _pos_y: An integer representing the y position of a bullet.
            _incr_x: An float representing the x component of a bullet's heading.
            _incr_y: An float representing the y component of a bullet's heading.
            _damage: An integer representing how much a damage a bullet should
                do on hit.
        """
        #things necessary for calculating heading
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._incr_x = incr_x
        self._incr_y = incr_y
        #define bullet damage (based on gun stats)
        self._damage = damage

        self._delta_x = self._incr_x * self._speed_per_tick
        self._delta_y = self._incr_y * self._speed_per_tick

        global bullet_counter
        self.name = f"bullet_{bullet_counter}"

        self.bullet_sprite = None

    # update positions

    def update_position(self):
        """
        Update's the bullet's stored position in the model.

        Returns:
            None.
        """
        self._pos_x += self._delta_x
        self._pos_y += self._delta_y

    def set_sprite(self, sprite):
        """
        Set a sprite for a bullet

        Args:
            sprite: A sprite representing the sprite of the bullet in the view.
        Returns:
            None.
        """
        self.bullet_sprite = sprite

# defining general gun classes


class classic(gun):
    """
    A model for a gun that emulates the classic.

    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.
    """
    _damage = 22
    _max_spread = math.ceil(frame_rate * 50/60)
    _min_spread = 0
    _shots_for_full_spread = 7
    _frames_before_shot = math.ceil(frame_rate*10/60)
    
    consecutive_bullets = 0
    _clip_size = 12
    _current_clip = 12
    _frames_for_reload = math.ceil(frame_rate*105/60)

    def __init__(self):
        """
        Creates an instance of a classic.
        """
        self._automatic = False
        self._bullet_dict = {}
        self._bullet_delete_dict = {}


class spectre(gun):
    """
    A model for a gun that emulates the spectre.

    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.
    """
    _damage = 22
    _max_spread = math.ceil(frame_rate*70/60)
    _min_spread = 0
    _shots_for_full_spread = 9
    _frames_before_shot = math.ceil(frame_rate*5/60)
    
    consecutive_bullets = 0
    _clip_size = 30
    current_clip = 30
    _frames_for_reload = math.ceil(frame_rate*135/60)

    def __init__(self):
        """
        Creates an instance of the spectre class.
        """
        self._automatic = True
        self._bullet_dict = {}
        self._bullet_delete_dict = {}


class guardian(gun):
    """
    A model of a gun that emulates the guardian.

    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.
    """
    _damage = 65
    _max_spread = math.ceil(frame_rate*40/60)
    _min_spread = 0
    _shots_for_full_spread = 9
    _frames_before_shot = math.ceil(frame_rate*10/60)
    
    consecutive_bullets = 0
    _clip_size = 12
    current_clip = 12
    _frames_for_reload = math.ceil(frame_rate*135/60)

    def __init__(self):
        """
        Creates an instance of the guardian class.
        """
        self._automatic = False
        self._bullet_dict = {}
        self._bullet_delete_dict = {}


class vandal(gun):
    """
    A model of a gun that emulates the vandal.

    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.
    """
    _damage = 40
    _max_spread = math.ceil(frame_rate*120/60)
    _min_spread = math.ceil(frame_rate*10/60)
    _shots_for_full_spread = 8
    _frames_before_shot = math.ceil(frame_rate*6/60)
    
    consecutive_bullets = 0
    _clip_size = 25
    current_clip = 25
    _frames_for_reload = math.ceil(frame_rate*150/60)

    def __init__(self):
        """
        Creates an instance of the vandal class.
        """
        self._automatic = True
        self._bullet_dict = {}
        self._bullet_delete_dict = {}

# this one is special. ill get to it later


class operator(gun):
    """
    A model of a gun that emulates the Operator.

    (have to put in alt fire before this + other stuff)
    
    Attributes:
        _damage: An integer representing how much damage a bullet shot from
            this gun should do.
        _max_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _min_spread: An integer representing the maximum spread of a bullet
            shot from this gun.
        _shots_for_full_spread: An integer representing the number of bullets
            that must be shot from this gun before full spread is achieved.
        _frames_before_shot: An integer representing the number of frames that
            the player must wait before shooting from this gun after shooting
            from it before.
        consecutive_bullets: An integer representing a running counter of
            bullets shot consecutively
        _clip_size: An integer representing the maximum number of bullets that
            can be shot from this gun before reloading.
        _frames_for_reload: An integer representing the number of frames before
            an initiated reload is over for this gun.
        current_clip: An integer representing the current number of bullets
            held by a gun.
        _automatic: A boolean representing if a gun is automatic.
        _bullet_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun.
        _bullet_delete_dict: A dictionary containing bullet names as keys and 
            instances of the bullet class as values. Keeps track of all
            active bullets shot by this gun that need to be deleted.
    """
    _damage = 150
    _max_spread = math.ceil(frame_rate*40/60)
    _min_spread = 0
    _shots_for_full_spread = 9
    _frames_before_shot = math.ceil(frame_rate*80/60)
    
    consecutive_bullets = 0
    _clip_size = 5
    current_clip = 5
    _frames_for_reload = math.ceil(frame_rate*222/60)

    def __init__(self):
        """
        Creates an instance of the operator class.
        """
        self._automatic = False
        self._bullet_dict = {}
        self._bullet_delete_dict = {}
      
    pass

gun_list =[classic(),spectre(),guardian(),vandal()]