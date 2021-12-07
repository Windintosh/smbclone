from pico2d import *
import game_framework
from hammer import Hammer
import game_world
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import server

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 10.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

HAMMER_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
HAMMER_SPEED_KMH = 30 # kmh
HAMMER_SPEED_MPM = (HAMMER_SPEED_KMH * 1000.0 / 60.0) #meter per minute
HAMMER_SPEED_MPS = (HAMMER_SPEED_MPM / 60.0) #METER PER SECOND
HAMMER_SPEED_PPS = (HAMMER_SPEED_MPS * HAMMER_PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8

FALL_SPEED_KMH = 20
FALL_SPEED_MPM = (FALL_SPEED_KMH * 1000.0 / 60.0) #meter per minute
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0) #METER PER SECOND
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER) #pixel per second

#action with timer, jump
class Bowser:
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/bowser_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.speed = 0
        self.htimer = 1
        self.jtimer = 1
        self.hp = 10
        self.build_behavior_tree()

    def get_bb(self):
        # fill here
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 32, 0, 32, 32, 0, 'h', self.x, self.y, 32, 32)

        elif self.dir == -1:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 32, self.x, self.y)

    def update(self):
        if self.hp > 0:
            self.bt.run()
            if self.dir == -1:
                pass
            else:
                pass
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.y -= FALL_SPEED_PPS * game_framework.frame_time

        elif self.hp == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1
            print('bowser is dead')

    def throw_hammer(self):
        self.htimer -= game_framework.frame_time
        if self.htimer <= 0:
            self.htimer = random.randint(1, 2)
            hammer = Hammer(self.x, self.y, self.dir * HAMMER_SPEED_PPS * game_framework.frame_time)
            game_world.add_object(hammer, 1)
            print('bowser threw hammer')
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def jump(self):
        if self.y >= 40:
            if self.jumping == 1:
                self.yacc = self.gravity
                while self.yacc > 0:
                    self.y += self.yacc
                    self.yacc -= 1
                    self.jumping = 0

    def find_player(self):
        # fill here
        distance2 = (server.mario.x - self.x) ** 2 + (server.mario.y - self.y) ** 2
        if distance2 <= (PIXEL_PER_METER * 10) ** 2:
            print('Bowser found player')
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def build_behavior_tree(self):
        find_player_node = LeafNode('FindPlayer', self.find_player)
        throw_hammer_node = LeafNode('ThrowHammer', self.throw_hammer)

        bowser_behavior = SequenceNode('BowserBehavior')
        bowser_behavior.add_children(find_player_node, throw_hammer_node)

        self.bt = BehaviorTree(bowser_behavior)