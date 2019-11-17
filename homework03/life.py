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
        self.grid = self.create_grid(randomize=True)

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
        new_grid = self.create_grid()
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                neighbours_count = self.get_neighbours((y, x)).count(1)
                if self.grid[y][x] == 0:
                    if neighbours_count == 3:
                        new_grid[y][x] = 1
                else:
                    if neighbours_count in [2, 3]:
                        new_grid[y][x] = 1
        return new_grid

    def run(self):
        grid = GameOfLife.create_grid(self, randomize=True)
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        k = 1
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    cell = event.pos
                    position = GameOfLife.get_number_cell(self, cell)
                    x, y = position
                    self.grid = prev_grid
                    if self.grid[y][x] == 0:
                        self.grid[y][x] = 1

                    else:
                        self.grid[y][x] = 0
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    print(cell)
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        k += 1
            if k % 2 == 0:
                continue
            prev_grid = self.grid
            self.draw_grid()
            self.grid = self.get_next_generation()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def get_number_cell(self, cell: list):
        x, y = cell
        x //= self.cell_size
        y //= self.cell_size
        cell = (x, y)
        return cell

    def create_grid(self, randomize: bool = False):
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
    game = GameOfLife()
    game.grid = game.create_grid(True)

    game.run()
