import pygame
from round import Round
from menu import *
from settings import *

class Game():

    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.DISPLAY_W = 800
        self.DISPLAY_H = int(self.DISPLAY_W + SIZES['FOOTER'] * self.DISPLAY_W)
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W,self.DISPLAY_H))
        self.timer = pygame.time.Clock()
        self.curr_round = None
        self.options_menu = OptionsMenu(self)
        self.main_menu = MainMenu(self)
        self.curr_frame = self.main_menu

        self.KEYS = {
            'K_PAUSE': False,
            'K_UP'   : False,
            'K_DOWN' : False,
            'K_LEFT' : False,
            'K_RIGHT': True,
            'K_SPACE': False,
        }

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause()
                if event.key == pygame.K_PAUSE:
                    self.KEYS['K_PAUSE'] = not self.KEYS['K_PAUSE']
                if event.key == pygame.K_UP:
                    self.KEYS['K_UP'], self.KEYS['K_DOWN'], self.KEYS['K_RIGHT'], self.KEYS[
                        'K_LEFT'] = True, False, False, False
                if event.key == pygame.K_DOWN:
                    self.KEYS['K_UP'], self.KEYS['K_DOWN'], self.KEYS['K_RIGHT'], self.KEYS[
                        'K_LEFT'] = False, True, False, False
                if event.key == pygame.K_RIGHT:
                    self.KEYS['K_UP'], self.KEYS['K_DOWN'], self.KEYS['K_RIGHT'], self.KEYS[
                        'K_LEFT'] = False, False, True, False
                if event.key == pygame.K_LEFT:
                    self.KEYS['K_UP'], self.KEYS['K_DOWN'], self.KEYS['K_RIGHT'], self.KEYS[
                        'K_LEFT'] = False, False, False, True
                if event.key == pygame.K_SPACE:
                    self.KEYS['K_SPACE'] = not self.KEYS['K_SPACE']

    def pause(self):
        self.curr_frame = self.main_menu
        self.main_menu._widgets[1]._visible = True

    def start_new_round(self):
        self.curr_round = Round(self)
        self.curr_frame = self.curr_round
        self.main_menu.close()

    def continue_current_round(self):
        self.curr_frame = self.curr_round

    # def reset_keys(self):
    #     for key in self.KEYS:
    #         self[key] = False


    def game_loop(self):

        pygame.display.flip()
        self.check_events()
        pass
        # while self.playing:


        # pygame.display.update()
        # # self.reset_keys()




