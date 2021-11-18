from pico2d import *


class World:
    def __init__(self):
        self.image = load_image('assets/106583.png')
        self.x, self.y = 2500, 200

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_bb(self):
        # fill here
        return 0, 0, 2500, 43