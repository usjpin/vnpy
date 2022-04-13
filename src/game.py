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

    def setOptions(self, options: Options) -> None:
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

    def setOptions(self, options: Options) -> None:
        self.options = options
        pass

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
        x = 10
        y = self.height/2 + 5
        pygame.draw.rect(
            self.screen, OPTION_COLOR,
            [x, y, self.width - 20, self.height/6 - 10],
            border_radius = 20
        )
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        message = font.render(text, True, FONT_COLOR)
        self.screen.blit(message, (x + 20, y + 20))
        self.render()

    def delay(self, number: int):
        i = 0
        while i < number:
            self.checkEvents()
            i += 1
            time.sleep(1)

    def createOption(self, message):
        x = 10
        y = self.height/2 + 5
        pygame.draw.rect(
            self.screen, OPTION_COLOR,
            [x, y, self.width - 20, self.height/6 - 10],
            border_radius = 20
        )
        font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        text = font.render(message, True, FONT_COLOR)
        self.screen.blit(text, (x + 20, y + 20))
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