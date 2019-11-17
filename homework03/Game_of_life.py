import pathlib
import random

from copy import deepcopy
from typing import Optional, Tuple


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.number_generation = 1

    def create_grid(self, randomize: bool = False):
        # Copy from previous assignment
        grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for y in range(self.rows):
                for x in range(self.cols):
                    grid[y][x] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell):
        # Copy from previous assignment
        neighbours = []
        x, y = cell
        if x + 1 <= self.rows - 1:
            neighbours.append(self.curr_generation[x + 1][y])
            if y + 1 <= self.cols - 1:
                neighbours.append(self.curr_generation[x + 1][y + 1])
            if y - 1 >= 0:
                neighbours.append(self.curr_generation[x + 1][y - 1])
        if x - 1 >= 0:
            neighbours.append(self.curr_generation[x - 1][y])
            if y - 1 >= 0:
                neighbours.append(self.curr_generation[x - 1][y - 1])
            if y + 1 <= self.cols - 1:
                neighbours.append(self.curr_generation[x - 1][y + 1])
        if y + 1 <= self.cols - 1:
            neighbours.append(self.curr_generation[x][y + 1])
        if y - 1 >= 0:
            neighbours.append(self.curr_generation[x][y - 1])

        return neighbours

    def get_next_generation(self):
        # Copy from previous assignment
        new_grid = self.create_grid()
        for y in range(self.rows):
            for x in range(self.cols):
                neighbours_n = self.get_neighbours((y, x)).count(1)
                if self.curr_generation[y][x] == 0:
                    if neighbours_n == 3:
                        new_grid[y][x] = 1
                else:
                    if neighbours_n in [2, 3]:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceed:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.number_generation += 1

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.number_generation >= self.max_generations:
            return True
        else:
            return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        else:
            return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            grid = [[int(x) for x in list(row)] for row in f.readlines()]
        rows, cols = len(grid), len(grid[0])

        game = GameOfLife((rows, cols))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as f:
            for row in self.curr_generation:
                f.write(''.join([str(x) for x in row]))
                f.write('\n')

        