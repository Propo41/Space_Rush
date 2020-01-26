import os
import random
import sys

from typing import List

import main
from Enemy import Enemy
from pygame import mixer, KEYDOWN

import pygame
from Player import Player
from background import Background
from buttons import Button, RESTART, HOME

# from main import button_mechanics
# from main import Game

CLOCK = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 850
PURPLE = (34, 0, 84)


def button_mechanics(target):
    mouse_pos = pygame.mouse.get_pos()
    for img in target:
        if img.rect.collidepoint(mouse_pos):
            # print("mouse hovered")
            img.hovered = True
        else:
            img.hovered = False


# sorts the file
def sort_file():
    list_scores1 = []
    with open("highscores.txt", "r") as f:
        for line in f:
            temp = line.splitlines()
            temp2 = (temp[0].split(' '))
            if len(temp2) <= 1:
                pass
            else:
                list_scores1.append((temp2[0], int(temp2[1])))
    # print(list_scores1)
    list_scores1 = sorted(list_scores1, key=lambda s: s[1], reverse=True)
    # output this data to file
    i = 0
    with open("highscores.txt", "w") as file_ptr:
        for line in list_scores1:
            file_ptr.write("%s %d\n" % (list_scores1[i][0], list_scores1[i][1]))
            i += 1
    print("file sorted")


class GameOverWindow:
    def __init__(self, score_val, player_name):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mouse.set_visible(True)
        self.running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gameover_buttons = []
        self.gameover_buttons.append(Button('Assets/UI/restart.png', 'Assets/UI/restart_1.png', 206, 425, 6))
        self.gameover_buttons.append(Button('Assets/UI/home.png', 'Assets/UI/home_1.png', 296, 425, 7))
        self.game_over_font = pygame.font.Font('SigmarOne.ttf', 55)
        self.game_over_tag = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.player_name = player_name

        self.obtained_score_font = pygame.font.Font('SigmarOne.ttf', 30)
        self.obtained_score_tag = self.obtained_score_font.render("SCORE: " + str(score_val), True, (255, 255, 255))
        self.score_tag_rect = self.obtained_score_tag.get_rect()
        self.score_tag_rect.center = (275, 310)
        self.score_tag_rect.y = 320

        # sound effects: MOVE IT TO UTIL FILE LATER
        self.click_sound = pygame.mixer.Sound('Assets/music/clicked.wav')
        self.hover_sound = pygame.mixer.Sound('Assets/music/hover.wav')
        mixer.music.load('Assets/music/game_over_music.wav')
        mixer.music.play()

        # save high score to file and then sort the file
        self.save_score(player_name, score_val)
        sort_file()

        self.game_loop()

    def display(self):
        self.screen.fill(PURPLE)
        # display font
        self.screen.blit(self.game_over_tag, (85, 200))  # displays GAME OVER tag
        self.screen.blit(self.obtained_score_tag, self.score_tag_rect)  # displays GAME OVER tag
        # display buttons
        for i in self.gameover_buttons:
            if i.hovered:
                i.img_hovered.set_colorkey((0, 0, 0))
                self.screen.blit(i.img_hovered, (i.x, i.y))
            else:
                i.img.set_colorkey((0, 0, 0))
                self.screen.blit(i.img, (i.x, i.y))

    def check_hovered_state(self, buttons_list):
        # iterates through the buttons list and checks which buttons are clicked
        for img in buttons_list:  # check which buttons are in hovered state
            if img.hovered:
                self.click_sound.play()
                if img.state == RESTART:
                    print("starting game")
                    self.running = False
                    GameWindow(self.player_name)
                elif img.state == HOME:
                    print("BACK TO HOME SCREEN ")
                    self.running = False
                    main.Game(self.player_name)

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # if left button pressed
                    self.click_sound.play()
                    self.check_hovered_state(self.gameover_buttons)

            elif event.type == pygame.MOUSEMOTION:  # mouse hover motions
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos[0], mouse_pos[1])

    def save_score(self, player_name, score):
        with open("highscores.txt", "a") as file_ptr:
            file_ptr.write("%s %d\n" % (player_name, score))
        print("saved score to txt file")

    def game_loop(self):
        while self.running:
            self.event_handling()
            button_mechanics(self.gameover_buttons)
            self.display()
            pygame.display.update()
            CLOCK.tick(FPS)


