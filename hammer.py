from pico2d import *

import collision
import game_world
import game_framework
import server

HAMMER_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
HAMMER_SPEED_KMH = 50 # kmh
HAMMER_SPEED_MPM = (HAMMER_SPEED_KMH * 1000.0 / 60.0) #meter per minute
HAMMER_SPEED_MPS = (HAMMER_SPEED_MPM / 60.0) #METER PER SECOND
HAMMER_SPEED_PPS = (HAMMER_SPEED_MPS * HAMMER_PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Hammer:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Hammer.image == None:
            Hammer.image = load_image('assets/hammer_sprite.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.state = 1

    def get_bb(self):
        # fill here
        return self.x - 7, self.y - 7, self.x + 7, self.y + 7

    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(int(self.frame) * 14, 0, 14, 14, self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame) * 14, 0, 14, 14, 0, 'h', self.x, self.y, 14, 14)

    def update(self):
        self.x += self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.x < 25 or self.x > 1600 - 25:
            self.state = 0
        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1
        else:
            if collision.collide(self, server.mario):
                if server.mario.state == 1:
                    server.mario.state = 0
                    self.state = 0
                else:
                    server.mario.state = 1
                    self.state = 0
                print('mario hit by hammer')

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass
