import sys
import random
import pygame
from box import *

#blits all items from to_blit onto surface.
def blit_all(surface, to_blit):
    for item in to_blit:
        surface.blit(item[0], item[1])

#creates and returns surface, rect for a given text and font.
def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

#given a list of buttons and a position, returns the clicked button.
#only works on Button objects.
def get_clicked(clickable, pos):
    for option in clickable:
        if option.rect.collidepoint(pos[0], pos[1]):
            return option
    return None

#class representing buttons.
class Button:
    #ic is the button's inactive color, ac is its color when hovered over.
    def __init__(self, text, x, y, w, h, ic, ac):
        self.inactive_color = ic
        self.active_color = ac
        self.current_color = ic
        self.text = text
        self.x, self.y, self.w, self.h = x, y, w, h
        self.rect = pygame.Rect(x, y, w, h)

    #function to draw the button to a given surface.
    def draw(self, surface):
        font_use = pygame.font.SysFont("arial black", 16)
        textSurf, textRect = text_objects(self.text, font_use)
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        #current mouse location
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse[0], mouse[1]):  #if user is hovering
            color = self.active_color
        else:
            color = self.inactive_color
        #display rectangle and text
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(textSurf, textRect)

    #button's behavior when clicked.
    #returns change in energy, character it applies to.
    def action(self):
        if self.text == "Attack":
            chance_attack = random.randint(1, 10)
            if chance_attack < 8:
                print("Your attack hit!")
                return -10, "enemy"  #change in enemy energy
            else:
                print("Your attack missed!")
                return 0, "enemy"    #change in enemy energy
        elif self.text == "Refresh":
            return 5, "player"
        elif self.text == "Range Attack":
            chance_attack = random.randint(1, 10)
            if chance_attack < 5:
                return -15, "enemy"
            else:
                return 0, "enemy"

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
    pg.init()
    pg.font.init()
    dimensions = (game_width, game_height)
    screen = pg.display.set_mode(dimensions)
    bg_color = (100, 0, 100)

    #colors
    black = (0, 0, 0)
    white = (255,255,255)
    lighter_blue = (152, 245, 255)

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

    #action buttons
    btn_padding = 25
    btn_width = 130
    attack_button = Button("Attack", btn_padding, 200, btn_width, 50, white, lighter_blue)
    clickable.append(attack_button)
    refresh_button = Button("Refresh", 2*btn_padding+btn_width, 200, btn_width, 50, white, lighter_blue)
    clickable.append(refresh_button)
    range_attack_button = Button("Range Attack", 3*btn_padding+2*btn_width, 200, btn_width, 50, white, lighter_blue)
    clickable.append(range_attack_button)

    while playing:
        screen.fill(bg_color)

        attack_button.draw(screen)
        refresh_button.draw(screen)
        range_attack_button.draw(screen)

        #handle events
        for event in pg.event.get():
            #quitting
            if event.type == pg.QUIT:
                playing = False
            #mouse input
            elif event.type == pg.MOUSEBUTTONDOWN:
                clicked = get_clicked(clickable, event.pos)
                print(clicked.text)
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
                        print(enemy_energy)


        # player energy display
        pygame.draw.rect(screen, (75, 0, 130), (100, 80, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (100, 80, player_energy, 10))

        # enemy energy display
        pygame.draw.rect(screen, (75, 0, 130), (400, 80, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (400, 80, enemy_energy, 10))

        #menu box display
        menu = Box(10, game_height-110, game_width-20, 100, (255, 255, 255), 10, (100, 200, 100))
        visible.append(menu.get_box())

        #blit all objects and update the screen.
        blit_all(screen, visible)
        pg.display.flip()

    #game loop has ended. exit the game.
    pg.quit()
    sys.exit()


run()
