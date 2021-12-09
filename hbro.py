from pico2d import *
import game_framework
from hammer import Hammer
import game_world
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import server
import collision

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 10.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

HAMMER_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
HAMMER_SPEED_KMH = 20 # kmh
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

# action with timer, jump, sprite needed
class Hbro:
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/hbro_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.jumping = 0
        # self.falling = 0
        # self.gravity = 12
        # self.yacc = 0
        self.yacc = 0
        self.state = 1
        self.speed = 0
        self.htimer = 1
        self.build_behavior_tree()
        self.fire_sound = load_wav('assets/smb_bowserfire.wav')

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 12, self.x + 8, self.y + 12

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 16, 0, 16, 24, 0, 'h', self.x, self.y, 16, 16)

        elif self.dir == -1:
            self.image.clip_draw(int(self.frame) * 16, 0, 16, 24, self.x, self.y)

    def update(self):
        if self.state == 1:
            self.bt.run()
            if self.dir == -1:
                # self.x -= RUN_SPEED_PPS * game_framework.frame_time
                pass
            else:
                # self.x += RUN_SPEED_PPS * game_framework.frame_time
                pass
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.y -= FALL_SPEED_PPS * game_framework.frame_time
            if self.y <= 0:
                self.state = 0
            if collision.collide(self, server.block):
                if self.y - 12 >= server.block.y:
                    self.y = server.block.y + 19
                    self.falling = 0
                    pass
                elif server.block.y >= self.y + 12:
                    self.y = server.block.y - 24
                    self.jumping = 0
                    self.falling = 1
                    pass
                elif self.x >= server.block.x:
                    self.x = server.block.x + 16
                    pass
                elif server.block.x >= self.x:
                    self.x = server.block.x - 16
                    pass
        elif self.state == 0:
            game_world.remove_object(self)
            self.x, self.y = -1, -1

    def throw_hammer(self): #sound
        self.htimer -= game_framework.frame_time
        if self.htimer <= 0:
            self.htimer = random.randint(1, 2)
            hammer = Hammer(self.x, self.y, self.dir * HAMMER_SPEED_PPS * game_framework.frame_time)
            game_world.add_object(hammer, 1)
            print('hbro threw hammer')
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
        if distance2 <= (PIXEL_PER_METER * 3) ** 2:
            print('Hbro found player')
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def build_behavior_tree(self):
        find_player_node = LeafNode('FindPlayer', self.find_player)
        throw_hammer_node = LeafNode('ThrowHammer', self.throw_hammer)

        hbro_behavior = SequenceNode('HBroBehavior')
        hbro_behavior.add_children(find_player_node, throw_hammer_node)

        self.bt = BehaviorTree(hbro_behavior)

    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass