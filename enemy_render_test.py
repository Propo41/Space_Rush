import os
import sys
from random import random, randrange
from random import randint

import pygame


def load_image(name):
    image = pygame.image.load(name)
    return image


ENEMY_SPRITE_INTERVAL = pygame.USEREVENT + 1
ENEMY_SPAWN_INTERVAL = pygame.USEREVENT + 2

pygame.time.set_timer(ENEMY_SPRITE_INTERVAL, 50)
pygame.time.set_timer(ENEMY_SPAWN_INTERVAL, 1000)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.images = []
        for image in os.listdir('Assets/enemy'):  # an efficient way to load all images in a folder
            self.images.append(pygame.image.load(image))
        # starting pos is randomly generated

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 91, 91)

    def update(self, val):
        """This method iterates through the elements inside self.images and displays the next one each tick. For a
        slower animation, I used a user-defined event called ENEMY_SPRITE_INTERVAL. This works like
        iSetTimer(func, time) """
        if val == "INTERVAL":
            self.index += 1
            if self.index >= len(self.images):
                self.index = len(self.images) - 1
            self.image = self.images[self.index]
        else:
            self.spawn_randomly()

    def spawn_randomly(self):
        self.rect.move_ip(0, 5)
        if self.rect.bottom >= 850:
            self.kill()
            print("killed")


def main():
    pygame.init()
    CLOCK = pygame.time.Clock()
    FPS = 60
    screen = pygame.display.set_mode((550, 850))
    my_group = pygame.sprite.Group()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == ENEMY_SPRITE_INTERVAL:
            my_group.update("INTERVAL")
            pass
        if event.type == ENEMY_SPAWN_INTERVAL:
            new_group = Enemy()
            my_group.add(new_group)

        # Calling the 'my_group.update' function calls the 'update' function of all
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        screen.fill((0, 0, 0))
        my_group.draw(screen)
        my_group.update("SPAWN")
        CLOCK.tick(FPS)
        pygame.display.flip()


main()
