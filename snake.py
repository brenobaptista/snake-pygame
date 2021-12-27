#!/usr/bin/env python
import pygame as pg
from pygame.locals import *
import random

TITLE = 'Snake'
FRAMES_PER_SECOND = 15
RESOLUTION = (600, 600)
SQUARE_SIDE = 15
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
START_SNAKE_DIRECTION = RIGHT
START_SNAKE_HEAD_POSITION = (300, 300)
START_SNAKE_LENGTH = 3
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (40, 40, 40)
SNAKE_COLOR = (255, 255, 255)
APPLE_COLOR = (255, 0, 0)

if RESOLUTION[0] % SQUARE_SIDE != 0 or RESOLUTION[1] % SQUARE_SIDE != 0:
    raise Exception("Resolution should be a multiple of the square side")

if START_SNAKE_HEAD_POSITION[0] % SQUARE_SIDE != 0 or START_SNAKE_HEAD_POSITION[1] % SQUARE_SIDE != 0:
    raise Exception("Snake position should be a multiple of the square side")


def generate_start_snake_position():
    start_snake_position = [(0, 0)] * START_SNAKE_LENGTH

    if START_SNAKE_DIRECTION == UP:
        for i in range(0, START_SNAKE_LENGTH - 1, 1):
            start_snake_position[i] = (START_SNAKE_HEAD_POSITION[0],
                                       START_SNAKE_HEAD_POSITION[1] + SQUARE_SIDE * i)
    elif START_SNAKE_DIRECTION == RIGHT:
        for i in range(0, START_SNAKE_LENGTH - 1, 1):
            start_snake_position[i] = (START_SNAKE_HEAD_POSITION[0] - SQUARE_SIDE * i,
                                       START_SNAKE_HEAD_POSITION[1])
    elif START_SNAKE_DIRECTION == DOWN:
        for i in range(0, START_SNAKE_LENGTH - 1, 1):
            start_snake_position[i] = (START_SNAKE_HEAD_POSITION[0],
                                       START_SNAKE_HEAD_POSITION[1] - SQUARE_SIDE * i)
    elif START_SNAKE_DIRECTION == LEFT:
        for i in range(0, START_SNAKE_LENGTH - 1, 1):
            start_snake_position[i] = (START_SNAKE_HEAD_POSITION[0] + SQUARE_SIDE * i,
                                       START_SNAKE_HEAD_POSITION[1])

    return start_snake_position


def generate_apple_position():
    return (random.randint(0, RESOLUTION[0]//SQUARE_SIDE - 1) * SQUARE_SIDE, random.randint(0, RESOLUTION[1]//SQUARE_SIDE - 1) * SQUARE_SIDE)


def detect_bite(snake_head, apple_position):
    return (snake_head[0] == apple_position[0]) and (snake_head[1] == apple_position[1])


def increase_snake_length(snake_position):
    snake_position.append((0, 0))


def move_snake_body_except_head(snake_position):
    for i in range(len(snake_position) - 1, 0, -1):
        snake_position[i] = (snake_position[i-1][0],
                             snake_position[i-1][1])


def move_snake_head(snake_position, snake_direction):
    if snake_direction == UP:
        snake_position[0] = (snake_position[0][0],
                             snake_position[0][1] - SQUARE_SIDE)
    elif snake_direction == RIGHT:
        snake_position[0] = (snake_position[0][0] +
                             SQUARE_SIDE, snake_position[0][1])
    elif snake_direction == DOWN:
        snake_position[0] = (snake_position[0][0],
                             snake_position[0][1] + SQUARE_SIDE)
    elif snake_direction == LEFT:
        snake_position[0] = (snake_position[0][0] -
                             SQUARE_SIDE, snake_position[0][1])


def render(screen, snake_position, apple_position):
    screen.fill(BACKGROUND_COLOR)
    for x in range(0, RESOLUTION[0], SQUARE_SIDE):
        pg.draw.line(screen, LINE_COLOR, (x, 0), (x, RESOLUTION[0]))
    for y in range(0, RESOLUTION[1], SQUARE_SIDE):
        pg.draw.line(screen, LINE_COLOR, (0, y), (RESOLUTION[1], y))

    snake_skin = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
    snake_skin.fill(SNAKE_COLOR)
    for position in snake_position:
        screen.blit(snake_skin, position)

    apple_peel = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
    apple_peel.fill(APPLE_COLOR)
    screen.blit(apple_peel, apple_position)

    pg.display.update()


def main():
    pg.init()
    screen = pg.display.set_mode(RESOLUTION)
    pg.display.set_caption(TITLE)

    clock = pg.time.Clock()

    snake_position = generate_start_snake_position()
    snake_direction = START_SNAKE_DIRECTION
    apple_position = generate_apple_position()

    while True:
        clock.tick(FRAMES_PER_SECOND)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

            if event.type == KEYDOWN:
                if event.key == K_UP and snake_direction != DOWN:
                    snake_direction = UP
                elif event.key == K_RIGHT and snake_direction != LEFT:
                    snake_direction = RIGHT
                elif event.key == K_DOWN and snake_direction != UP:
                    snake_direction = DOWN
                elif event.key == K_LEFT and snake_direction != RIGHT:
                    snake_direction = LEFT

        if detect_bite(snake_position[0], apple_position):
            apple_position = generate_apple_position()
            increase_snake_length(snake_position)

        move_snake_body_except_head(snake_position)

        move_snake_head(snake_position, snake_direction)

        render(screen, snake_position, apple_position)


if __name__ == "__main__":
    main()
