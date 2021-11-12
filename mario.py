from pico2d import *
import game_framework
import game_world
import title_state
import world
import goomba
import koopa
from hammer import Hammer
import random

history = []

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, SPACE = range(10)
event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SLEEP_TIMER', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER', 'DEBUG_KEY', 'SPACE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_d): DEBUG_KEY,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
RUN_SPEED_KMH = 20.0 # kmh
RUN_SPEED_MPM = (RUN_SPEED_KMH * 1000.0 / 60.0) #meter per minute
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #METER PER SECOND
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #pixel per second

HAMMER_PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 당 30cm
HAMMER_SPEED_KMH = 25.0 # kmh
HAMMER_SPEED_MPM = (HAMMER_SPEED_KMH * 1000.0 / 60.0) #meter per minute
HAMMER_SPEED_MPS = (HAMMER_SPEED_MPM / 60.0) #METER PER SECOND
HAMMER_SPEED_PPS = (HAMMER_SPEED_MPS * HAMMER_PIXEL_PER_METER) #pixel per second

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
        mario.timer = 1000

    def exit(mario, event):
        if event == SPACE:
            mario.fire_hammer()
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.timer -= 1
        # if mario.timer == 0:
        #     mario.add_event(SLEEP_TIMER)

    def draw(mario):
        # if mario.prevdir == 1 or mario.prevdir == 0:
            mario.image.clip_draw(96, 48, 16, 16, mario.x, mario.y)
        # elif mario.prevdir == -1:
            mario.image.clip_composite_draw(96, 48, 16, 16, 0, 'h', mario.x, mario.y, 16, 16)


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
        if event == SPACE:
            mario.fire_hammer()
            pass

    def do(mario):
        # fill here
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.x += mario.speed * game_framework.frame_time
        mario.x = clamp(25, mario.x, 1600 - 25)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(int(mario.frame) * 16, 48, 16, 16, mario.x, mario.y)

        elif mario.dir == -1:
            mario.image.clip_composite_draw(int(mario.frame) * 16, 48, 16, 16, 0, 'h', mario.x, mario.y, 16, 16)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState},
    # SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState}
}




class Mario:
    def __init__(self):
        self.x, self.y = 100, 40
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/mario_sprite.png')
        self.frame = 0
        self.dir = 1
        self.prevdir = 0
        self.speed = 0
        self.jumping = 0
        self.falling = 0
        self.gravity = 12
        self.yacc = 0
        self.state = 1
        self.running = 0
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

    def fire_hammer(self):
        hammer = Hammer(self.x, self.y, self.dir * HAMMER_SPEED_PPS * game_framework.frame_time)
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



"""
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mario.dir += 1
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)
            elif event.key == SDLK_x:
                if mario.falling == 0 and mario.jumping == 0:
                    mario.jumping = 1
                    mario.jump()
                else:
                    pass
            elif event.key == SDLK_z:
                mario.running = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
                mario.prevdir = 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1
                mario.prevdir = -1
            elif event.key == SDLK_x:
                mario.jumping = 0
            elif event.key == SDLK_z:
                mario.running = 0
    pass


def scroll():

    if mario.x > 350:
        if world.x < -1960:
            world.x = -1960
            pass
        else:
            if mario.running == 1:
                world.x -= 15
                goomba.x -= 15
                koopa.x -= 15
                mario.x -= 15
                # mario.ax = mario.x
            else:
                world.x -= 5
                goomba.x -= 5
                koopa.x -= 5
                mario.x -= 5

"""

if __name__ == '__main__':
    main()
