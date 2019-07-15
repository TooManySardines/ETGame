import pygame
import math
import random



def get_relative_pos(pos, parent_pos):
    return (pos[0]-parent_pos[0], pos[1]-parent_pos[0])

#class representing buttons.
class Button:
    #ic is the button's inactive color, ac is its color when hovered over.
    def __init__(self, text, x, y, w, h, ic, ac, parent_pos):
        self.inactive_color = ic
        self.active_color = ac
        self.current_color = ic
        self.text = text
        self.x, self.y, self.w, self.h = x, y, w, h
        self.parent_pos = parent_pos
        self.rect = pygame.Rect(x, y, w, h)

    #function to draw the button to a given surface.
    def draw(self, surface):
        font_use = pygame.font.SysFont("arial black", 16)
        textSurf, textRect = text_object(self.text, font_use)
        textRect.center = ((self.x + (self.w / 2)), (self.y + (self.h / 2)))
        #current mouse location
        mouse = pygame.mouse.get_pos()

        color = self.active_color if self.rect_absolute_pos().collidepoint(mouse[0], mouse[1]) else self.inactive_color

        #display rectangle and text
        if self.text == "Attack":
            print(color)
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

    def rect_absolute_pos(self):
        return pygame.Rect(self.parent_pos[0]+self.x, self.parent_pos[1]+self.y, self.w, self.h)

#creates and returns surface, rect for a given text and font.
def text_object(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

#class for drawing boxes. here to make drawing boxes take fewer lines of code, and also as a superclass for fancier boxes.
class Box:
    #make a surface and rect for the box.
    def __init__(self, x, y, width, height, color, border_width = -1, border_color = (0, 0, 0)):
        self.color = color
        self.border_width = border_width
        self.border_color = border_color
        self.width = width
        self.height = height
        self.surface = self.get_new_surface()
        self.pos = (x, y)
        self.rect = self.surface.get_rect(topleft = self.pos)

    #return the box in the form of a tuple: (surface, rect)
    def get_box(self):
        return (self.surface, self.rect)

    def get_new_surface(self):
        surface =pygame.Surface((self.width, self.height))
        surface.fill(self.color)
        pygame.draw.rect(surface, self.border_color,pygame.Rect(0, 0, self.width, self.height), self.border_width)
        return surface

# #class to manage buttons within a UIbox.
# class UIbutton:
#     def __init__(self, text, font):
#         self.font = font
#         width = self.font.size(text)[0]
#         height = self.font.size(text)[1]
#         self.color = (0, 0, 0)
#         self.text = text
#         self.pos = (0, 0)
#         self.surface = self.font.render(text, False, self.color)
#
#     def update_surface(self):
#         self.surface = self.font.render(self.text, False, self.color)

#class to display clickable options.
class UIbox(Box):
    def __init__(self, options, ic, ac, x, y, width, height, color, border_width = 10, border_color = (100, 200, 100)):
        #make the box
        Box.__init__(self, x, y, width, height, color, border_width, border_color)
        pygame.font.init()
        self.font = pygame.font.SysFont("Sans-Serif", 30)
        self.buttons = self.generate_buttons(options, ic, ac, self.pos)
        self.draw()

    def generate_buttons(self, options, ic, ac, parent_pos):
        result = []
        width, height = 100, 50
        margin = 25
        x, y = 25, 25
        for op in options:
            result.append(Button(op, x, y, width, height, ic, ac, parent_pos))
            x += width + margin
        return result


    #given a list of buttons and a position, returns the clicked button.
    #only works on Button objects.
    def get_clicked(self, pos):
        for op in self.buttons:
            if op.rect.collidepoint(get_relative_pos(pos, self.pos[0], self.pos[1])):
                return op
        else:
            return None

    def get_longest(self):
        longest = self.options[0]
        for op in self.options:
            if self.font.size(op.text)[0] > self.font.size(longest.text)[0]:
                longest = op
        return longest

    def draw(self):
        self.surface = self.get_new_surface()
        for button in self.buttons:
            button.draw(self.surface)
        #blit options to UIbox's surface
        # current_x = 20
        # current_y = 20
        # length = self.font.size(self.get_longest().text)[0] + 20
        # height = self.font.size(self.options[0].text)[1] + 15
        # for op in self.options:
        #     if current_x + length + 20 > self.rect.width:
        #         current_y += height
        #         current_x = 20
        #         self.surface.blit(op.surface, (current_x, current_y))
        #         op.pos = (current_x, current_y)
        #         current_x += length
        #     else:
        #         self.surface.blit(op.surface, (current_x, current_y))
        #         op.pos = (current_x, current_y)
        #         current_x += length
