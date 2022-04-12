import sys
import pygame
import time
from typing import List

OPTION_COLOR = (255, 255, 255)
FONT_FAMILY = 'Corbel'
FONT_SIZE = 35
FONT_COLOR = (0, 0, 0)

from stmt import *

'''
Template To Follow

class VNGame:
    options: Options = None

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
        self.options = options
        # Clear Previous Options
        # Display Options (store locations of each)
        pass

    def delay(self, value: int) -> None:
        # Delay (Check For Events While At it (like quit))
        pass

    def waitChoice(self) -> None:
        # Check Event for Option Click (or check input for console)
        # Use stored locations / index n stuff
        # Return Stmt Belonging To Case
        pass

    --- for gui only ---
    def showImage(self, path: str) -> None:
        # store image path -> Image object
        # show image (on top of any existing images)
        pass

    def hideImage(self, path: str) -> None:
        # lookup stored images, delete it
        # rerender all images

    def startAudio / stopAudio
'''


class VNConsoleGame:
    options = None

    def __init__(self) -> None:
        pass

    def display(self, text: str) -> None:
        pass

    def setOptions(self, options: Options) -> None:
        self.options = options
        pass

    def delay(self, value: int) -> None:
        pass

    def waitChoice(self) -> None:
        pass

class VNGUIGame:
    options = None
    imagelist = {}
    audiolist = {}

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

    def display(self, path: str):
        self.checkEvents()
        pic = pygame.image.load(path)
        pic = pygame.transform.scale(pic, (self.width, self.height))
        self.screen.blit(pic, (0, 0))
        self.render()

    def wait(self, number: int):
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