import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation
        try:
            for row in range(self.life.rows):
                for col in range(self.life.cols):
                    screen.addstr(row + 1, col + 1, "*" if grid[row][col] else " ")
        except curses.error:  # type: ignore
            pass

    def run(self) -> None:
        screen = curses.initscr()

        max_rows, max_cols = screen.getmaxyx()
        max_rows -= 2  # Учтем границы экрана
        max_cols -= 2

        self.life.rows = min(self.life.rows, max_rows)
        self.life.cols = min(self.life.cols, max_cols)
        subwin = screen.subwin(self.life.rows + 2, self.life.cols + 2, 0, 0)

        while True:
            self.draw_borders(subwin)
            self.draw_grid(subwin)

            subwin.refresh()
            self.life.step()

            if subwin.getch() == ord("q"):
                curses.endwin()
                break


if __name__ == "__main__":
    game = GameOfLife(size=(25, 70), randomize=True, max_generations=0)
    console = Console(life=game)
    console.run()

curses.endwin()  # type: ignore
