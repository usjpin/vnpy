import sys
import pygame
import time

OPTION_COLOR = (255, 255, 255)
FONT_FAMILY = 'Corbel'
FONT_SIZE = 35
FONT_COLOR = (0, 0, 0)

class Game:

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