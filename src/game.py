import sys
import pygame
import time
from PIL import Image
from typing import List

OPTION_COLOR = (255, 255, 255)
FONT_FAMILY = 'Corbel'
FONT_SIZE = 35
FONT_COLOR = (0, 0, 0)

from stmt import *

class VNGame:

    def __init__(self) -> None:
        pass

    def display(self, text: str) -> None:
        # Clear Previous Text
        # Show Text
        pass

    def newScreen(self) -> None:
        # Clear the Screen
        pass

    def popOptions(self, options: List[Tuple[Token, Stmt]]) -> None:
        # Clear Previous Options
        # Display Options (store locations of each)
        pass

    def delay(self, value: int) -> None:
        # Delay (Check For Events While At it (like quit))
        pass


class VNConsoleGame(VNGame):

    def __init__(self) -> None:
        pass

    def display(self, text: str) -> None:
        print(text)

    def popOptions(self, options: List[Tuple[Token, Stmt]]) -> None:
        for idx, option in enumerate(options):
            print(str(idx+1) + ". " + option[0].literal)
        print("Pick An Option (Enter a Number):")
        valid = False
        while not valid:
            valid = True
            print(">> Option #", end = "")
            try:
                choice = int(input())-1
                if choice > len(options):
                    valid = False
            except:
                valid = False
            if valid == False:
                print("Incorrect Input, Pick Again:")
        return options[choice]

    def delay(self, value: int) -> None:
        i = 0
        while i < value:
            i += 1
            time.sleep(1)

class VNGUIGame(VNGame):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.imagelist = {}
        self.audiolist = {}
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

    def showImage(self, path: str):
        self.checkEvents()
        pic = pygame.image.load(path)
        pic = pygame.transform.scale(pic, (self.width, self.height))
        self.screen.blit(pic, (0, 0))
        self.render()

    def hideImage(self, path: str):
        pass

    def display(self, text: str):
        self.checkEvents()
        x = int(self.width//50)
        y = int(self.height//2 - self.height//100)
        w = self.width - 2 * x
        h = int(self.height//7) - int(self.height//50)
        r = int(self.width//25)
        s = pygame.Surface((w, h))
        s.set_alpha(100)
        pygame.draw.rect(s, OPTION_COLOR, [0, 0, w, h], border_radius = r)
        font = pygame.font.SysFont(FONT_FAMILY, int(h/1.5))
        message = font.render(text, True, FONT_COLOR)
        s.blit(message, (0.05 * w, 0.3 * h))
        self.screen.blit(s, (x, y))
        self.render()

    def delay(self, number: int):
        i = 0
        while i < number:
            self.checkEvents()
            i += 1
            time.sleep(1)

    def popOptions(self, options: List[Tuple[Token, Stmt]]) -> Stmt:
        # Implement Hover and Clicking
        w = int(0.9 * self.width)
        h = int(self.height//(len(options) * 2.5)) - int(self.height//50)
        r = int(self.width//25)
        x = int(0.05 * self.width)
        y = int(self.height//2 + self.height//7 - self.height//100)
        for idx, option in enumerate(options):
            s = pygame.Surface((w, h))
            s.set_alpha(100)
            pygame.draw.rect(s, OPTION_COLOR, [0, 0, w, h], border_radius = r)
            font = pygame.font.SysFont(FONT_FAMILY, int(h/1.5))
            message = font.render(option[0].literal, True, FONT_COLOR)
            s.blit(message, (0.05 * w, 0.3 * h))
            self.screen.blit(s, (x, y))
            y += h + self.height//100
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        return pygame.event.get()

    def render(self):
        pygame.display.flip()

# For later?
def to_ascii(path):
    img = Image.open(path)
    width, height = img.size
    aspect_ratio = height/width
    new_width = 140
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    chars = ["B","S","#","&","@","$","%","*","!",":","."]
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image