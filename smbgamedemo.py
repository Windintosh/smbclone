from pico2d import *
import game_framework
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
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/mario_sprite.png')
        self.frame = 0
        self.dir = 0
        self.prevdir = 0
        self.jumping = 0
        self.falling = 0
        self.gravity = 12
        self.yacc = 0
        self.state = 1
        self.running = 0

    def draw(self):
        if self.dir == 1:
            if self.jumping or self.falling == 1:
                self.image.clip_draw(64, 0, 16, 16, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

        elif self.dir == -1:
            if self.jumping or self.falling == 1:
                self.image.clip_composite_draw(64, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)
            else:
                self.image.clip_composite_draw(self.frame * 16, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

        else:
            if self.prevdir == 1 or self.prevdir == 0:
                self.image.clip_draw(96, 0, 16, 16, self.x, self.y)
            elif self.prevdir == -1:
                self.image.clip_composite_draw(96, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

    def update(self):
        if self.x > 240:
            self.x = 240

        if self.dir == 1:
            if self.x > 240:
                self.x = 240
            else:
                # if self.ax < self.x + 500:
                #     self.ax += 250
                #     if self.ax > 500:
                #         self.ax = 500
                #         self.x = (1 - 0.01) * self.x + 0.01 * self.ax
                #     else:
                #         self.x = (1 - 0.01) * self.x + 0.01 * self.ax
                if self.running == 1:
                    self.x += 15
                else:
                    self.x += 5

        elif self.dir == -1:
            if self.x < 0:
                self.x = 0
            else:
                # if self.ax > self.x - 500:
                #     self.ax -= 250
                #     if self.ax < -500:
                #         self.ax = -500
                #         self.x = (1 - 0.01) * self.x + 0.01 * self.ax
                #     else:
                #         self.x = (1 - 0.01) * self.x + 0.01 * self.ax
                if self.running == 1:
                    self.x -= 15
                else:
                    self.x -= 5
        # else:
        #     self.x = (1 - 0.01) * self.x + 0.01 * self.ax

        if self.y > 40 and self.jumping == 0:
            self.falling = 1
            self.yacc = self.gravity
            self.y -= self.yacc
            self.yacc += 1
        else:
            self.y = 40
            self.yacc = self.gravity
            self.falling = 0

        self.frame = (self.frame + 1) % 3
        delay(0.05)

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


class Goomba:
    def __init__(self):
        self.x, self.y = 240, 40
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/goomba_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(self.frame * 16, 0, 16, 16, 0, 'h', self.x, self.y, 16, 16)

        elif self.dir == -1:
            self.image.clip_draw(self.frame * 16, 0, 16, 16, self.x, self.y)

    def update(self):
        self.x -= 5

        self.frame = (self.frame + 1) % 2

class Koopa:
    def __init__(self):
        self.x, self.y = 300, 42
        self.ax, self.ay = self.x, self.y
        self.image = load_image('assets/koopa_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.state = 0

    def draw(self):
        if self.dir == 1:
            self.image.clip_composite_draw(self.frame * 16, 0, 16, 24, 0, 'h', self.x, self.y, 16, 16)

        elif self.dir == -1:
            self.image.clip_draw(self.frame * 16, 0, 16, 24, self.x, self.y)

    def update(self):
        self.x -= 5

        self.frame = (self.frame + 1) % 2

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

    if mario.x > 230:
        if world.x < -1320:
            world.x = -1320
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


open_canvas(320, 240)
world = World()
mario = Mario()
goomba = Goomba()
koopa = Koopa()

running = True;

# game main loop code
while running:
    handle_events()

    #game logic
    mario.update()
    goomba.update()
    koopa.update()
    if mario.jumping == 1:
        mario.jump()

    #game drawing
    clear_canvas()
    world.draw()
    mario.draw()
    goomba.draw()
    koopa.draw()
    scroll()
    update_canvas()

# finalization code

close_canvas()