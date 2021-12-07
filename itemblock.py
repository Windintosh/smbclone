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

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.clip_draw(0, 0, 16, 16, self.x, self.y)

    def update(self):
        if self.state == 0:
            self.image.clip_draw(16, 0, 16, 16, self.x, self.y)
            self.x, self.y = -1, -1