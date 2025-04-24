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
        self.message = ""

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
        else:
            self.message = "Cannot move in opposite direction"

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
        print("#" * self.width)
        print(f"Score: {self.score}")
        if self.message:
            print(f"message: {self.message}")
            self.message = ""
        print("controls: W=Up, S=Down, A=Left, D=Right, Q=Quit, P=Pause")

    def run(self):
        paused = False
        while not self.game_over:
            # handle input
            if msvcrt.kbhit():
                try:
                    key = msvcrt.getch().decode("utf-8").lower()
                except UnicodeDecodeError:
                    self.message = "Invalid key pressed!"
                    key = None

                if key == "w":
                    self.change_direction(UP)
                elif key == "s":
                    self.change_direction(DOWN)
                elif key == "a":
                    self.change_direction(LEFT)
                elif key == "d":
                    self.change_direction(RIGHT)
                elif key == "q":
                    self.game_over = True
                    break
                elif key == "p":
                    paused = not paused
                    self.message = (
                        "Game paused. Press P again to resume."
                        if paused
                        else "Game resumed!"
                    )
                else:
                    if key:
                        self.message = f"Invalid key: '{key}'. Use W,A,S,D to move, P to pause, Q to quit."

            if not paused:
                self.step()

            self.draw()

            # Control speed (slower when score is low)
            time.sleep(max(0.05, 0.2 - self.score * 0.005))

        # After loop exits
        clear_screen()
        print("Game Over! Final Score:", self.score)
        msvcrt.getch()


if __name__ == "__main__":
    try:
        game = SnakeGame(WIDTH, HEIGHT)
        game.run()
    except Exception as e:
        clear_screen()
        print(f"An unexpected error occured. {e}")
        msvcrt.getch()
