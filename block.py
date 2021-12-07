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

class Block:
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/block_sprite.png')
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
        self.image.draw(self.x, self.y, 16, 16)

    def update(self):
        if self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1