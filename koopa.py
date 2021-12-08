from pico2d import *

import collision
import game_framework
import game_world
import server

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

SLIDE_SPEED_KMH = 30
SLIDE_SPEED_MPM = (SLIDE_SPEED_KMH * 1000.0 / 60.0) #meter per minute
SLIDE_SPEED_MPS = (SLIDE_SPEED_MPM / 60.0) #METER PER SECOND
SLIDE_SPEED_PPS = (SLIDE_SPEED_MPS * PIXEL_PER_METER) #pixel per second

class Koopa:
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/koopa_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.state = 2
        self.speed = 1
        self.sliding = 0
        self.stomp_sound = load_wav('assets/smb_stomp.wav')
        self.kick_sound = load_wav('assets/smb_kick.wav')

    def shell(self):
        self.speed = 0
        self.dir = 0

    def slide(self):
        if self.dir == 0:
            self.dir = server.mario.dir
            pass
        self.x += self.dir * SLIDE_SPEED_PPS * game_framework.frame_time

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 12, self.x + 8, self.y + 12

    def draw(self):
        if self.state == 1:
            self.image = load_image('assets/shell_sprite.png')
            self.image.clip_draw(16, 0, 16, 15, self.x, self.y)
        else:
            if self.dir == 1:
                self.image.clip_composite_draw(int(self.frame) * 16, 0, 16, 24, 0, 'h', self.x, self.y, 16, 16)

            elif self.dir == -1:
                self.image.clip_draw(int(self.frame) * 16, 0, 16, 24, self.x, self.y)

    def update(self):
        if self.dir == -1:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time * self.speed
        else:
            self.x += RUN_SPEED_PPS * game_framework.frame_time * self.speed
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.y -= FALL_SPEED_PPS * game_framework.frame_time


        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1

        elif self.state == 1:
            if self.y <= 0:
                self.state = 0
            if collision.collide(self, server.mario): #
                if server.mario.jumping == 1 or server.mario.falling == 1:
                    server.mario.y += 20
                    if self.sliding == 0:
                        self.sliding = 1
                    else:
                        self.sliding = 0
                else:
                    if self.sliding == 0:
                        self.sliding = 1
                    else:
                        self.sliding = 0
                    if self.sliding == 1:
                        self.slide()
                    else:
                        self.shell()

            if self.sliding == 1: #
                self.slide()
            else:
                self.shell()

        elif self.state == 2: #
            if self.y <= 0:
                self.state = 0
            if collision.collide(self, server.mario):
                if server.mario.jumping == 1 or server.mario.falling == 1:
                    self.state = 1
                    server.mario.y += 20
                else:
                    if server.mario.state == 1:
                        server.mario.state = 0
                    else:
                        server.mario.state = 1

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass