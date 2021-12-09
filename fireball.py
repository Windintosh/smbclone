from pico2d import *

import collision
import game_world
import game_framework
import main_state
import server

FB_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
FB_SPEED_KMH = 60 # kmh
FB_SPEED_MPM = (FB_SPEED_KMH * 1000.0 / 60.0) #meter per minute
FB_SPEED_MPS = (FB_SPEED_MPM / 60.0) #METER PER SECOND
FB_SPEED_PPS = (FB_SPEED_MPS * FB_PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Fireball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Fireball.image == None:
            Fireball.image = load_image('assets/fb_sprite.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.state = 1

    def get_bb(self):
        # fill here
        return self.x - 4, self.y - 4, self.x + 4, self.y + 4

    def draw(self):
        if self.velocity > 0:
            self.image.clip_draw(int(self.frame) * 8, 0, 8, 8, self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame) * 8, 0, 8, 8, 0, 'h', self.x, self.y, 8, 8)

    def update(self):
        self.x += self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)
        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1
        else:
            if collision.collide(self, server.goomba):
                server.goomba.state = 0
                self.state = 0
                print('hit goomba')
            elif collision.collide(self, server.koopa):
                server.koopa.state = 0
                self.state = 0
                print('hit koopa')
            elif collision.collide(self, server.hbro):
                server.hbro.state = 0
                self.state = 0
                print('hit hammer bro')
            elif collision.collide(self, server.bowser):
                server.bowser.hp -= 1
                self.state = 0
                print('hit bowser')
            if main_state.level == 2:
                if collision.collide(self, server.goomba2):
                    server.goomba2.state = 0
                    self.state = 0
                    print('hit goomba2')
                elif collision.collide(self, server.koopa2):
                    server.koopa2.state = 0
                    self.state = 0
                    print('hit koopa2')
                elif collision.collide(self, server.hbro2):
                    server.hbro2.state = 0
                    self.state = 0
                    print('hit hammer bro2')

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass