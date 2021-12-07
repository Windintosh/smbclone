import random
import json
import os

from pico2d import *
import game_framework
import game_world
import server

from mario import Mario
from world import World
from goomba import Goomba
from koopa import Koopa
from hbro import Hbro
from bowser import Bowser
from fireball import Fireball
from block import Block
from itemblock import Itemblock
from hammer import Hammer

name = "MainState"


def enter():
    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    server.world = World()
    game_world.add_object(server.world, 0)

    server.goomba = Goomba(random.randint(1, 30), random.randint(5, 20))
    game_world.add_object(server.goomba, 1)

    server.koopa = Koopa(random.randint(1, 30), random.randint(5, 20))
    game_world.add_object(server.koopa, 1)

    server.hbro = Hbro(random.randint(1, 30), random.randint(5, 20))
    game_world.add_object(server.hbro, 1)

    server.bowser = Bowser(random.randint(10, 30), random.randint(5, 20))
    game_world.add_object(server.bowser, 1)

    server.block = Block(random.randint(1, 30), random.randint(5, 20))
    game_world.add_object(server.block, 1)

    server.itemblock = Itemblock(random.randint(1, 30), random.randint(1, 20))
    game_world.add_object(server.itemblock, 1)


    server.fb = Fireball()

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
            server.mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    # fill here
    # delay(0.01)
    #collision  ->move to individuals
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






