import pygame


class Background:
    def __init__(self, dir, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(dir).convert()
        self.visible = True
        self.image.set_colorkey((0, 0, 0))

    def update(self, rate):
        self.y += rate  # images will flow downwards

    def get_image(self):
        return self.image

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def set_visible(self, val):
        self.visible = val
