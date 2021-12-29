#!/usr/bin/env python
import pygame as pg
from pygame.locals import *
import random
import sys

TITLE = 'Snake'
FRAMES_PER_SECOND = 15
RESOLUTION = (720, 480)
SQUARE_SIDE = 20
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
START_SNAKE_DIRECTION = RIGHT
START_SNAKE_HEAD_POSITION = (120, 240)
START_SNAKE_LENGTH = 3
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
SCORE_COLOR = (255, 255, 255)
SCORE_SIZE = 20
SCORE_PADDING = (4, 2)
END_GAME_COLOR = (255, 0, 0)
END_GAME_SIZE = 50
FONT_ANTIALIAS = True

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
        self.is_game_over = False
        self.score = 0

    def run(self, snake, apple):
        pg.init()
        pg.display.set_caption(TITLE)

        while not self.is_game_over:
            self.limit_frames_per_second()
            self.handle_input(snake)

            snake.move()
            self.detect_snake_collision(snake.position)
            self.detect_border_collision(snake.position[0])
            if self.is_game_over:
                break

            self.handle_bite(snake, apple)

            self.render(snake, apple)

        self.end_game()

    def limit_frames_per_second(self):
        self.clock.tick(FRAMES_PER_SECOND)

    def handle_input(self, snake):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN:
                snake.change_direction(event.key)

    def handle_bite(self, snake, apple):
        if self.detect_bite(snake.position[0], apple.position):
            self.spawn_new_apple(snake.position, apple)
            self.score += 10
            snake.increase_length()

    def detect_bite(self, snake_head_position, apple_position):
        return (snake_head_position[0] == apple_position[0]) and (snake_head_position[1] == apple_position[1])

    def spawn_new_apple(self, snake_position, apple):
        while True:
            new_apple_position = generate_random_position()
            apple_detection_area = pg.Rect(
                new_apple_position[0], new_apple_position[1], SQUARE_SIDE, SQUARE_SIDE)

            if not any(apple_detection_area.collidepoint(*position) for position in snake_position):
                break

        apple.position = new_apple_position

    def detect_border_collision(self, snake_head_position):
        if snake_head_position[0] >= RESOLUTION[0] or snake_head_position[1] >= RESOLUTION[1] or snake_head_position[0] < 0 or snake_head_position[1] < 0:
            self.is_game_over = True

    def detect_snake_collision(self, snake_position):
        if snake_position[0] in snake_position[1:]:
            self.is_game_over = True

    def render_grid(self):
        for x in range(0, RESOLUTION[0], SQUARE_SIDE):
            pg.draw.line(self.screen, GRID_COLOR,
                         (x, 0), (x, RESOLUTION[1]))

        for y in range(0, RESOLUTION[1], SQUARE_SIDE):
            pg.draw.line(self.screen, GRID_COLOR,
                         (0, y), (RESOLUTION[0], y))

    def render_score(self):
        score_font = pg.font.Font(pg.font.get_default_font(), SCORE_SIZE)

        score_surface = score_font.render(
            'Score: %s' % (self.score), FONT_ANTIALIAS, SCORE_COLOR)

        score_rect = score_surface.get_rect()

        score_rect.topleft = SCORE_PADDING

        self.screen.blit(score_surface, score_rect)

    def render(self, snake, apple):
        self.screen.fill(BACKGROUND_COLOR)

        self.render_grid()

        self.render_score()

        for position in snake.position:
            self.screen.blit(snake.skin, position)

        self.screen.blit(apple.peel, apple.position)

        pg.display.update()

    def end_game(self):
        end_game_font = pg.font.Font(pg.font.get_default_font(), END_GAME_SIZE)

        end_game_surface = end_game_font.render(
            'Game Over', FONT_ANTIALIAS, END_GAME_COLOR)

        end_game_rect = end_game_surface.get_rect()

        end_game_rect.midtop = (RESOLUTION[0]/2, RESOLUTION[1]/4)

        self.screen.blit(end_game_surface, end_game_rect)
        pg.display.flip()

        time.sleep(2)

        pg.quit()
        sys.exit()


class Snake():
    def __init__(self):
        self.skin = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
        self.skin.fill(SNAKE_COLOR)
        self.direction = START_SNAKE_DIRECTION
        self.change_direction_to = START_SNAKE_DIRECTION
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
            self.change_direction_to = UP
        elif event_key == K_RIGHT and self.direction != LEFT:
            self.change_direction_to = RIGHT
        elif event_key == K_DOWN and self.direction != UP:
            self.change_direction_to = DOWN
        elif event_key == K_LEFT and self.direction != RIGHT:
            self.change_direction_to = LEFT

    def move(self):
        self.position.pop()

        if self.change_direction_to == UP:
            self.direction = UP
            self.position.insert(
                0, (self.position[0][0], self.position[0][1] - SQUARE_SIDE))
        elif self.change_direction_to == RIGHT:
            self.direction = RIGHT
            self.position.insert(
                0, (self.position[0][0] + SQUARE_SIDE, self.position[0][1]))
        elif self.change_direction_to == DOWN:
            self.direction = DOWN
            self.position.insert(
                0, (self.position[0][0], self.position[0][1] + SQUARE_SIDE))
        elif self.change_direction_to == LEFT:
            self.direction = LEFT
            self.position.insert(
                0, (self.position[0][0] - SQUARE_SIDE, self.position[0][1]))

    def increase_length(self):
        snake_tail = self.position[len(self.position) - 1]
        self.position.append((snake_tail[0], snake_tail[1]))


class Apple():
    def __init__(self):
        self.peel = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
        self.peel.fill(APPLE_COLOR)
        self.position = generate_random_position()


def main():
    gameplay = Gameplay()
    snake = Snake()
    apple = Apple()

    gameplay.run(snake, apple)


if __name__ == "__main__":
    main()
