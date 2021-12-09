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
import main_state
from mushroom import Mushroom
from hammer import Hammer
from fireball import Fireball
import random

class Itemblock:
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/itemblock_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.speed = 0
        self.state = 1
        self.item_appear_sound = load_wav('assets/smb_powerup_appears.wav')
        self.item_appear_sound.set_volume(32)
        self.item_acquire_sound = load_wav('assets/smb_powerup.wav')
        self.item_acquire_sound.set_volume(32)

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        if self.state == 1:
            self.image.clip_draw(0, 0, 16, 16, self.x, self.y)
        else:
            self.image.clip_draw(16, 0, 16, 16, self.x, self.y)

    def spawn_item(self):
        mushroom = Mushroom(self.x, self.y + 16)
        game_world.add_object(mushroom, 1)
        pass

    def update(self):
        if collision.collide(self, server.mario):
            if server.mario.y - 12 >= self.y:  # mario is above
                server.mario.y = self.y + 19
                server.mario.falling = 0
                pass
            elif self.y >= server.mario.y + 12:  # mario is below
                if server.mario.jumping == 1:
                    server.mario.y = self.y - 24
                    server.mario.jumping = 0
                    server.mario.falling = 1
                    if self.state == 1:
                        self.state = 0
                        self.spawn_item()
                    pass
            elif server.mario.x >= self.x:  # mario is right
                # server.mario.x += server.mario.speed * game_framework.frame_time
                server.mario.bump = 1
                server.mario.x = self.x + 16
                pass
            elif self.x >= server.mario.x:  # mario is left
                # server.mario.x -= server.mario.speed * game_framework.frame_time
                server.mario.bump = 1
                server.mario.x = self.x - 16
                pass
        if collision.collide(self, server.goomba):
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
        if collision.collide(self, server.koopa):
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
        if collision.collide(self, server.hbro):
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
        if main_state.level == 2:
            if collision.collide(self, server.goomba2):
                if server.goomba2.y - 12 >= self.y:  # goomba is above
                    server.goomba2.y = self.y + 19
                    server.goomba2.falling = 0
                    pass
                elif self.y >= server.goomba2.y + 12:  # goomba is below
                    server.goomba2.y = self.y - 12
                    pass
                elif server.goomba2.x >= self.x:  # goomba is right
                    server.goomba2.x = self.x + 16
                    server.goomba2.dir = server.goomba2.dir * -1
                    pass
                elif self.x >= server.goomba2.x:  # goomba is left
                    server.goomba2.x = self.x - 16
                    server.goomba2.dir = server.goomba2.dir * -1
                    pass
                pass
            if collision.collide(self, server.koopa2):
                if server.koopa2.y - 12 >= self.y:  # koopa is above
                    server.koopa2.y = self.y + 19
                    server.koopa2.falling = 0
                    pass
                elif self.y >= server.koopa2.y + 12:  # koopa is below
                    server.koopa2.y = self.y - 12
                    pass
                elif server.koopa2.x >= self.x:  # koopa is right
                    server.koopa2.x = self.x + 16
                    server.koopa2.dir = server.koopa2.dir * -1
                    pass
                elif self.x >= server.koopa2.x:  # koopa is left
                    server.koopa2.x = self.x - 16
                    server.koopa2.dir = server.koopa2.dir * -1
                    pass
                pass
            if collision.collide(self, server.hbro2):
                if server.hbro2.y - 12 >= self.y:  # hbro is above
                    server.hbro2.y = self.y + 19
                    server.hbro2.falling = 0
                    pass
                elif self.y >= server.hbro2.y + 12:  # hbro is below
                    server.hbro2.y = self.y - 12
                    pass
                elif server.hbro2.x >= self.x:  # hbro is right
                    server.hbro2.x = self.x + 16
                    pass
                elif self.x >= server.hbro2.x:  # hbro is left
                    server.hbro2.x = self.x - 16
                    pass
                    pass
        if collision.collide(self, server.bowser):
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

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass