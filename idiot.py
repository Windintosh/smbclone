import game_framework
from pico2d import *
import title_state
import server

name = "Idiot"
image = None
logo_time = 0.0
change_time = 0.3
wb = 0


def enter():
    global image
    global sound_effect
    image = load_image('assets/idiota.png')
    server.mario.idiot_sound.play()
    pass


def exit():
    global image
    del image
    pass


def update():
    global logo_time
    global change_time
    global wb

    if logo_time > 7.5 :
        logo_time = 0
        # game_framework.quit()
        game_framework.change_state(title_state)
    # delay(0.01)
    logo_time += 0.01
    change_time -= 0.01
    pass


def draw():
    global image
    global change_time
    global wb
    clear_canvas()
    # image.draw(310, 190, )
    if change_time <= 0:
        change_time = 0.3
        if wb == 0:
            wb = 1
        else:
            wb = 0
    if wb == 1:
        image.clip_draw(0, 0, 501, 310, 290, 220)
    else:
        image.clip_draw(505,0, 501, 310, 290, 220)

    update_canvas()
    pass




def handle_events():
    def handle_events():
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                game_framework.quit()
            else:
                if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                    game_framework.quit()
                elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                    game_framework.change_state(title_state)
                    pass

        pass


def pause(): pass


def resume(): pass

