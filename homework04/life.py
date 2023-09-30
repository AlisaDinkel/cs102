import copy
import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [[random.choice([0, 1]) if randomize else 0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                y, x = cell[0] + j, cell[1] + i
                if i == 0 and j == 0:
                    continue
                elif -1 < x < self.cols and -1 < y < self.rows:
                    neighbours.append(self.curr_generation[y][x])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                if sum(neighbours) not in (2, 3) and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 0
                elif sum(neighbours) == 3 and self.curr_generation[i][j] == 0:
                    new_grid[i][j] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation, self.curr_generation = self.curr_generation, self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
            # if self.max_generations == 0:
            # return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with filename.open() as file:
            grid = [list(map(int, col.strip())) for col in file.readlines()]

        size = len(grid), len(grid[0])

        new_game = GameOfLife(size, randomize=False)
        new_game.curr_generation = grid
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        grid_txt = "\n".join(["".join(map(str, col)) for col in self.curr_generation])

        with filename.open(mode="w") as file:
            file.write(grid_txt)
