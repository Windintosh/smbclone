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
RUN_SPEED_KMH = 20.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

class Block:
    image = None
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        if Block.image == None:
            Block.image = load_image('assets/block_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.speed = 0
        self.state = 1
        self.break_block_sound = load_wav('assets/smb_breakblock.wav')

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.draw(self.x, self.y, 16, 16)

    def update(self):
        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1
        else:
            if collision.collide(self, server.mario):
                if server.mario.y - 12 >= self.y:  # mario is above
                    server.mario.y = self.y + 19
                    server.mario.falling = 0
                    pass
                elif self.y >= server.mario.y + 12:  # mario is below
                    server.mario.y = self.y - 12
                    server.mario.jumping = 0
                    server.mario.falling = 1
                    self.state = 0
                    pass
                elif server.mario.x >= self.x:  # mario is right
                    # server.mario.x += server.mario.speed * game_framework.frame_time
                    server.mario.x = self.x + 16
                    pass
                elif self.x >= server.mario.x:  # mario is left
                    # server.mario.x -= server.mario.speed * game_framework.frame_time
                    server.mario.x = self.x - 16
                    pass
            elif collision.collide(self, server.goomba):
                if server.goomba.y - 12 >= self.y:  # goomba is above
                    server.goomba.y = self.y + 19
                    server.goomba.falling = 0
                    pass
                elif self.y >= server.goomba.y + 12:  # goomba is below
                    server.goomba.y = self.y - 12
                    pass
                elif server.goomba.x >= self.x:  # goomba is right
                    server.goomba.x = self.x + 16
                    server.goomba.dir = server.goomba.dir * -1
                    pass
                elif self.x >= server.goomba.x:  # goomba is left
                    server.goomba.x = self.x - 16
                    server.goomba.dir = server.goomba.dir * -1
                    pass
                pass
            elif collision.collide(self, server.koopa):
                if server.koopa.y - 12 >= self.y:  # koopa is above
                    server.koopa.y = self.y + 19
                    server.koopa.falling = 0
                    pass
                elif self.y >= server.koopa.y + 12:  # koopa is below
                    server.koopa.y = self.y - 12
                    pass
                elif server.koopa.x >= self.x:  # koopa is right
                    server.koopa.x = self.x + 16
                    server.koopa.dir = server.koopa.dir * -1
                    pass
                elif self.x >= server.koopa.x:  # koopa is left
                    server.koopa.x = self.x - 16
                    server.koopa.dir = server.koopa.dir * -1
                    pass
                pass
            elif collision.collide(self, server.hbro):
                if server.hbro.y - 12 >= self.y:  # hbro is above
                    server.hbro.y = self.y + 19
                    server.hbro.falling = 0
                    pass
                elif self.y >= server.hbro.y + 12:  # hbro is below
                    server.hbro.y = self.y - 12
                    pass
                elif server.hbro.x >= self.x:  # hbro is right
                    server.hbro.x = self.x + 16
                    pass
                elif self.x >= server.hbro.x:  # hbro is left
                    server.hbro.x = self.x - 16
                    pass
                pass
            elif collision.collide(self, server.bowser):
                if server.bowser.y - 12 >= self.y:  # bowser is above
                    server.bowser.y = self.y + 19
                    server.bowser.falling = 0
                    pass
                elif self.y >= server.bowser.y + 12:  # bowser is below
                    server.bowser.y = self.y - 12
                    pass
                elif server.bowser.x >= self.x:  # mario is right
                    server.bowser.x = self.x + 16
                    pass
                elif self.x >= server.bowser.x:  # mario is left
                    server.bowser.x = self.x - 16
                    pass
                pass

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass