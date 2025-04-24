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

    def change_direction(self, new_dir):
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.direction = new_dir

    def step(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # collisions
        if (
            new_head[0] <= 0
            or new_head[0] >= self.width - 1
            or new_head[1] <= 0
            or new_head[1] >= self.height - 1
            or new_head in self.snake
        ):
            self.game_over = True
            return

        # move snake
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        clear_screen()
        # top border
        print("#" * self.width)
        for y in range(1, self.height - 1):
            row = ""
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    row += "O"
                elif (x, y) in self.snake:
                    row += "o"
                elif (x, y) == self.food:
                    row += "*"
                elif x == 0 or x == self.width - 1:
                    row += "#"
                else:
                    row += " "
            print(row)
