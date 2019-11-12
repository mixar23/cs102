import curses

from ui import UI
from life import GameOfLife
class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток """
        pass

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.endwin()