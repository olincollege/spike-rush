"""
For the Enemy AI
"""
from players_guns_bullets import *

#Let's code WII TANKS BABYYYYYYYYYYY

#maybe this should be a controller


example_rectangle = pygame.Rect(600, 200, 60, 60)
top_rect = pygame.Rect(0, 0, 1500, 3)
bottom_rect = pygame.Rect(0, 497, 1500, 3)
left_rect = pygame.Rect(0, 0, 3, 500)
right_rect = pygame.Rect(1497, 0, 3, 500)
vision_checks = [example_rectangle, bottom_rect, left_rect, top_rect, right_rect]

enemy_1_vision_collide_list = vision_checks

class basic_enemy_controller(player_test_controller):
    
    def __init__(self,enemy,player):

        self.enemy = enemy
        self.player = player #the player
    def enemy_main(self):

        self.check_see_player()

        if self.enemy.see_player:
            print("player seen")
            self.shoot()


    def shoot(self):
        if self.enemy.frames_since_reload < self.enemy.gun.frames_for_reload \
            and self.player.is_reloading:
            return
        elif self.enemy.is_reloading:
            self.enemy.is_reloading = False
        
        if self.enemy.frames_since_last_shot >= \
            self.enemy.gun.frames_before_shot and self.enemy.gun.current_clip != 0:
            

            self.enemy.gun.shoot(self.enemy.xpos,self.enemy.ypos,self.player.xpos,self.player.ypos)

            self.enemy.frames_since_last_shot = 0
            self.enemy.gun.consecutive_bullets = 1

            self.player.frames_since_last_shot += 1

        

    def check_see_player(self):
        """
        check if the enemy can see the player
        """
        player_x = self.player.xpos
        player_y = self.player.ypos


        norm_value = ((self.enemy.xpos -player_x)**2 + (self.enemy.ypos -player_y)**2)**.5
        x_incr = (self.enemy.xpos - player_x)/norm_value
        y_incr = (self.enemy.ypos - player_y)/norm_value

        vision_bullet = bullet(self.enemy.xpos,self.enemy.ypos,x_incr,y_incr,0)
        print("vision bullet created")
        self.invisible_bullet_main(vision_bullet)

    def invisible_bullet_main(self,vision_bullet):

        """
        vision_collide_list is a list of rectangles that block vision
        not necessarilly that block bullets. its global
        """
        global enemy_1_vision_collide_list

        distance_from_seer = ((self.enemy.xpos - vision_bullet.pos_x)**2 + (self.enemy.ypos - vision_bullet.pos_y)**2)**.5
        
        while distance_from_seer < self.enemy.vision_radius:
            print("bullet updating")
            #check if hitting player
            if vision_bullet.check_basic_collision(self.player.rect):
                print("enemy sees you")
                self.enemy.see_player = True
                return
                
            for vision_obstacle in enemy_1_vision_collide_list:
                print("collision checked")
                if vision_bullet.check_basic_collision(vision_obstacle):
                    self.enemy.see_player = False
                    return
            
            vision_bullet.update_position()
        #if you exceed the maximum distance, then the enemy doesn't see you
        self.enemy.see_player = False



class basic_enemy(player_test):


    health = 100
    see_player = False

    #how far the dude can see
    vision_radius = 150

    def __init__(self,player,x_init,y_init,radius,a_gun):
        self.player = player #not the enemy
        self.xpos = x_init
        self.ypos = y_init
        self.radius = radius
        #instance of the gun class
        self.gun = a_gun

    


