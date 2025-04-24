import os
import random
import time
import msvcrt

# controls are
# w = up, s = down, a = left, d = right, q = quit

WIDTH = 40
HEIGHT = 20

# directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = RIGHT
        self.spawn_food()
        self.score = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            self.food = (
                random.randint(1, self.width - 2),
                random.randint(1, self.height - 2),
            )
            if self.food not in self.snake:
                break
