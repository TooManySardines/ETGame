import sys
import random
import pygame
from box import *

#blits all items from to_blit onto surface.
def blit_all(surface, to_blit):
    for item in to_blit:
        surface.blit(item[0], item[1])

#run the game.
def run():
    #basic game variables
    playing = True
    game_width = 500
    game_height = 400
    visible = []
    clickable = []
    player_energy = 50
    enemy_energy = 50

    #set up pygame stuff
    pygame.init()
    pygame.font.init()
    dimensions = (game_width, game_height)
    screen = pygame.display.set_mode(dimensions)
    bg_color = (100, 0, 100)

    #colors
    black = (0, 0, 0)
    white = (255,255,255)
    lighter_blue = (152, 245, 255)

    #play music
    pygame.mixer.music.load('temp.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    #player surface and variables
    player = Box(100, 100, 50, 50, (0, 255, 0))
    visible.append(player.get_box())

    #enemy surface and variables
    enemy = Box(400, 100, 50, 50, (255, 0, 0))
    visible.append(enemy.get_box())

    # #action buttons
    # btn_margin = 15
    # btn_width = 140
    # attack_button = Button("Attack", 25, 200, btn_width, 50, white, lighter_blue)
    # clickable.append(attack_button)
    # refresh_button = Button("Refresh", 25+btn_margin+btn_width, 200, btn_width, 50, white, lighter_blue)
    # clickable.append(refresh_button)
    # range_attack_button = Button("Range Attack", 25+2*btn_margin+2*btn_width, 200, btn_width, 50, white, lighter_blue)
    # clickable.append(range_attack_button)
    ui = UIbox(["Attack", "Refresh", "Range Attack"], (255, 255, 0), (100, 100, 255), 10, game_height-110, game_width-20, 100, (255, 255, 255), 10, (100, 200, 100))
    visible.append(ui.get_box())

    while playing:
        screen.fill(bg_color)

        ui.draw()
        # attack_button.draw(screen)
        # refresh_button.draw(screen)
        # range_attack_button.draw(screen)

        #handle events
        for event in pygame.event.get():
            #quitting
            if event.type == pygame.QUIT:
                playing = False
            #mouse input
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked = get_clicked(clickable, event.pos)
                if clicked != None:
                    d_energy, affected = clicked.action()
                    if affected == "player":
                        if player_energy + d_energy > 50:
                            player_energy = 50
                        else:
                            player_energy += d_energy
                    elif affected == "enemy":
                        if enemy_energy + d_energy < 0:
                            enemy_energy = 0
                        else:
                            enemy_energy += d_energy
                        print(player_energy, enemy_energy)


        # player energy display
        pygame.draw.rect(screen, (75, 0, 130), (100, 80, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (100, 80, player_energy, 10))

        # enemy energy display
        pygame.draw.rect(screen, (75, 0, 130), (400, 80, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (400, 80, enemy_energy, 10))

        # #menu box display
        # menu = Box(10, game_height-110, game_width-20, 100, (255, 255, 255), 10, (100, 200, 100))
        # visible.append(menu.get_box())

        #blit all objects and update the screen.
        blit_all(screen, visible)
        pygame.display.flip()

    #game loop has ended. exit the game.
    pygame.quit()
    sys.exit()


run()
