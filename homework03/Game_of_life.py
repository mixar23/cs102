import random
import pathlib

from copy import deepcopy


class GameOfLife:

    def __init__(self,size,randomize: bool = True,max_generations:[float] = float('inf')) -> None:
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
        #текущее состояние поля
        self.grid = self.create_grid

    def create_grid(self, randomize: bool=False):
        # Copy from previous assignment
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
        for i in range(self.rows):
            grid.append(0)
        for i in range(self.rows):
            grid[i] = list()
            for l in range(self.cols):
                if randomize:
                    f = random.randint(0, 1)
                    grid[i].append(f)
                else:
                    grid[i].append(0)
        return grid

    def get_neighbours(self, cell):
        # Copy from previous assignment
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
        if x + 1 <= self.rows - 1:
            neighbours.append(self.grid[x + 1][y])
            if y + 1 <= self.cols - 1:
                neighbours.append(self.grid[x + 1][y + 1])
            if y - 1 >= 0:
                neighbours.append(self.grid[x + 1][y - 1])
        if x - 1 >= 0:
            neighbours.append(self.grid[x - 1][y])
            if y - 1 >= 0:
                neighbours.append(self.grid[x - 1][y - 1])
            if y + 1 <= self.cols - 1:
                neighbours.append(self.grid[x - 1][y + 1])
        if y + 1 <= self.cols - 1:
            neighbours.append(self.grid[x][y + 1])
        if y - 1 >= 0:
            neighbours.append(self.grid[x][y - 1])

        return neighbours

    def get_next_generation(self):
        # Copy from previous assignment
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

    def step(self):
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = deepcopy(self.curr_generation)
            self.curr_generation = self.get_next_generation()
            self.number_generation += 1

    @property
    def is_max_generations_exceeded(self,quantity_of_steps) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.number_generation > self.max_generations:
            return True
        else:
            return False
        


    @property
    def is_changing(self,grid) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation(grid) != self.prev_generation:
            return True
        else:
            return False


    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            grid = [[int(x) for x in list(row)] for row in file.readlines()]
        rows, cols = len(grid), len(grid[0])
        game = GameOfLife((rows,cols))
        game.curr_generation = grid
        return game

    def save(self,filename: pathlib.Path):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write(''.join([str(x) for x in row]))
                file.write('\n')

        
