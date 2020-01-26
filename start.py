import os
import sys

import pygame

from main import Game

CLOCK = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 850


class StartGame:
    def __init__(self):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        print("hello")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.img = pygame.image.load('Assets/background/name_window.png').convert()
        self.img_x = 0
        self.img_y = 0
        self.font = pygame.font.Font('SigmarOne.ttf', 24)
        self.entered_name = ""

        self.running = True
        self.game_loop()

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        self.entered_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.entered_name = self.entered_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.running = False
                        Game(self.entered_name)
            self.display()
            pygame.display.update()
            CLOCK.tick(FPS)

    def display(self):
        self.screen.blit(self.img, (self.img_x, self.img_y))
        name_tag = self.font.render(self.entered_name, True, (238, 238, 238))
        name_rect = name_tag.get_rect()
        name_rect.center = self.screen.get_rect().center
        name_rect.y = 330
        self.screen.blit(name_tag, name_rect)


a = StartGame()
