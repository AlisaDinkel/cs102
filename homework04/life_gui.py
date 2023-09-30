import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.cell_size = cell_size
        # Размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        grid = self.life.curr_generation
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                y, x = i * self.cell_size, j * self.cell_size
                color = pygame.Color("white") if grid[i][j] == 0 else pygame.Color("green")
                pygame.draw.rect(self.screen, color, [x, y, self.cell_size, self.cell_size])

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        pause = True
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click_x, click_y = pygame.mouse.get_pos()
                    y, x = click_x // self.cell_size, click_y // self.cell_size
                    self.life.curr_generation[x][y] = 1 - self.life.curr_generation[x][y]

                if not pause:
                    self.life.step()
                if not (not self.life.is_max_generations_exceeded and self.life.is_changing):
                    pause = True

            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife((20, 20), max_generations=10)
    gui = GUI(game)
    gui.run()
