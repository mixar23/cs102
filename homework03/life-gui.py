import pygame

from Game_of_life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        # ...
        super().__init__(life)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
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

    def run(self) -> None:
        # Copy from previous assignment
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
            self.grid = self.get_next_generation()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
