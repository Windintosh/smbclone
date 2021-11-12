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

name = "MainState"

mario = None

def enter():
    global mario
    mario = Mario()
    world = World()
    goomba = Goomba()
    koopa = Koopa()
    game_world.add_object(world, 0)
    game_world.add_object(mario, 1)
    game_world.add_object(goomba, 1)
    game_world.add_object(koopa, 1)


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

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






