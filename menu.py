import pygame
import pygame_menu


class Menu(pygame_menu.Menu):

    def __init__(self, game):
        self.game = game

        super().__init__(width=400, height=400,title='',
                                theme=pygame_menu.themes.THEME_BLUE)


    def display(self):
        self.mainloop(self.game.window,disable_loop=True)

class MainMenu(Menu):

    def __init__(self, game):

        super().__init__(game)

        self.set_title('MENU')
        self.add.button('New game', self.game.start_new_round)
        self.add.button('Continue', self.game.continue_current_round)
        self._widgets[1]._visible = False

        def display_options_menu():
            self.game.curr_frame = self.game.options_menu

        self.add.button('Option', display_options_menu)
        self.add.button('Quit', pygame_menu.events.EXIT)

class OptionsMenu(Menu):

    def __init__(self, game):

        super().__init__(game)

        self.ignore_walls = False
        self.ignore_tail  = False
        self.box_size_x = 20
        self.box_size_y = 20
        self.speed = 3
        self.acceleration = 7


        self.set_title('OPTIONS')

        def set_ignore_walls(value1, value2):
            self.ignore_walls = value2
            if self.game.curr_round != None:
                self.game.curr_round.snake.ignore_walls = value2

        def set_ignore_tail(value1, value2):
            self.ignore_tail = value2
            if self.game.curr_round != None:
                self.game.curr_round.snake.ignore_tail = value2

        def bacl_to_main_menu():
            self.game.curr_frame = self.game.main_menu

        def set_box_size_x(value):
            self.box_size_x = value

        def set_box_size_y(value):
            self.box_size_y = value

        def set_speed(value):
            self.speed = value
            if self.game.curr_round != None:
                self.game.curr_round.snake.speed = value

        def set_acceleration(value):
            self.acceleration = value
            if self.game.curr_round != None:
                self.game.curr_round.snake.acceleration = value

        self.add.text_input('Speed: ', self.speed, input_type='input-int', onchange=set_speed)
        self.add.text_input('Acceleration: ', self.acceleration , input_type='input-int', onchange=set_acceleration)
        self.add.selector('Ignore walls: ', [('False', False), ('True', True)], onchange=set_ignore_walls)
        self.add.selector('Ignore tail :', [('False', False), ('True', True)], onchange=set_ignore_tail)
        self.add.text_input('Box size X: ', self.box_size_x, input_type='input-int', onchange=set_box_size_x)
        self.add.text_input('Box size Y: ', self.box_size_y, input_type='input-int', onchange=set_box_size_y)
        self.add.button('Back', bacl_to_main_menu)

    def display(self):
        if self.game.curr_round != None:
            self._widgets[0]._input_string = str(self.game.curr_round.snake.speed)
            self._widgets[1]._input_string = str(self.game.curr_round.snake.acceleration)
        self.mainloop(self.game.window, disable_loop=True)

# class RoundOverMenu(Menu):
#
#     def __init__(self, game):
#
#         super().__init__(game)
#
#         self.set_title('GAME OVER')
#         self.add.button('New game', self.game.start_new_round)
#         self.add.button('Continue', self.game.continue_current_round)