import pygame

from settings import *
import datetime
import random

class Round():

    def __init__(self, game):

        self.game = game
        self.table = Table(game,game.options_menu.box_size_x,game.options_menu.box_size_y)
        self.snake = Snake(self.game, self.table)
        self.table.make_apple()

    def display_footer(self):

        size = self.game.DISPLAY_W * SIZES['FOOTER']

        footer_rect = pygame.draw.rect(self.game.window, COLORS['FOOTER'],
                                       [0, self.game.DISPLAY_H - size, self.game.DISPLAY_W,
                                        size])

        font_courier = pygame.font.SysFont('courier',40,True)

        text_total = font_courier.render(f"Total:{len(self.snake)}", 0, (255, 255, 255))
        text_speed = font_courier.render(f"Speed:{self.snake.speed}", 0, (255, 255, 255))

        self.game.window.blit(text_total, [self.game.DISPLAY_W // 4 - 85, footer_rect.centery - 20])
        self.game.window.blit(text_speed, [self.game.DISPLAY_W - self.game.DISPLAY_W // 4 - 85, footer_rect.centery - 20])

    def display(self):

        self.game.window.fill(COLORS['BACKGROUND'])

        self.snake.make_step()

        self.table.display()

        self.display_footer()

class Table(list):

    def __init__(self, game, x=20, y=20):

        self.game = game

        block_border_size = 1
        block_size = (self.game.DISPLAY_W) / (max(x,y) + 2) - block_border_size

        for column in range(y):
            table_row = []
            self.append(table_row)
            for row in range(x):
                block_left  = (block_size + block_border_size) * row + block_size + block_border_size
                block_top = (block_size + block_border_size) * column + block_size + block_border_size
                block = Block(self.game, row, column, block_left, block_top, block_size)
                table_row.append(block)

    def display(self):
        for table_row in self:
            for block in table_row:
                block.display()

    def make_apple(self):

        while True:
            block = self[random.randint(0, len(self)-1)][random.randint(0, len(self[0])-1)]
            if block.status == 1:
                break

        block.status = 3

class Snake(list):

    def __init__(self, game,  table, size=3):

        self.game = game
        self.table = table
        self.inversely = False
        middle = [(len(table[0])+1)//2-size, (len(table)+1)//2]
        for i in range(size):
            block = table[middle[1]][middle[0]+i]
            block.status = 2
            self.append(block)
        self.speed = self.game.options_menu.speed
        self.acceleration = self.game.options_menu.acceleration
        self.d_x = 1
        self.d_y = 0
        self.ignore_walls = self.game.options_menu.ignore_walls
        self.ignore_tail  = self.game.options_menu.ignore_tail

    def set_direction(self):

        if self.game.KEYS['K_UP'] and self.d_y != 1:
            self.d_x = 0
            self.d_y = -1
        elif self.game.KEYS['K_DOWN'] and self.d_y != -1:
            self.d_x = 0
            self.d_y = 1
        elif self.game.KEYS['K_LEFT'] and self.d_x != 1:
            self.d_x = -1
            self.d_y = 0
        elif self.game.KEYS['K_RIGHT'] and self.d_x !=-1:
            self.d_x = 1
            self.d_y = 0

    def turn_around(self):

        if self.game.KEYS['K_SPACE']:

            if (self[-1].y < self[-2].y) != (self[0].y < self[1].y):
                self.d_y*=-1
            if (self[-1].x < self[-2].x) != (self[0].x < self[1].x):
                self.d_x*=-1
            self.reverse()
            self.game.KEYS['K_SPACE'] = False
            self.inversely = not self.inversely

    def accelerate(self):

        if len(self) % self.acceleration == 0:
            self.speed += 1

    def make_step(self):

        self.set_direction()

        self.turn_around()

        head = self[-1]
        position = [head.x + self.d_x, head.y + self.d_y]
        if not self.check_next_position(position):
            return False

        new_head = self.table[position[1]][position[0]]

        tail = self[0]
        if new_head.status == 3:
            self.accelerate()
            self.table.make_apple()
        else:
            double = [i for i,d in enumerate(self) if d==tail]
            if not len(double)>1:
                tail.status = 1
            self.pop(0)

        self.game.timer.tick(self.speed)

        self.append(new_head)
        new_head.status = 4
        head.status = 2

        return True

    def check_next_position(self, position):

        result = True
        if self.ignore_walls:
            if position[1] == len(self.table):
                position[1] = 0

            if position[0] == len(self.table[0]):
                position[0] = 0
        else:
            if position[1] < 0 or position[0] < 0 or position[1] > len(self.table) - 1 or position[0] > len(self.table[0]) - 1:
                print('wall')
                result = False
                return result

        block = self.table[position[1]][position[0]]
        if not self.ignore_tail and block.status == 2:
            print('tail')
            result = False

        return result

class Block:

    def __init__(self, game, x, y, left, top, size):

        self.game = game
        self.x = x
        self.y = y
        self.size = size
        self.left = left
        self.top = top
        self._color = None
        self._status = None
        self.status = 1
        self.rect = None

    def display(self):
        self.rect =  pygame.draw.rect(self.game.window, self.color, [self.left, self.top, self.size, self.size])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):

        self._status = value
        if self._status == 1:
            if (self.x + self.y) % 2 == 0:
                self._color = COLORS['TABLE1']
            else:
                self._color = COLORS['TABLE2']
        elif self._status == 2:
            self._color = COLORS['SNAKE']
        elif self._status == 3:
            self._color = COLORS['APPLE']
        elif self._status == 4:
            self._color = COLORS['SNAKE_HEAD']
            # now = datetime.datetime.now()
            # if now.second % 2 == 0:
            #     self._color = COLORS['SNAKE_HEAD']
            # else:
            #     self._color = COLORS['SNAKE']

    @property
    def color(self):
        return self._color