class GameWindow:
    ingame_bg: List[Background]
    collision_sound: mixer.Sound

    def __init__(self, player_name):
        # position the window at the center
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.running = True
        self.SCREEN_WIDTH = 550
        self.SCREEN_HEIGHT = 850
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.hp_bars_list = []
        self.init_assets()

        self.first_marker = 0  # a marker to indicate the end of the first picture
        self.removed = False  # used to handle when the first picture is rendered
        self.rate = 2  # the rate increases as player approaches higher scores

        self.enemy_group = pygame.sprite.Group()

        self.ENEMY_SPRITE_INTERVAL = pygame.USEREVENT + 1
        self.ENEMY_SPAWN_INTERVAL = pygame.USEREVENT + 2

        self.current_spawn_rate = 1500
        pygame.time.set_timer(self.ENEMY_SPRITE_INTERVAL, 50)
        pygame.time.set_timer(self.ENEMY_SPAWN_INTERVAL, self.current_spawn_rate)

        self.player = Player()
        self.player_name = player_name
        self.score_val = 0
        self.font = pygame.font.Font('SigmarOne.ttf', 30)
        self.paused_font = pygame.font.Font('SigmarOne.ttf', 57)
        self.score_x = 400
        self.score_y = 100
        self.score = 0

        # these are used to trigger the condition blocks in game_mechanics() only once
        self.final_spawn_rate_marker = False
        self.final_spawn_rate_marker_2 = False

        self.gameOver = False
        self.show_effects = False
        self.effects = pygame.image.load('Assets/effect.png').convert()
        self.show_effects_counter = 0
        self.init_sounds()
        self.paused = False
        self.game_loop()

    def init_assets(self):
        self.init_background()
        self.init_hud()

    def init_background(self):
        self.ingame_bg = [Background("Assets/background/0.png", 0, 0),
                          Background("Assets/background/1.png", 0, -850),
                          Background("Assets/background/2.png", 0, -1700)]

    def init_hud(self):
        hp_bar_img = pygame.image.load("Assets/hp.png").convert()
        for i in range(0, 5):
            self.hp_bars_list.append(hp_bar_img)
        self.pause_icon = pygame.image.load('Assets/pause.png').convert()
        self.pause_filter = pygame.image.load('Assets/pause_filter.png').convert()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit(0)

            if not self.paused:
                if event.type == self.ENEMY_SPRITE_INTERVAL:
                    self.enemy_group.update("INTERVAL", self.rate)
                elif event.type == self.ENEMY_SPAWN_INTERVAL:
                    new_group = Enemy()
                    self.enemy_group.add(new_group)
                    self.player.update_dir("mid")  # normally keep dir to mid
                elif event.type == pygame.MOUSEMOTION:  # player movement
                    self.player_mechanics()
            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("game paused")
                    if not self.paused:
                        self.paused = True
                        pygame.mouse.set_visible(True)
                        pygame.time.set_timer(self.ENEMY_SPAWN_INTERVAL, 0)
                    else:
                        self.paused = False
                        pygame.mouse.set_visible(False)
                        pygame.time.set_timer(self.ENEMY_SPAWN_INTERVAL, self.current_spawn_rate)

    def player_mechanics(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.player.x:  # mouse moving left
            self.player.update_dir("left")
        elif mouse_pos[0] > self.player.x:  # mouse moving left
            self.player.update_dir("right")

        self.player.x = mouse_pos[0]
        self.player.rect_mid.x = self.player.x
        self.player.rect_left.x = self.player.x
        self.player.rect_right.x = self.player.x

        if self.player.rect_mid.x >= 400 or self.player.rect_left.x >= 400 or self.player.rect_right.x >= 400:
            self.player.rect_mid.x = 400
            self.player.rect_left.x = 400
            self.player.rect_right.x = 400
            self.player.x = 400

    def game_mechanics(self):
        self.check_collision()
        self.enemy_group.update("SPAWN", self.rate)  # spawns enemies
        if self.score_val >= 200 and not self.final_spawn_rate_marker:  # when score hits 200 increase spawn rate
            pygame.time.set_timer(self.ENEMY_SPAWN_INTERVAL, 1000)  # add more logic later to keep increasing rate
            self.final_spawn_rate_marker = True
            print("spawn interval increased to 1000")
        elif self.score_val >= 1000 and not self.final_spawn_rate_marker_2:
            pygame.time.set_timer(self.ENEMY_SPAWN_INTERVAL, 700)  # add more logic later to keep increasing rate
            self.final_spawn_rate_marker_2 = True
            print("spawn interval increased to 700")

        self.calc_score()

    def background_mechanics(self):
        # keep iterating 0-1-2 and then when 0 is completely passed, iterate elements 1-2 indefinitely
        if not self.removed:
            for img in self.ingame_bg:
                img.update(self.rate)  # parameter: rate
                if self.first_marker >= self.SCREEN_HEIGHT and not self.removed:  # first picture passed, thus it's
                    # removed
                    self.ingame_bg.pop(0)
                    self.removed = True
            self.first_marker += self.rate
        else:  # a separate block is written to use the for loop with an index system.
            length = len(self.ingame_bg)
            for i in range(0, length):
                self.ingame_bg[i].update(self.rate)
                if self.ingame_bg[i].get_y() >= 850:
                    temp = self.ingame_bg[(i + 1) % length].get_y()
                    self.ingame_bg[i].set_y(temp - self.SCREEN_HEIGHT + 10)  # 10 is used to fill up a gap

    def display(self):
        self.display_background()
        self.display_character()
        if not self.gameOver:
            self.display_HUD()

    def display_background(self):
        self.screen.fill((0, 0, 0))
        for img in self.ingame_bg:
            self.screen.blit(img.get_image(), (img.get_x(), img.get_y()))
        if self.show_effects:
            self.effects.set_colorkey((0, 0, 0))
            self.screen.blit(self.effects, (0, 0))
            self.show_effects_counter += 1
            if self.show_effects_counter >= 2:
                self.show_effects = False
                self.show_effects_counter = 0

    def display_character(self):
        self.enemy_group.draw(self.screen)
        if self.player.mid:
            self.player.surf_mid.set_colorkey((0, 0, 0))
            self.screen.blit(self.player.surf_mid, (self.player.x, self.player.y))
        elif self.player.left:
            self.player.surf_left.set_colorkey((0, 0, 0))
            self.screen.blit(self.player.surf_left, (self.player.x, self.player.y))
        elif self.player.right:
            self.player.surf_right.set_colorkey((0, 0, 0))
            self.screen.blit(self.player.surf_right, (self.player.x, self.player.y))

    def display_HUD(self):
        # show score
        self.score = self.font.render("SCORE: " + str(int(self.score_val)), True, (255, 255, 255))
        self.screen.blit(self.score, (350, 20))  # displays score tag
        x = 20
        y = 30
        for img in self.hp_bars_list:  # displays life bars
            img.set_colorkey((0, 0, 0))
            self.screen.blit(img, (x, y))
            x += img.get_rect().width + 10
        self.pause_icon.set_colorkey((0, 0, 0))
        self.screen.blit(self.pause_icon, (15, 790))
        if self.paused:
            self.screen.blit(self.pause_filter, (0, 0))
            self.paused_tag = self.paused_font.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(self.paused_tag, (140, 389))  # displays score tag

    def check_collision(self):
        # if any sprite in the enemy_group collides with the sprite, then kill that sprite and
        # pop an element from the hp bars list
        # if player hp bars becomes less than 0, then game over
        for curr_sprite in self.enemy_group:
            if curr_sprite.rect.colliderect(self.player.rect_mid):
                print("collided")
                # play sound of collision
                self.collision_sound.play()

                curr_sprite.kill()
                self.player.life -= 1
                self.hp_bars_list.pop()
                self.show_effects = True
                if self.player.life <= 0:  # game over
                    print("game over")
                    self.gameOver = True
                    # pygame.time.wait(0)
                    self.running = False
                    mixer.music.stop()
                    GameOverWindow(int(self.score_val), self.player_name)

                # add overlay visual effect

    def game_loop(self):
        while self.running:
            self.event_handling()
            if not self.paused:
                self.background_mechanics()
                self.game_mechanics()
            self.display()
            pygame.display.update()
            CLOCK.tick(FPS)

    def calc_score(self):
        self.score_val += 0.15
        # increase rate of speed as time passes
        self.rate += 0.005

        # print(self.score_val)

    def init_sounds(self):
        self.collision_sound = mixer.Sound('Assets/music/collision.wav')
        mixer.music.load('Assets/music/bg_music.wav')
        mixer.music.play(-1)

# test_run = GameWindow()
# test_run = GameOverWindow(1500)
# GameOverWindow(1500, "Ahnaf")
