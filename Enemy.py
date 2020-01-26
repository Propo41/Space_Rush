import glob
import pygame
from random import randrange


def load_images(dir_name):
    images = []
    for image in glob.glob(dir_name):  # an efficient way to load all images in a folder
        images.append(pygame.image.load(image))
    return images


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()

        self.images = []
        self.images = load_images("Assets/enemy/*.png")

        # starting pos is randomly generated
        self.spawn_rate = 1  # as time increases, the rate will go up
        self.spawn_dir = 0  # 0 indicates object will move vertically downwards.
        self.index = 0
        self.image = self.images[self.index]

        self.rect = pygame.Rect(randrange(0, 450), randrange(-100, 200), 50, 50)

    def update(self, val, spawn_rate):
        """This method iterates through the elements inside self.images and displays the next one each tick. For a
        slower animation, I used a user-defined event called ENEMY_SPRITE_INTERVAL. This works like
        iSetTimer(func, time) """
        self.spawn_rate = spawn_rate
        if val == "INTERVAL":
            self.sprite_interval()
        elif val == "SPAWN":
            self.spawn_randomly()

    def sprite_interval(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = len(self.images) - 1
        self.image = self.images[self.index]

    def spawn_randomly(self):
        self.rect.move_ip(self.spawn_dir, self.spawn_rate)
        if self.rect.bottom >= 800:
            self.kill()
            # print("killed")
