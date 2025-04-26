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

def is_point_in_polygon(x, y, sides, radius):
    center_x = dis_width / 2
    center_y = dis_height / 2
    angle = math.atan2(y - center_y, x - center_x)
    r = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    theta = 2 * math.pi / sides
    R = radius / math.cos(math.pi / sides)
    r_max = R / math.cos(angle % theta - theta / 2)
    return r <= r_max

def get_sides():
    pygame.event.clear()
    sides = 3
    while True:
        dis.fill(blue)
        message("Enter the number of sides (3-8): ", white)
        message("Press number (3-8)", white, 50, "small")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if pygame.K_3 <= event.key <= pygame.K_8:
                    sides = event.key - pygame.K_0
                    if 3 <= sides <= 8:
                        return sides
                elif pygame.K_KP3 <= event.key <= pygame.K_KP8:
                    sides = event.key - pygame.K_KP0
                    if 3 <= sides <= 8:
                        return sides

        clock.tick(30)

def gameLoop():
    try:
        sides = get_sides()
        if sides < 3:
            sides = 3
    except pygame.error:
        pygame.quit()
        quit()

    radius = min(dis_width, dis_height) * 0.4

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    while True:
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        if not is_point_in_polygon(foodx, foody, sides, radius):
            break

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
                game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    return gameLoop()
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        next_x = x1 + x1_change
        next_y = y1 + y1_change
        if not is_point_in_polygon(next_x, next_y, sides, radius):
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = dis_width / 2 + radius * math.cos(angle)
            y = dis_height / 2 + radius * math.sin(angle)
            points.append((int(x), int(y)))

        if len(points) >= 3:
            pygame.draw.polygon(dis, white, points, 2)

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

        if x1 == foodx and y1 == foody:
            while True:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                if is_point_in_polygon(foodx, foody, sides, radius):
                    break
            Length_of_snake += 1

        clock.tick(snake_speed)
    

if __name__ == "__main__":
    gameLoop()




