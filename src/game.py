import sys
import pygame
import time
from PIL import Image
from typing import List

OPTION_COLOR = (255, 255, 255)
OPTION_HOVER = (255, 255, 0)
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

    def render(self) -> None:
        pass

class VNGUIGame(VNGame):

    def __init__(self, width: int, height: int, volume: float):
        self.width = width
        self.height = height
        self.volume = volume
        self.imagePaths = []
        self.imageSurfaces = []
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

    def showImage(self, path: str = None):
        if path is not None:
            self.imagePaths.append(path)
            pic = pygame.image.load(path)
            pic = pygame.transform.scale(pic, (self.width, self.height))
            self.imageSurfaces.append(pic)
        self.screen.fill((0, 0, 0))
        for imageSurface in self.imageSurfaces:
            self.screen.blit(imageSurface, (0, 0))

    def hideImage(self, path: str):
        if path not in self.imagePaths:
            # Throw Error?
            return
        idx = self.imagePaths.index(path)
        self.imagePaths.pop(idx)
        self.imageSurfaces.pop(idx)
        self.showImage()

    def startAudio(self, path: str):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def stopAudio(self):
        pygame.mixer.music.stop()

    def display(self, text: str = None):
        x = int(self.width//50)
        y = int(self.height//2 - self.height//100)
        if text is not None:
            self.displayText = text
            w = self.width - 2 * x
            h = int(self.height//7) - int(self.height//50)
            r = int(self.width//25)
            s = pygame.Surface((w, h))
            s.set_alpha(100)
            pygame.draw.rect(s, OPTION_COLOR, [0, 0, w, h], border_radius = r)
            font = pygame.font.SysFont(FONT_FAMILY, int(h/1.5))
            message = font.render(text, True, FONT_COLOR)
            s.blit(message, (0.05 * w, 0.3 * h))
            self.displaySurface = s
        self.showImage()
        if self.displaySurface is not None:
            self.screen.blit(self.displaySurface, (x, y))

    def delay(self, number: int):
        i = 0
        while i < number:
            self.checkEvents()
            i += 1
            time.sleep(1)

    def popOptions(self, options: List[Tuple[str, Stmt]]) -> Stmt:
        while True:
            events = self.checkEvents()
            self.display()
            w = int(0.9 * self.width)
            h = int(self.height//(len(options) * 2.5)) - int(self.height//50)
            r = int(self.width//25)
            x = int(0.05 * self.width)
            y = int(self.height//2 + self.height//7 - self.height//100)
            for idx, option in enumerate(options):
                mux, muy = pygame.mouse.get_pos()
                mx = mux - x
                my = muy - y
                s = pygame.Surface((w, h))
                s.set_alpha(100)
                if mx >= 0 and mx <= w and my >= 0 and my <= h:
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            return options[idx][1]
                    pygame.draw.rect(s, OPTION_HOVER, [0, 0, w, h], border_radius = r)
                else:
                    pygame.draw.rect(s, OPTION_COLOR, [0, 0, w, h], border_radius = r)
                font = pygame.font.SysFont(FONT_FAMILY, int(h/1.5))
                message = font.render(option[0], True, FONT_COLOR)
                s.blit(message, (0.05 * w, 0.3 * h))
                self.screen.blit(s, (x, y))
                y += h + self.height//100
            self.render()

    def checkEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
        return events

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