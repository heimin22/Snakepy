import os
import random
import time
import msvcrt
import pygame
import math

# controls are
# w = up, s = down, a = left, d = right, q = quit

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
    input_received = False
    sides = 4

    while not input_received:
        dis.fill(blue)
        message("Enter the number of sides (3-8): ", white) 
        message("Press number (3-8)", white, 50, "small")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode in "34567":
                    sides = int(event.unicode)
                    input_received = True
                elif event.key == pygame.K_8:
                    sides = 8
                    input_received = True
            elif event.key == pygame.QUIT:
                pygame.quit()
                quit()

    return sides

def gameLoop():
    sides = get_sides()
    radius = min(dis_width, dis_height) * 0.4

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
