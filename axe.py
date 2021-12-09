from pico2d import *
import collision
import game_framework
import server
import idiot
import gameclear
import main_state
import title_state
import world

class Axe: #
    image = None
    def __init__(self, l, h):
        self.left = l
        self.up = h
        self.x, self.y = self.left * 16, self.up * 16
        self.ax, self.ay = self.x, self.y
        if Axe.image == None:
            Axe.image = load_image('assets/axe_sprite.png')
        self.frame = 0
        self.dir = -1
        self.falling = 0
        self.gravity = 11
        self.yacc = 0
        self.speed = 0
        self.state = 1
        self.clear_music = load_wav('assets/smb_world_clear.wav')

    def get_bb(self):
        # fill here
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.draw(self.x, self.y, 16, 16)

    def update(self):
        if collision.collide(self, server.mario):
            if server.bowser.hp != 0:
                game_framework.change_state(idiot)
            else:
                if main_state.level == 2:
                    game_framework.change_state(gameclear)
                    main_state.level = 1
                    self.clear_music.play()
                    server.world.bgm.set_volume(0)
                else :
                    game_framework.change_state(title_state)
                    main_state.level += 1
                pass


    def scroll(self):
        if server.mario.x >= 350 and server.mario.speed >0:
            if server.mario.dash ==1:
                self.x -= server.mario.speed * game_framework.frame_time * 2
            else:
                self.x -= server.mario.speed * game_framework.frame_time
            pass
        pass