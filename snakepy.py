import os
import random
import time
import msvcrt
import pygame
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 35)


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace = 0, size = "normal"):
    if size == "normal":
        mesg = font_style.render(msg, True, color)
    else:
        mesg = small_font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def generate_random_shape_points(sides, margin=50):
    points = []
    # Define the boundaries with margin from window edges
    min_x = margin
    max_x = dis_width - margin
    min_y = margin
    max_y = dis_height - margin
    
    # Start with a point near the top-left
    current_x = random.randint(min_x, max_x // 2)
    current_y = random.randint(min_y, max_y // 2)
    points.append((current_x, current_y))
    
    remaining_sides = sides - 1
    last_direction = None  # Track last direction to ensure alternating horizontal/vertical lines
    
    while remaining_sides > 0:
        # Alternate between horizontal and vertical movements
        if last_direction in [None, "vertical"]:
            # Move horizontally
            new_x = random.randint(min_x, max_x)
            new_y = current_y
            last_direction = "horizontal"
        else:
            # Move vertically
            new_x = current_x
            new_y = random.randint(min_y, max_y)
            last_direction = "vertical"
        
        # Add the new point
        current_x, current_y = new_x, new_y
        points.append((current_x, current_y))
        remaining_sides -= 1
    
    # Connect back to the first point with appropriate straight lines
    if last_direction == "horizontal":
        # Add vertical line to get back to starting y
        points.append((current_x, points[0][1]))
    else:
        # Add horizontal line to get back to starting x
        points.append((points[0][0], current_y))
    
    return points

def is_point_in_polygon(x, y, points):
    n = len(points)
    inside = False
    
    j = n - 1
    for i in range(n):
        if ((points[i][1] > y) != (points[j][1] > y) and
            x < (points[j][0] - points[i][0]) * (y - points[i][1]) /
            (points[j][1] - points[i][1]) + points[i][0]):
            inside = not inside
        j = i
    
    return inside

def get_sides():
    current_input = ""

    while True:
        dis.fill(blue)
        message("Enter the number of sides (3-8): ", white)
        message(current_input, white, 50, "small")
        message("Press Enter to confirm", white, 100, "small")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    try:
                        sides = int(current_input)
                        if 3 <= sides <= 8:
                            return sides
                    except ValueError:
                        current_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.unicode.isdigit():
                    if len(current_input) < 1:
                        current_input += event.unicode

        clock.tick(30)

def spawn_food(shape_points):
    # Find boundaries of the shape
    min_x = min(p[0] for p in shape_points)
    max_x = max(p[0] for p in shape_points)
    min_y = min(p[1] for p in shape_points)
    max_y = max(p[1] for p in shape_points)
    
    attempts = 0
    while attempts < 100:
        # Generate food position aligned with snake grid
        fx = round(random.randint(min_x + 10, max_x - 10) / 10.0) * 10.0
        fy = round(random.randint(min_y + 10, max_y - 10) / 10.0) * 10.0
        
        if is_point_in_polygon(fx, fy, shape_points):
            return fx, fy
        attempts += 1
    
    # Fallback to center if no valid position found
    return dis_width/2, dis_height/2

def gameLoop():
    try:
        sides = get_sides()
        if sides < 3:
            sides = 3
    except pygame.error:
        pygame.quit()
        quit()

    # Generate shape points
    shape_points = generate_random_shape_points(sides)
    
    game_over = False
    game_close = False

    # Start snake in the middle of the shape
    x1 = sum(p[0] for p in shape_points) / len(shape_points)
    y1 = sum(p[1] for p in shape_points) / len(shape_points)
    x1 = round(x1 / 10.0) * 10.0  # Align to grid
    y1 = round(y1 / 10.0) * 10.0  # Align to grid

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx, foody = spawn_food(shape_points)

    while not game_over:
        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0


        next_x = x1 + x1_change
        next_y = y1 + y1_change

        # Check if next position is inside the shape
        if not is_point_in_polygon(next_x, next_y, shape_points):
            game_close = True

        x1 = next_x
        y1 = next_y
        dis.fill(blue)

        # Draw the shape with thicker border
        pygame.draw.polygon(dis, white, shape_points, 8)  # Increased thickness to 8

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx, foody = spawn_food(shape_points)
            Length_of_snake += 1

        clock.tick(snake_speed)


if __name__ == "__main__":
    gameLoop()




