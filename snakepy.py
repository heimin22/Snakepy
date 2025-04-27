# putangina ng thesis na yan ang tagal nila gumawa ng data
# shout out sayo calvin, gumawa ka na pls sa thesis natin
# good luck sa probinsiyana mo adrian
# love na love ko asawa ko.

import random
import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dis_width = 1200
dis_height = 1000

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

# helper function to check if point q lies on segment pr
def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

# helper function to find orientation of ordered triplet (p, q, r)
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or Counterclockwise

# helper function to check if line segment 'p1q1' and 'p2q2' intersect.
def do_intersect(p1, q1, p2, q2):
    # find the four orientations needed for general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # general case
    if o1 != o2 and o3 != o4:
        return True

    # special cases
    # p1, q1 and p2 are collinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(p1, p2, q1): return True
    # p1, q1 and q2 are collinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1): return True
    # p2, q2 and p1 are collinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(p2, p1, q2): return True
    # p2, q2 and q1 are collinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False # Doesn't intersect

def generate_random_shape_points(sides, margin=15, min_segment_length=50):
    max_retries_per_point = 50 # Avoid infinite loops

    while True: # keep trying until a valid shape is generated
        points = []
        min_x = margin
        max_x = dis_width - margin
        min_y = margin
        max_y = dis_height - margin

        # start point somewhere near the center-ish top
        start_x = random.randint(min_x + (max_x-min_x)//4, max_x - (max_x-min_x)//4)
        start_y = random.randint(min_y, min_y + (max_y-min_y)//4)
        points.append((start_x, start_y))

        current_x, current_y = start_x, start_y
        last_direction = "horizontal" # assume starting horizontal virtual segment
        remaining_sides = sides

        shape_possible = True
        while remaining_sides > 1: # generate sides-1 points
            retries = 0
            point_added = False
            while retries < max_retries_per_point:
                if last_direction == "horizontal":
                    # try to move vertically
                    new_y = random.randint(min_y, max_y)
                    # ensure minimum segment length
                    if abs(new_y - current_y) < min_segment_length:
                        retries += 1
                        continue
                    new_x = current_x
                    proposed_direction = "vertical"
                else: # last_direction == "vertical"
                    # try to move horizontally
                    new_x = random.randint(min_x, max_x)
                    # ensure minimum segment length
                    if abs(new_x - current_x) < min_segment_length:
                        retries += 1
                        continue
                    new_y = current_y
                    proposed_direction = "horizontal"

                new_point = (new_x, new_y)
                last_point = points[-1]

                # check for intersections with non-adjacent segments
                intersects = False
                if len(points) > 1: # need at least 2 existing segments to check intersection
                    # check against segments 0 to n-3 (non-adjacent)
                    for i in range(len(points) - 2):
                        if do_intersect(last_point, new_point, points[i], points[i+1]):
                            intersects = True
                            break

                if not intersects:
                    points.append(new_point)
                    current_x, current_y = new_x, new_y
                    last_direction = proposed_direction
                    point_added = True
                    break # point added successfully
                else:
                    retries += 1

            if not point_added:
                shape_possible = False
                break # failed to add a point after retries, restart shape generation
            
            remaining_sides -= 1

        if not shape_possible:
            continue # Restart the whole shape generation

        # Try to close the shape
        # Add the second to last point (corner before closing)
        closing_point1 = None
        if last_direction == "horizontal":
            closing_point1 = (current_x, points[0][1])
        else: # vertical
            closing_point1 = (points[0][0], current_y)

        # check intersection for the segment before the final closing segment
        intersects1 = False
        if len(points) > 0:
            last_point = points[-1]
            # check against segments 0 to n-3
            for i in range(len(points) - 2):
                 if do_intersect(last_point, closing_point1, points[i], points[i+1]):
                    intersects1 = True
                    break

        # check intersection for the final closing segment (closing_point1 to points[0])
        intersects2 = False
        # check against segments 1 to n-2 (can't intersect with 0 or n-1)
        for i in range(1, len(points) - 1):
            if do_intersect(closing_point1, points[0], points[i], points[i+1]):
                intersects2 = True
                break

        if not intersects1 and not intersects2 and abs(closing_point1[0]-points[0][0]) + abs(closing_point1[1]-points[0][1]) > 0: # ensure closing point is not the start point
             # check min length for the two closing segments
            if abs(closing_point1[0] - points[-1][0]) + abs(closing_point1[1] - points[-1][1]) >= min_segment_length and \
               abs(points[0][0] - closing_point1[0]) + abs(points[0][1] - closing_point1[1]) >= min_segment_length:
                points.append(closing_point1)

                # center the polygon
                min_poly_x = min(p[0] for p in points)
                max_poly_x = max(p[0] for p in points)
                min_poly_y = min(p[1] for p in points)
                max_poly_y = max(p[1] for p in points)

                poly_center_x = (min_poly_x + max_poly_x) / 2
                poly_center_y = (min_poly_y + max_poly_y) / 2

                display_center_x = dis_width / 2
                display_center_y = dis_height / 2

                translate_x = display_center_x - poly_center_x
                translate_y = display_center_y - poly_center_y

                translated_points = [(p[0] + translate_x, p[1] + translate_y) for p in points]

                # shape successfully generated and centered
                return translated_points
        
        # if closing failed or intersected, loop again to generate a new shape

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
    # increase buffer to prevent spawning too close to edges
    buffer = snake_block * 5 
    min_x = int(min(p[0] for p in shape_points) + buffer)
    max_x = int(max(p[0] for p in shape_points) - buffer)
    min_y = int(min(p[1] for p in shape_points) + buffer)
    max_y = int(max(p[1] for p in shape_points) - buffer)
    
    attempts = 0
    while attempts < 100:
        fx = round(random.randint(min_x, max_x) / 10.0) * 10.0
        fy = round(random.randint(min_y, max_y) / 10.0) * 10.0
        
        if is_point_in_polygon(fx, fy, shape_points):
            return fx, fy
        attempts += 1
    
    # fallback to center if no valid position found
    center_x = sum(p[0] for p in shape_points) / len(shape_points)
    center_y = sum(p[1] for p in shape_points) / len(shape_points)
    return round(center_x / 10.0) * 10.0, round(center_y / 10.0) * 10.0

# function to display score
def show_score(score):
    value = small_font.render("Score: " + str(score), True, white)
    dis.blit(value, [10, 10]) # display at top-left corner

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
    score = 0 # Initialize score

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

        # check if any corner of the next head position is outside the shape
        corner_top_left = (next_x, next_y)
        corner_top_right = (next_x + snake_block - 1, next_y)
        corner_bottom_left = (next_x, next_y + snake_block - 1)
        corner_bottom_right = (next_x + snake_block - 1, next_y + snake_block - 1)

        if not is_point_in_polygon(corner_top_left[0], corner_top_left[1], shape_points) or \
           not is_point_in_polygon(corner_top_right[0], corner_top_right[1], shape_points) or \
           not is_point_in_polygon(corner_bottom_left[0], corner_bottom_left[1], shape_points) or \
           not is_point_in_polygon(corner_bottom_right[0], corner_bottom_right[1], shape_points):
            game_close = True

        x1 = next_x
        y1 = next_y
        dis.fill(blue)

        # draw the shape with thicker border
        pygame.draw.polygon(dis, white, shape_points, 8)  # increased thickness to 8

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
        show_score(score) # Display score
        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx, foody = spawn_food(shape_points)
            Length_of_snake += 1
            score += 1 # Increment score

        clock.tick(snake_speed)


if __name__ == "__main__":
    gameLoop()




