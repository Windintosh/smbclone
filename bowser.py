from pico2d import *
import game_framework
from hammer import Hammer
import game_world

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 10.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

HAMMER_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
HAMMER_SPEED_KMH = 50 # kmh
HAMMER_SPEED_MPM = (HAMMER_SPEED_KMH * 1000.0 / 60.0) #meter per minute
HAMMER_SPEED_MPS = (HAMMER_SPEED_MPM / 60.0) #METER PER SECOND
HAMMER_SPEED_PPS = (HAMMER_SPEED_MPS * HAMMER_PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8

#action with timer, jump
class Bowser:
    def __init__(self):
        self.x, self.y = 300, 42
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/bowser_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.state = 0
        self.speed = 0
        self.timer = 30
    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 32, 0, 32, 32, 0, 'h', self.x, self.y, 32, 32)

        elif self.dir == -1:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 32, self.x, self.y)

    def update(self):
        if self.dir == -1:
            self.x -= RUN_SPEED_PPS * game_framework.frame_time
        else:
            self.x += RUN_SPEED_PPS * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def throw_hammer(self):
        hammer = Hammer(self.x, self.y, self.dir * HAMMER_SPEED_PPS * game_framework.frame_time)
        game_world.add_object(hammer, 1)
        pass