import pygame as pg
import math

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
        self.rect = self.surface.get_rect(topleft=(x, y))

    #return the box in the form of a tuple: (surface, rect)
    def get_box(self):
        return (self.surface, self.rect)

    def get_new_surface(self):
        surface = pg.Surface((self.width, self.height))
        surface.fill(self.color)
        pg.draw.rect(surface, self.border_color, pg.Rect(0, 0, self.width, self.height), self.border_width)
        return surface

#fancier box class for text.
#fix at some point. can only accomodate up to 2 lines of text.
#also, better to split text by words. why didn't i think of that earlier.
class Textbox(Box):
    def __init__(self, text, x, y, width, height, color, border_width, border_color):
        Box.__init__(self, x, y, width, height, color, border_width, border_color)
        pg.font.init()
        font = pg.font.SysFont("Sans-Serif", 30)
        self.text = text
        if font.size(text)[0] > width-40:
            split_len = -1
            found_split = False
            high = len(text)
            low = 0
            last_was_high = False
            while not found_split:
                new_len = math.floor((high+low)/2)
                new_width = font.size(text[:new_len])[0]
                if new_width > width-40:
                    high = new_len
                    last_was_high = True
                else:
                    low = new_len
                    if last_was_high:
                        split_len = new_len
                        found_split = True
                    last_was_high = False
            text_surface_1 = font.render(text[:split_len], False, (0, 0, 0))
            text_surface_2 = font.render(text[split_len:], False, (0, 0, 0))
            self.surface.blit(text_surface_1, (20, 20))
            self.surface.blit(text_surface_2, (20, text_surface_1.get_rect().height + 20))
        else:
            text_surface = font.render(text, False, (0, 0, 0))
            self.surface.blit(text_surface, (20, 20))


#class to manage buttons within a UIbox.
class UIbutton:
    def __init__(self, text, font):
        self.font = font
        width = self.font.size(text)[0]
        height = self.font.size(text)[1]
        self.color = (0, 0, 0)
        self.text = text
        self.pos = (0, 0)
        self.surface = self.font.render(text, False, self.color)

    def update_surface(self):
        self.surface = self.font.render(self.text, False, self.color)

#class to display clickable options.
class UIbox(Box):
    def __init__(self, ops, x, y, width, height, color, border_width = 10, border_color = (100, 200, 100)):
        #make the box
        Box.__init__(self, x, y, width, height, color, border_width, border_color)
        self.ops = ops
        pg.font.init()
        self.font = pg.font.SysFont("Sans-Serif", 30)
        # #make the options
        self.options = []
        for op in self.ops:
            self.options.append(UIbutton(op, self.font))
        self.color = color
        self.draw()


    def get_clicked(self, pos):
        for op in self.options:
            if op.surface.get_rect(topleft=op.pos).collidepoint((pos[0]-self.rect.x, pos[1]-self.rect.y)):
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
        for option in self.options:
            option.update_surface()
        #blit options to UIbox's surface
        current_x = 20
        current_y = 20
        length = self.font.size(self.get_longest().text)[0] + 20
        height = self.font.size(self.options[0].text)[1] + 15
        for op in self.options:
            if current_x + length + 20 > self.rect.width:
                current_y += height
                current_x = 20
                self.surface.blit(op.surface, (current_x, current_y))
                op.pos = (current_x, current_y)
                current_x += length
            else:
                self.surface.blit(op.surface, (current_x, current_y))
                op.pos = (current_x, current_y)
                current_x += length
