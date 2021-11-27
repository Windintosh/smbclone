from pico2d import *

import collision
import server


class World:
    def __init__(self):
        self.image = load_image('assets/106583.png')
        self.x, self.y = 2500, 200

    def update(self):
        if collision.collide(self, server.mario):
            server.mario.y = 43
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        # fill here
        return 0, 0, 2500, 43