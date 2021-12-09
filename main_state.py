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
from axe import Axe
from hammer import Hammer

name = "MainState"

level = 1

def enter():
    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    server.world = World()
    game_world.add_object(server.world, 0)

    server.goomba = Goomba(20, random.randint(6, 10))
    game_world.add_object(server.goomba, 1)

    server.koopa = Koopa(80, random.randint(6, 10))
    game_world.add_object(server.koopa, 1)

    server.hbro = Hbro(100, random.randint(6, 10))
    game_world.add_object(server.hbro, 1)

    server.bowser = Bowser(random.randint(120, 150), random.randint(8, 10))
    game_world.add_object(server.bowser, 1)

    if level == 2:
        server.goomba2 = Goomba(random.randint(50, 60), random.randint(6, 10))
        game_world.add_object(server.goomba2, 1)

        server.koopa2 = Koopa(random.randint(150, 170), random.randint(6, 10))
        game_world.add_object(server.koopa2, 1)

        server.hbro2 = Hbro(random.randint(150, 180), random.randint(6, 10))
        game_world.add_object(server.hbro2, 1)

    # elif level == 3:
    #     server.goomba2 = Goomba(random.randint(50, 160), random.randint(6, 10))
    #     game_world.add_object(server.goomba2, 1)
    #
    #     server.koopa2 = Koopa(random.randint(50, 170), random.randint(6, 10))
    #     game_world.add_object(server.koopa2, 1)
    #
    #     server.hbro2 = Hbro(random.randint(50, 180), random.randint(6, 10))
    #     game_world.add_object(server.hbro2, 1)
    #
    #     server.goomba3 = Goomba(random.randint(50, 160), random.randint(6, 10))
    #     game_world.add_object(server.goomba3, 1)
    #
    #     server.koopa3 = Koopa(random.randint(50, 170), random.randint(6, 10))
    #     game_world.add_object(server.koopa3, 1)
    #
    #     server.hbro3 = Hbro(random.randint(50, 180), random.randint(6, 10))
    #     game_world.add_object(server.hbro3, 1)
    #
    # elif level == 4:
    #     server.goomba2 = Goomba(random.randint(50, 160), random.randint(6, 10))
    #     game_world.add_object(server.goomba2, 1)
    #
    #     server.koopa2 = Koopa(random.randint(50, 170), random.randint(6, 10))
    #     game_world.add_object(server.koopa2, 1)
    #
    #     server.hbro2 = Hbro(random.randint(50, 180), random.randint(6, 10))
    #     game_world.add_object(server.hbro2, 1)
    #
    #     server.goomba3 = Goomba(random.randint(50, 160), random.randint(6, 10))
    #     game_world.add_object(server.goomba3, 1)
    #
    #     server.koopa3 = Koopa(random.randint(50, 170), random.randint(6, 10))
    #     game_world.add_object(server.koopa3, 1)
    #
    #     server.hbro3 = Hbro(random.randint(50, 180), random.randint(6, 10))
    #     game_world.add_object(server.hbro3, 1)
    #
    #     server.goomba4 = Goomba(random.randint(50, 160), random.randint(6, 10))
    #     game_world.add_object(server.goomba4, 1)
    #
    #     server.koopa4 = Koopa(random.randint(50, 170), random.randint(6, 10))
    #     game_world.add_object(server.koopa4, 1)
    #
    #     server.hbro4 = Hbro(random.randint(50, 180), random.randint(6, 10))
    #     game_world.add_object(server.hbro4, 1)

    for i in range(69): # total length of level = 211 blocks, platform 1
        server.block = Block(i, 1)
        game_world.add_object(server.block, 1)

        server.block = Block(68, 2)
        game_world.add_object(server.block, 1)

    server.itemblock = Itemblock(17, 5)
    game_world.add_object(server.itemblock, 1)

    for i in range(21, 27, 2): #~25
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    for i in range(22, 26, 2): # ~24
        server.itemblock = Itemblock(i, 5)
        game_world.add_object(server.itemblock, 1)

    server.itemblock = Itemblock(23, 9)
    game_world.add_object(server.itemblock, 1)

    for i in range(29, 31):
        for k in range(2, 4):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)

    for i in range(40, 42):
        for k in range(2, 5):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)

    for i in range(48, 50): #make pipe
        for k in range(2, 6):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)

    for i in range(60, 62):
        for k in range(2, 6):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)

    for i in range(72, 88): #platform 2
        server.block = Block(i, 1)
        game_world.add_object(server.block, 1)

    server.block = Block(72, 2)
    game_world.add_object(server.block, 1)

    server.block = Block(87, 2)
    game_world.add_object(server.block, 1)

    for i in range(78, 81, 2):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    server.itemblock = Itemblock(79, 5)
    game_world.add_object(server.itemblock, 1)

    for i in range(81, 90):
        server.block = Block(i, 9)
        game_world.add_object(server.block, 1)

    for i in range(91, 155): #platform 3
        server.block = Block(i, 1)
        game_world.add_object(server.block, 1)

    server.block = Block(91, 2)
    game_world.add_object(server.block, 1)

    for i in range(93, 96):
        server.block = Block(i, 9)
        game_world.add_object(server.block, 1)

    server.itemblock = Itemblock(96, 9)
    game_world.add_object(server.itemblock, 1)

    server.block = Block(96, 5)
    game_world.add_object(server.block, 1)

    for i in range(102, 104):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    for i in range(108, 115, 3): #-114
        server.itemblock = Itemblock(i, 5)
        game_world.add_object(server.itemblock, 1)

    server.itemblock = Itemblock(111, 9)
    game_world.add_object(server.itemblock, 1)

    server.block = Block(120, 5)
    game_world.add_object(server.block, 1)

    for i in range(123, 126):
        server.block = Block(i, 9)
        game_world.add_object(server.block, 1)

    for i in range(130, 134, 3): #-133
        server.block = Block(i, 9)
        game_world.add_object(server.block, 1)

    for i in range(131, 133):
        server.itemblock = Itemblock(i, 9)
        game_world.add_object(server.itemblock, 1)

    for i in range(131, 133):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)
    #double steps
    for i in range(136, 140):
        server.block = Block(i, 2)
        game_world.add_object(server.block, 1)

    for i in range(142, 146):
        server.block = Block(i, 2)
        game_world.add_object(server.block, 1)

    for i in range(137, 140):
        server.block = Block(i, 3)
        game_world.add_object(server.block, 1)

    for i in range(142, 145):
        server.block = Block(i, 3)
        game_world.add_object(server.block, 1)

    for i in range(138, 140):
        server.block = Block(i, 4)
        game_world.add_object(server.block, 1)

    for i in range(142, 144):
        server.block = Block(i, 4)
        game_world.add_object(server.block, 1)

    for i in range(139, 143, 3):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)
    #end of double steps

    for i in range(150, 155):
        server.block = Block(i, 2)
        game_world.add_object(server.block, 1)

    for i in range(151, 155):
        server.block = Block(i, 3)
        game_world.add_object(server.block, 1)

    for i in range(152, 155):
        server.block = Block(i, 4)
        game_world.add_object(server.block, 1)

    for i in range(153, 155):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    for i in range(157, 211):  # platform 4 ~ end of the level
        server.block = Block(i, 1)
        game_world.add_object(server.block, 1)

    for i in range(157, 161):
        server.block = Block(i, 2)
        game_world.add_object(server.block, 1)

    for i in range(157, 160):
        server.block = Block(i, 3)
        game_world.add_object(server.block, 1)

    for i in range(157, 159):
        server.block = Block(i, 4)
        game_world.add_object(server.block, 1)

    server.block = Block(157, 5)
    game_world.add_object(server.block, 1)

    for i in range(165, 167): #make pipe ~166
        for k in range(2, 4):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)

    for i in range(170, 172):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    server.itemblock = Itemblock(172, 5)
    game_world.add_object(server.itemblock, 1)

    server.block = Block(173, 5)
    game_world.add_object(server.block, 1)

    for i in range(181, 183): #make pipe ~182
        for k in range(2, 4):
            server.block = Block(i, k)
            game_world.add_object(server.block, 1)
    #make stairs
    for i in range(183, 193):
        server.block = Block(i, 2)
        game_world.add_object(server.block, 1)

    for i in range(184, 193):
        server.block = Block(i, 3)
        game_world.add_object(server.block, 1)

    for i in range(185, 193):
        server.block = Block(i, 4)
        game_world.add_object(server.block, 1)

    for i in range(186, 193):
        server.block = Block(i, 5)
        game_world.add_object(server.block, 1)

    for i in range(187, 193):
        server.block = Block(i, 6)
        game_world.add_object(server.block, 1)

    for i in range(188, 193):
        server.block = Block(i, 7)
        game_world.add_object(server.block, 1)

    for i in range(189, 193):
        server.block = Block(i, 8)
        game_world.add_object(server.block, 1)

    for i in range(190, 193):
        server.block = Block(i, 9)
        game_world.add_object(server.block, 1)

    server.axe = Axe(201, 2)
    game_world.add_object(server.axe, 1)

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
        if server.mario.bump == 0:
            game_object.scroll()
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






