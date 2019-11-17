import curses
import time

from Game_of_life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
 
        screen.addstr(0, 0, '+' + self.life.cols * '-' + '+')
 
        for i in range(1, self.life.rows + 1):
            screen.addstr(i, 0, '|')
            screen.addstr(i, self.life.cols + 1, '|')
 
        screen.addstr(self.life.rows + 1, 0, '+' + self.life.cols * '-' + '+')
 
    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        print(self.life.curr_generation)
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                symbol = ' '
                if self.life.curr_generation[row][col] == 1:
                    symbol = '*'
                screen.addstr(row + 1, col + 1, symbol)

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while (
                self.life.is_changing and not self.life.is_max_generations_exceed
        ) and running:
            try:
                screen.clear()

                self.draw_borders(screen)
                self.draw_grid(screen)

                self.life.step()

                screen.refresh()
                time.sleep(0.5)

            except KeyboardInterrupt:
                running = False

        curses.endwin()


if __name__ == '__main__':
    life = GameOfLife((24, 80), max_generations=50)

    ui = Console(life)
    ui.run()