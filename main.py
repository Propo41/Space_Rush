import glob
import os
import sys

import pygame

# ---------------------BUGS---------------------------


# main file. Connects all other files
# useful links: https://stackoverflow.com/questions/35001207/how-to-detect-collision-between-objects-in-pygame
# https://stackoverflow.com/questions/42577197/pygame-how-to-correctly-use-get-rect
# https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame
# https://stackoverflow.com/questions/57837263/how-to-spawn-and-track-multiple-random-objects-with-time-delay-in-pygame
# https://stackoverflow.com/questions/54166630/how-to-make-an-animation-in-pygame
# https://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
# https://stackoverflow.com/questions/54817961/pygame-collide-rect-is-detecting-a-non-existent-collision
# https://realpython.com/pygame-a-primer/#sprite-images


# load all images from a given directory
from buttons import Button, PLAY, OPTIONS, HIGHSCORE, NEXT, RESTART, EXIT, BACK
from game_window import GameWindow

CLOCK = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 850


def load_images(dir_name):
    images = []
    for image in glob.glob(dir_name):  # an efficient way to load all images in a folder
        images.append(pygame.image.load(image))
    return images


def load_image(address):
    return pygame.image.load(address).convert()


def button_mechanics(target):
    mouse_pos = pygame.mouse.get_pos()
    for img in target:
        if img.rect.collidepoint(mouse_pos):
            # print("mouse hovered")
            img.hovered = True
        else:
            img.hovered = False


# given a list of pairs, sort them in descending order
def sort_list(high_scores):
    pass


class HighScoreWindow:
    def __init__(self, player_name):
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        self.formatted_scores = ""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.high_scores = []
        self.running = True
        self.img = load_image('Assets/background/high_score.png')
        self.font = pygame.font.Font('SigmarOne.ttf', 22)
        self.click_sound = pygame.mixer.Sound('Assets/music/clicked.wav')
        self.player_name = player_name
        self.back_button = []
        self.back_button.append(Button('Assets/UI/back-1.png', 'Assets/UI/back.png', 25, 775, 6))

        self.name_tag = []
        self.import_highscores()
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.event_handling()
            button_mechanics(self.back_button)
            self.display()
            pygame.display.update()
            CLOCK.tick(FPS)

    def display(self):
        self.screen.blit(self.img, (0, 0))
        # display all imported texts with a formatting
        if self.back_button[0].hovered:
            self.back_button[0].img_hovered.set_colorkey((0, 0, 0))
            self.screen.blit(self.back_button[0].img_hovered, (self.back_button[0].x, self.back_button[0].y))
        else:
            self.back_button[0].img.set_colorkey((0, 0, 0))
            self.screen.blit(self.back_button[0].img, (self.back_button[0].x, self.back_button[0].y))

        self.display_scores()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)
            elif event.type == pygame.MOUSEMOTION:  # mouse hover motions
                mouse_pos = pygame.mouse.get_pos()
                # print(mouse_pos[0], mouse_pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # if left button pressed
                    # check which buttons are in hovered state
                    self.check_hovered_state(self.back_button)

    def import_highscores(self):
        with open("highscores.txt", "r") as file_ptr:  # always fetch max 5 lines from the file
            self.high_scores = file_ptr.readlines()
        cnt = 0
        for line in self.high_scores:
            if cnt >= 5:
                break
            split_line = line.splitlines()
            # print(split_line)
            temp2 = (split_line[0].split(' '))
            # print("temp2: ", temp2)
            if len(temp2) <= 1:
                print("empty list")
                formatted_line = '{:<12}'.format(temp2[0])
            else:
                formatted_line = '           {:<12}                    {:>12}'.format(temp2[0], temp2[1])
            print(formatted_line)
            self.name_tag.append(self.font.render(formatted_line, True, (238, 238, 238)))
            # str_a = temp2[0] + "      " + temp2[1]
            # self.name_tag.append(self.font.render(str_a, True, (238, 238, 238)))
            cnt += 1

    def check_hovered_state(self, back_button):
        if self.back_button[0].hovered:
            self.click_sound.play()
            if back_button[0].state == BACK:  # move to the desired window
                Game(self.player_name)
                self.running = False

    def display_scores(self):
        x, y = 30, 320
        for line in self.name_tag:
            self.screen.blit(line, (x, y))
            y += 40


