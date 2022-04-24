import sys
import pygame
import time
from typing import List

OPTION_COLOR = (255, 255, 255)
OPTION_HOVER = (255, 255, 255)
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
        y = int(self.height - self.height // 4)
        if text is not None:
            self.displayText = text
            w = self.width - 2 * x
            h = int(self.height//4) - int(self.height//50)
            r = int(self.width//25)
            s = pygame.Surface((w, h))
            s.set_alpha(256)
            pygame.draw.rect(s, OPTION_COLOR, [0, 0, w, h], border_radius = r)

            #for text wrapping
            fontSize = h/3.5
            charsPerLine = int(w // (fontSize * 1/2))
            font = pygame.font.SysFont(FONT_FAMILY, int(fontSize))
            textArray = [ text[i:i+charsPerLine] for i in range(0, len(text), charsPerLine) ]
            for i in range(len(textArray)):  
                message = font.render(textArray[i], True, FONT_COLOR)
                s.blit(message, (0.05 * w, (h*0.1) + 0.3 * h * i))
            self.displaySurface = s

        self.showImage()
        if self.displaySurface is not None:
            self.screen.blit(self.displaySurface, (x, y))

    def delay(self, number: int):
        i = 0
        while i < number * 10:
            self.checkEvents()
            i += 1
            time.sleep(0.1)

    def popOptions(self, options: List[Tuple[str, Stmt]]) -> Stmt:
        while True:
            events = self.checkEvents()
            self.display()
            w = int(0.9 * self.width)
            h = int(self.height//10) - int(self.height//50) #int(self.height//(len(options) * 5.5)) - int(self.height//50)
            r = int(self.width//25)
            x = int(0.05 * self.width)
            y = int(self.height//3)
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
                y += h + self.height//50
            self.render()

    def getClick(self):
        while True:
            events = self.checkEvents()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
            time.sleep(0.01)

    def getKey(self):
        while True:
            events = self.checkEvents()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    return
            time.sleep(0.01)

    def checkEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit(0)
        return events

    def render(self):
        pygame.display.flip()


#from PIL import Image
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