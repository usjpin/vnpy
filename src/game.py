import sys
import pygame
import time

class Game:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        pygame.init()
        pygame.display.set_mode((self.width, self.height))

    def show(self, path: str):
        self.checkEvent()
        pic = pygame.image.load(path)
        pic = pygame.transform.scale(pic, (self.width, self.height))
        pygame.display.get_surface().blit(pic, (0, 0))
        pygame.display.flip()

    def wait(self, number: int):
        i = 0
        while i < number:
            self.checkEvent()
            i += 1
            time.sleep(1)

    def checkEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        return pygame.event.get()