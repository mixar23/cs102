import pygame
import random
from pprint import pprint as pp
from pygame.locals import *


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 80, speed: int = 10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание списка клеток
        self.grid = self.create_grid(randomize = True)

    def draw_lines(self):
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self):
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        index = -1
        for i in self.grid:
            index += 1
            s = -1
            for l in self.grid[index]:
                s += 1
                x, y = s, index
                if self.grid[index][s] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell):
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        x, y = cell
        if x + 1 <= self.cell_height - 1:
            neighbours.append(self.grid[x + 1][y])
            if y + 1 <= self.cell_width - 1:
                neighbours.append(self.grid[x + 1][y + 1])
            if y - 1 >= 0:
                neighbours.append(self.grid[x + 1][y - 1])
        if x - 1 >= 0:
            neighbours.append(self.grid[x - 1][y])
            if y - 1 >= 0:
                neighbours.append(self.grid[x - 1][y - 1])
            if y + 1 <= self.cell_width - 1:
                neighbours.append(self.grid[x - 1][y + 1])
        if y + 1 <= self.cell_width - 1:
            neighbours.append(self.grid[x][y + 1])
        if y - 1 >= 0:
            neighbours.append(self.grid[x][y - 1])

        return neighbours

    def get_next_generation(self):
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        New_grid = self.grid
        for i in range(len(self.grid)):
            for l in range(len(self.grid[i])):
                sosedi = GameOfLife.get_neighbours(self, [i, l])
                s = 0
                for k in sosedi:
                    if k == 1:
                        s += 1
                if (s == 2) or (s == 3):
                    New_grid[i][l] = 1
                else:
                    New_grid[i][l] = 0
        self.grid = New_grid
        return self.grid

    def run(self):
        grid = GameOfLife.create_grid(self, randomize=True)
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            grid = self.get_next_generation()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize):
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = list()
        for i in range(self.cell_height):
            grid.append(0)
        for i in range(self.cell_height):
            grid[i] = list()
            for l in range(self.cell_width):
                if randomize:
                    f = random.randint(0, 1)
                    grid[i].append(f)
                else:
                    grid[i].append(0)
        return grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 10)
    game.run()

