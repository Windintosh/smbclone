from pico2d import *
import game_framework
import game_world
import title_state
import world
import goomba
import koopa
from hammer import Hammer
from fireball import Fireball
import random

history = []

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, DASH_DOWN, DASH_UP, DEBUG_KEY, JUMP_DOWN, JUMP_UP = range(9)
event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'DASH_DOWN', 'DASH_UP', 'DEBUG_KEY', 'JUMP_DOWN', 'JUMP_UP' ]

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): DEBUG_KEY,
    # (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    # (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    # (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    # (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_z): DASH_DOWN,
    (SDL_KEYUP, SDLK_z): DASH_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): JUMP_DOWN,
    (SDL_KEYUP, SDLK_x): JUMP_UP
}

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 20.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

FB_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
FB_SPEED_KMH = 60 # kmh
FB_SPEED_MPM = (FB_SPEED_KMH * 1000.0 / 60.0) #meter per minute
FB_SPEED_MPS = (FB_SPEED_MPM / 60.0) #METER PER SECOND
FB_SPEED_PPS = (FB_SPEED_MPS * FB_PIXEL_PER_METER) #pixel per second

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.speed += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.speed -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.speed -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.speed += RUN_SPEED_PPS

    def exit(mario, event):
        if event == DASH_DOWN:
            mario.fire_fb()
        elif event == JUMP_DOWN:
            mario.fire_hammer()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(0, 33, 16, 24, mario.x, mario.y)
        else:
            mario.image.clip_composite_draw(0, 33, 16, 24, 0, 'h', mario.x, mario.y, 16, 24)


class RunState:

    def enter(mario, event):
        # fill here
        if event == RIGHT_DOWN:
            mario.speed += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.speed -= RUN_SPEED_PPS
        elif event == RIGHT_UP :
            mario.speed -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.speed += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.speed, 1)
        pass

    def exit(mario, event):
        if event == DASH_DOWN:
            mario.fire_fb()
        elif event == JUMP_DOWN:
            mario.fire_hammer()
        pass

    def do(mario):
        # fill here
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        mario.x += mario.speed * game_framework.frame_time
        mario.x = clamp(25, mario.x, 576-25) # 350

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 16, 32, 16, 24, mario.x, mario.y)
        else:
            mario.image.clip_composite_draw(int(mario.frame) * 16, 32, 16, 24, 0, 'h', mario.x, mario.y, 16, 24)

class DashState:

    def enter(mario, event):
        print('ENTER DASH')
        mario.dir = clamp(-1, mario.speed, 1)


    def exit(mario, event):
        print('EXIT DASH')
        if event == DASH_DOWN:
            mario.fire_fb()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        mario.x += mario.speed * game_framework.frame_time * 2
        mario.x = clamp(25, mario.x, 576 - 25) #350

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 16, 32, 16, 24, mario.x, mario.y)
        else:
            mario.image.clip_composite_draw(int(mario.frame) * 16, 32, 16, 24, 0, 'h', mario.x, mario.y, 16, 24)

class JumpState: # needed

    def enter(mario, event):
        print('ENTER JUMP')
        mario.dir = clamp(-1, mario.speed, 1)


    def exit(mario, event):
        print('EXIT JUMP')
        if event == JUMP_DOWN:
            mario.fire_hammer()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.x += mario.speed * game_framework.frame_time * 2
        mario.x = clamp(25, mario.x, 576 - 25) #350

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(48, 32, 16, 24, mario.x, mario.y)
        else:
            mario.image.clip_composite_draw(48, 32, 16, 24, 0, 'h', mario.x, mario.y, 16, 24)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, DASH_DOWN: IdleState, DASH_UP: IdleState, JUMP_DOWN: IdleState, JUMP_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, DASH_DOWN: DashState, DASH_UP: RunState, JUMP_DOWN: JumpState, JUMP_UP: RunState},
    DashState: {DASH_UP: RunState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState, DASH_DOWN: DashState, JUMP_DOWN: DashState, JUMP_UP: DashState},
    JumpState: {DASH_UP: RunState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_UP: IdleState, RIGHT_DOWN: IdleState, DASH_DOWN: DashState, JUMP_DOWN: JumpState, JUMP_UP: JumpState}
        # {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, DASH_DOWN: IdleState, DASH_UP: IdleState, JUMP_DOWN: JumpState, JUMP_UP: IdleState}
}


# change state, collision check, items

class Mario:
    def __init__(self):
        self.x, self.y = 100, 43
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/mario_new_sprite.png')
        self.frame = 0
        self.dir = 1
        self.prevdir = 0
        self.speed = 0
        self.jumping = 0
        self.falling = 0
        self.gravity = 12
        self.yacc = 0
        self.state = 1
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def jump(self):
        if self.y >= 40:
            if self.jumping == 1:
                self.yacc = self.gravity
                while self.yacc > 0:
                    self.y += self.yacc
                    self.yacc -= 1
                    self.jumping = 0

        else:
            self.y = 40
            self.jumping = 0

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 12, self.x + 8, self.y + 12

    def fire_fb(self):
        fb = Fireball(self.x, self.y, self.dir * FB_SPEED_PPS * game_framework.frame_time)
        game_world.add_object(fb, 1)

    def fire_hammer(self):
        hammer = Hammer(self.x, self.y, self.dir * FB_SPEED_PPS * game_framework.frame_time)
        game_world.add_object(hammer, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        # fill here
        # self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

if __name__ == '__main__':
    main()
