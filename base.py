import sys
import random
import pygame as pg
from box import *

def blit_all(surface, to_blit):
    for item in to_blit:
        surface.blit(item[0], item[1])

def run():
    #basic game variables
    playing = True
    game_width = 500
    game_height = 400
    visible = []

    #set up pygame stuff
    pg.init()
    pg.font.init()
    dimensions = (game_width, game_height)
    screen = pg.display.set_mode(dimensions)
    bg_color = (100, 0, 100)

    #play music
    pg.mixer.music.load('temp.wav')
    pg.mixer.music.set_volume(0.5)
    pg.mixer.music.play(-1)

    #player surface and variables
    player = Box(100, 100, 50, 50, (0, 255, 0))
    visible.append(player.get_box())
    #enemy surface and variables
    enemy = Box(400, 100, 50, 50, (255, 0, 0))
    visible.append(enemy.get_box())
    #menu box
    menu = UIbox(["Testing1", "Testing2", "Testing3", "Testing4", "Testing5", "Testing6", "Testing7", "Testing8"], 10, game_height-110, game_width-20, 100, (255, 255, 255), 10, (100, 200, 100))
    visible.append(menu.get_box())
    selected = None


    while playing:
        screen.fill(bg_color)

        #handle events
        for event in pg.event.get():
            #quitting
            if event.type == pg.QUIT:
                playing = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                selected = menu.get_clicked(event.pos)
                if selected is not None:
                    print(selected)
                    selected.color = (255, 0, 0)
                    menu.draw()
            elif event.type == pg.MOUSEBUTTONUP:
                if selected is not None:
                    selected.color = (0, 0, 0)
                    menu.draw()

        #display all the things
        blit_all(screen, visible)
        #update display
        pg.display.flip()


    #when the game is finished, quit pygame.
    pg.quit()
    sys.exit()

#run the game!
run()
