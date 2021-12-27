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


def generate_random_position():
    return (random.randint(0, RESOLUTION[0]//SQUARE_SIDE - 1) * SQUARE_SIDE, random.randint(0, RESOLUTION[1]//SQUARE_SIDE - 1) * SQUARE_SIDE)


class Gameplay():
    def __init__(self):
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()

    def setup(self, snake, apple):
        pg.init()
        pg.display.set_caption(TITLE)

        while True:
            self.limit_frames_per_second()
            self.handle_input(snake)
            self.handle_swallow(snake, apple)
            snake.move()
            self.render(snake, apple)

    def limit_frames_per_second(self):
        self.clock.tick(FRAMES_PER_SECOND)

    def handle_input(self, snake):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()

            if event.type == KEYDOWN:
                snake.change_direction(event.key)

    def handle_swallow(self, snake, apple):
        if self.detect_swallow(snake.position[0], apple.position):
            self.spawn_new_apple(snake.position, apple)
            snake.increase_length()

    def detect_swallow(self, snake_head_position, apple_position):
        return (snake_head_position[0] == apple_position[0]) and (snake_head_position[1] == apple_position[1])

    def spawn_new_apple(self, snake_position, apple):
        while True:
            new_apple_position = generate_random_position()
            apple_detection_area = pg.Rect(
                new_apple_position[0], new_apple_position[1], SQUARE_SIDE, SQUARE_SIDE)

            if not any(apple_detection_area.collidepoint(*position) for position in snake_position):
                break

        apple.position = new_apple_position

    def render(self, snake, apple):
        self.screen.fill(BACKGROUND_COLOR)

        for x in range(0, RESOLUTION[0], SQUARE_SIDE):
            pg.draw.line(self.screen, LINE_COLOR, (x, 0), (x, RESOLUTION[0]))
        for y in range(0, RESOLUTION[1], SQUARE_SIDE):
            pg.draw.line(self.screen, LINE_COLOR, (0, y), (RESOLUTION[1], y))

        for position in snake.position:
            self.screen.blit(snake.skin, position)

        self.screen.blit(apple.peel, apple.position)

        pg.display.update()


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

    def change_direction(self, event_key):
        if event_key == K_UP and self.direction != DOWN:
            self.direction = UP
        elif event_key == K_RIGHT and self.direction != LEFT:
            self.direction = RIGHT
        elif event_key == K_DOWN and self.direction != UP:
            self.direction = DOWN
        elif event_key == K_LEFT and self.direction != RIGHT:
            self.direction = LEFT

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
        self.position = generate_random_position()


def main():
    gameplay = Gameplay()
    snake = Snake()
    apple = Apple()

    gameplay.setup(snake, apple)


if __name__ == "__main__":
    main()
