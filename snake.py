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
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

if RESOLUTION[0] % SQUARE_SIDE != 0 or RESOLUTION[1] % SQUARE_SIDE != 0:
    raise Exception("Resolution should be a multiple of the square side")

if START_SNAKE_HEAD_POSITION[0] % SQUARE_SIDE != 0 or START_SNAKE_HEAD_POSITION[1] % SQUARE_SIDE != 0:
    raise Exception("Snake position should be a multiple of the square side")


class Snake():
    def __init__(self):
        self.skin = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
        self.skin.fill(SNAKE_COLOR)
        self.direction = START_SNAKE_DIRECTION
        self.position = self.generate_start_position()

    def generate_start_position(self):
        start_position = [(0, 0)] * START_SNAKE_LENGTH

        if START_SNAKE_DIRECTION == UP:
            for i in range(0, START_SNAKE_LENGTH - 1, 1):
                start_position[i] = (START_SNAKE_HEAD_POSITION[0],
                                     START_SNAKE_HEAD_POSITION[1] + SQUARE_SIDE * i)
        elif START_SNAKE_DIRECTION == RIGHT:
            for i in range(0, START_SNAKE_LENGTH - 1, 1):
                start_position[i] = (START_SNAKE_HEAD_POSITION[0] - SQUARE_SIDE * i,
                                     START_SNAKE_HEAD_POSITION[1])
        elif START_SNAKE_DIRECTION == DOWN:
            for i in range(0, START_SNAKE_LENGTH - 1, 1):
                start_position[i] = (START_SNAKE_HEAD_POSITION[0],
                                     START_SNAKE_HEAD_POSITION[1] - SQUARE_SIDE * i)
        elif START_SNAKE_DIRECTION == LEFT:
            for i in range(0, START_SNAKE_LENGTH - 1, 1):
                start_position[i] = (START_SNAKE_HEAD_POSITION[0] + SQUARE_SIDE * i,
                                     START_SNAKE_HEAD_POSITION[1])

        return start_position

    def move_body_except_head(self):
        for i in range(len(self.position) - 1, 0, -1):
            self.position[i] = (self.position[i-1][0],
                                self.position[i-1][1])

    def move_head(self):
        if self.direction == UP:
            self.position[0] = (self.position[0][0],
                                self.position[0][1] - SQUARE_SIDE)
        elif self.direction == RIGHT:
            self.position[0] = (self.position[0][0] +
                                SQUARE_SIDE, self.position[0][1])
        elif self.direction == DOWN:
            self.position[0] = (self.position[0][0],
                                self.position[0][1] + SQUARE_SIDE)
        elif self.direction == LEFT:
            self.position[0] = (self.position[0][0] -
                                SQUARE_SIDE, self.position[0][1])

    def move(self):
        self.move_body_except_head()
        self.move_head()

    def increase_length(self):
        self.position.append((0, 0))


class Apple():
    def __init__(self):
        self.peel = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
        self.peel.fill(APPLE_COLOR)
        self.position = self.generate_random_position()

    def generate_random_position(self):
        return (random.randint(0, RESOLUTION[0]//SQUARE_SIDE - 1) * SQUARE_SIDE, random.randint(0, RESOLUTION[1]//SQUARE_SIDE - 1) * SQUARE_SIDE)

    def spawn_new_apple(self):
        self.position = self.generate_random_position()


def detect_bite(snake_head_position, apple_position):
    return (snake_head_position[0] == apple_position[0]) and (snake_head_position[1] == apple_position[1])


def render(screen, snake, apple):
    screen.fill(BACKGROUND_COLOR)
    for x in range(0, RESOLUTION[0], SQUARE_SIDE):
        pg.draw.line(screen, LINE_COLOR, (x, 0), (x, RESOLUTION[0]))
    for y in range(0, RESOLUTION[1], SQUARE_SIDE):
        pg.draw.line(screen, LINE_COLOR, (0, y), (RESOLUTION[1], y))

    for position in snake.position:
        screen.blit(snake.skin, position)

    screen.blit(apple.peel, apple.position)

    pg.display.update()


def main():
    pg.init()
    screen = pg.display.set_mode(RESOLUTION)
    pg.display.set_caption(TITLE)

    clock = pg.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(FRAMES_PER_SECOND)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

            if event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT

        if detect_bite(snake.position[0], apple.position):
            apple.spawn_new_apple()
            snake.increase_length()

        snake.move()

        render(screen, snake, apple)


if __name__ == "__main__":
    main()
