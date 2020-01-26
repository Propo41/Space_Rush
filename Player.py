import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.life = 5
        self.x = 275
        self.y = 700
        self.surf_mid = pygame.image.load('Assets/player/char_1_mid.png').convert()
        self.surf_left = pygame.image.load('Assets/player/char_1_left.png').convert()
        self.surf_right = pygame.image.load('Assets/player/char_1_right.png').convert()

        self.rect_mid = self.surf_mid.get_rect().move(self.x, self.y)
        self.rect_left = self.surf_left.get_rect().move(self.x, self.y)
        self.rect_right = self.surf_right.get_rect().move(self.x, self.y)

        self.left = False
        self.right = False
        self.mid = True

    def init_character(self):
        pass

    def update_dir(self, dir):
        if dir == "left":
            self.left = True
            self.right = False
            self.mid = False
        elif dir == "right":
            self.left = False
            self.right = True
            self.mid = False
        elif dir == "mid":
            self.left = False
            self.right = False
            self.mid = True
