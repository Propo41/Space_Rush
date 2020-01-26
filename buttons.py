import pygame


def load_image(address):
    return pygame.image.load(address).convert()


# state is a MACRO
PLAY = 1
OPTIONS = 2
HIGHSCORE = 3
EXIT = 4
NEXT = 5
RESTART = 6
BACK = 6
HOME = 7


class Button:
    def __init__(self, img_address, img_address_clicked, topleft_x, topleft_y, state):
        self.x = topleft_x
        self.y = topleft_y
        self.hovered = False
        self.img = load_image(img_address)
        self.img_hovered = load_image(img_address_clicked)
        self.rect = self.img.get_rect(topleft=(topleft_x, topleft_y))
        self.rect_hovered = self.img_hovered.get_rect(topleft=(topleft_x, topleft_y))
        self.state = state
