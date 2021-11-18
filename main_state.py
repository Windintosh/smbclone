import random
import json
import os

from pico2d import *
import game_framework
import game_world

from mario import Mario
from world import World
from goomba import Goomba
from koopa import Koopa
from hbro import Hbro
from bowser import Bowser
from fireball import Fireball
from hammer import Hammer

name = "MainState"

mario = None
world = None
goomba = None
koopa = None
hbro = None
bowser = None
fb = None

def collide(a, b):
    # fill here
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def enter():
    global mario
    mario = Mario()
    world = World()
    goomba = Goomba()
    koopa = Koopa()
    hbro = Hbro()
    bowser = Bowser()
    fb = Fireball()

    game_world.add_object(world, 0)
    game_world.add_object(mario, 1)
    game_world.add_object(goomba, 1)
    game_world.add_object(koopa, 1)
    game_world.add_object(bowser, 1)
    game_world.add_object(hbro, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    # delay(0.01)
    #collision check
    # if collide(fb, goomba):
    #     print("Goomba Hit")
    #     Goomba.remove(goomba)
    #     game_world.remove_object(Goomba)
    # elif collide(fb, koopa):
    #     print("Koopa Hit")
    #     Goomba.remove(koopa)
    #     game_world.remove_object(koopa)
    # elif collide(fb, bowser):
    #     print("Bowser Hit")
    #     Goomba.remove(bowser)
    #     game_world.remove_object(bowser)
    # elif collide(fb, hbro):
    #     print("Hammer Bro Hit")
    #     Goomba.remove(hbro)
    #     game_world.remove_object(hbro)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