class Game:
    def __init__(self, player_name):
        #  declare variables for UI navigation
        # load UI images and background images

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player_name = player_name
        self.running = True
        self.start_img = load_image('Assets/background/start.png')
        self.instructions_img = load_image('Assets/background/instructions.png')
        self.instruction_window = False
        self.all_buttons = []
        self.next_button = []
        self.next_button.append(Button('Assets/UI/next.png', 'Assets/UI/next_1.png', 476, 775, 5))
        self.init_buttons()

        # sound effects
        self.click_sound = pygame.mixer.Sound('Assets/music/clicked.wav')
        self.hover_sound = pygame.mixer.Sound('Assets/music/hover.wav')

        # fonts to display player name
        font = pygame.font.Font('SigmarOne.ttf', 20)
        self.player_name_tag = font.render(self.player_name, True, (255, 255, 255))

        self.game_loop()

    def game_loop(self):
        while self.running:
            self.event_handling()
            if not self.instruction_window:
                button_mechanics(self.all_buttons)
            else:
                button_mechanics(self.next_button)

            self.display()
            pygame.display.update()
            CLOCK.tick(FPS)

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)
            elif event.type == pygame.MOUSEMOTION:  # mouse hover motions
                mouse_pos = pygame.mouse.get_pos()
                # print(mouse_pos[0], mouse_pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # if left button pressed
                    # check which buttons are in hovered state
                    self.check_hovered_state(self.all_buttons)
                    self.check_hovered_state(self.next_button)

    def check_hovered_state(self, buttons_list):
        # iterates through the buttons list and checks which buttons are clicked
        for img in buttons_list:  # check which buttons are in hovered state
            if img.hovered:
                self.click_sound.play()
                if img.state == PLAY:  # move to the desired window
                    self.instruction_window = True
                elif img.state == NEXT:
                    print("starting game")
                    self.running = False
                    GameWindow(self.player_name)
                elif img.state == EXIT:
                    sys.exit(0)
                elif img.state == OPTIONS:
                    pass
                elif img.state == HIGHSCORE:
                    self.running = False
                    HighScoreWindow(self.player_name)

    def display(self):
        self.screen.fill((0, 0, 0))
        if self.instruction_window:
            self.screen.blit(self.instructions_img, (0, 0))
            if self.next_button[0].hovered:
                self.next_button[0].img_hovered.set_colorkey((0, 0, 0))
                self.screen.blit(self.next_button[0].img_hovered, (self.next_button[0].x, self.next_button[0].y))
            else:
                self.next_button[0].img.set_colorkey((0, 0, 0))
                self.screen.blit(self.next_button[0].img, (self.next_button[0].x, self.next_button[0].y))
        else:
            self.screen.blit(self.start_img, (0, 0))  # displays start image in background
            # display name on top right corner
            self.screen.blit(self.player_name_tag, (SCREEN_WIDTH - self.player_name_tag.get_rect().width - 10, 5))
            # display buttons
            for i in self.all_buttons:
                if i.hovered:
                    i.img_hovered.set_colorkey((0, 0, 0))
                    self.screen.blit(i.img_hovered, (i.x, i.y))
                else:
                    i.img.set_colorkey((0, 0, 0))
                    self.screen.blit(i.img, (i.x, i.y))

    # img_address, img_address_clicked, topleft_x, topleft_y
    def init_buttons(self):
        self.all_buttons.append(Button('Assets/UI/play.png', 'Assets/UI/play_1.png', 175, 250, 1))
        self.all_buttons.append(Button('Assets/UI/options.png', 'Assets/UI/options_1.png', 150, 500, 2))
        self.all_buttons.append(Button('Assets/UI/highscore.png', 'Assets/UI/highscore_1.png', 150, 600, 3))
        self.all_buttons.append(Button('Assets/UI/exit.png', 'Assets/UI/exit_1.png', 150, 700, 4))

# game = Game()
