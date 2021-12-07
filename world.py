from pico2d import *

import collision
import server


class World:
    def __init__(self):
        self.image = load_image('assets/106583.png')
        self.x, self.y = 2500, 200

    def update(self):
        # if collision.collide(self, server.mario):
        #     server.mario.y = 43
        #     server.mario.falling = 0
        if collision.collide(self, server.goomba):
            server.goomba.y = 40 # mario - 3px
        if collision.collide(self, server.koopa):
            server.koopa.y = 43
        if collision.collide(self, server.hbro):
            server.hbro.y = 43
        if collision.collide(self, server.bowser):
            server.bowser.y = 47 # mario + 4px
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(0, 0, 2500, 31)

    def get_bb(self):
        # fill here
        return 0, 0, 2500, 31