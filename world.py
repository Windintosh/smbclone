from pico2d import *

import collision
import server
import game_framework


class World:
    def __init__(self): #
        self.image = load_image('assets/background_sky.png')
        self.x, self.y = 0, 0
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.bgm = load_music('assets/smb_metal.mp3')
        self.bgm.set_volume(100)
        self.bgm.repeat_play()

    def update(self):
        # self.window_left =clamp(0, int(server.mario.x) - server.world.canvas_width // 2, server.world.w - server.world.canvas_width)
        # self.window_bottom = clamp(0, int(server.mario.y) - server.world.canvas_height // 2, server.world.h -server.world.canvas_height)

        # if collision.collide(self, server.goomba):
        #     server.goomba.y = 40 # mario - 3px
        # if collision.collide(self, server.koopa):
        #     server.koopa.y = 43
        # if collision.collide(self, server.hbro):
        #     server.hbro.y = 43
        # if collision.collide(self, server.bowser):
        #     server.bowser.y = 47 # mario + 4px
        pass
        # if collision.collide(self, server.mushroom):
        #     server.mushroom.y = 40
    def draw(self):
        self.image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
        # self.image.clip_draw(576//2, 432//2, 576, 432, 0, 0)
        # self.image.clip_draw_to_origin(self.window_left, self.window_bottom, server.world.canvas_width,
        #                                server.world.canvas_height, 0, 0)
        # draw_rectangle(0, 0, 2500, 31)

    def get_bb(self):
        # fill here
        return 0, 0, 2500, 31

    def scroll(self):
        # if server.mario.x >= 350 and server.mario.speed >0:
        #     if server.mario.dash ==1:
        #         self.x -= server.mario.speed * game_framework.frame_time * 2
        #     else:
        #         self.x -= server.mario.speed * game_framework.frame_time
        #     pass
        pass