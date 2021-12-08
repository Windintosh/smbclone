from pico2d import *
import collision
import game_framework
import game_world
import title_state
import world
import goomba
import koopa
import hbro
import bowser
import server
from hammer import Hammer
from fireball import Fireball
import random

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 10.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8

FALL_SPEED_KMH = 20
FALL_SPEED_MPM = (FALL_SPEED_KMH * 1000.0 / 60.0) #meter per minute
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0) #METER PER SECOND
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER) #pixel per second

class Mushroom:
    image = None
    def __init__(self, x = 100, y = 100):
        self.x, self.y = x, y
        self.ax, self.ay = self.x, self.y
        if Mushroom.image == None:
            Mushroom.image = load_image('assets/mushroom_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.speed = 0
        self.state = 1
        self.powerup_sound = load_wav('assets/smb_powerup.wav')

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        if self.y <= 0:
            self.state = 0

        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1
        else:
            if collision.collide(self, server.mario): #
                if server.mario.state == 1:
                    server.mario.state = 2
                    self.state = 0
                else:
                    self.state = 0
            pass

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass