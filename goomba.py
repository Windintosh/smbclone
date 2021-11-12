from pico2d import *

class Goomba:
    def __init__(self):
        self.x, self.y = 240, 40
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/goomba_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(self.frame * 16, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

        elif self.dir == -1:
            self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

    def update(self):
        self.x -= 5

        self.frame = (self.frame + 1) % 2