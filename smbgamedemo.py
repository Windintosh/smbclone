from pico2d import *
import random


class World:
    def __init__(self):
        self.image = load_image('assets/world1-1_over.png')
        self.x, self.y = 1688, 120

    def draw(self):
        self.image.draw(self.x, self.y)


class Mario:
    def __init__(self):
        self.x, self.y = 100, 40
        self.image = load_image('assets/mario_sprite.png')
        self.frame = 0
        self.dir = 0
        self.prevdir = 0

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

        elif self.dir == -1:
            self.image.clip_composite_draw(self.frame * 16, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

        else:
            if self.prevdir == 1 or self.prevdir == 0:
                self.image.clip_draw(96, 0, 16, 16, self.x, self.y)
            elif self.prevdir == -1:
                self.image.clip_composite_draw(96, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

    def update(self):
        if self.dir == 1:
            if self.x > 240:
                self.x = 240
            else:
                self.x += 5

        elif self.dir == -1:
            if self.x < 0:
                self.x = 0
            else:
                self.x -= 5


        self.frame = (self.frame + 1) % 3
        delay(0.05)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                mario.dir += 1
            elif event.key == SDLK_LEFT:
                mario.dir -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                mario.dir -= 1
                mario.prevdir = 1
            elif event.key == SDLK_LEFT:
                mario.dir += 1
                mario.prevdir = -1
    pass


def scroll():

    if mario.x > 230 and mario.dir == 1:
        if world.x < -1320:
            world.x = -1320
            pass
        else:
            world.x -= 5


open_canvas(320, 240)
world = World()
mario = Mario()

running = True;

# game main loop code
while running:
    handle_events()

    #game logic
    mario.update()


    #game drawing
    clear_canvas()
    world.draw()
    mario.draw()
    scroll()
    update_canvas()

# finalization code

close_canvas()