#!/usr/bin/env python
import pygame as pg
from pygame.locals import *
import random
import time
import sys
import os

TITLE = 'Snake'
FRAMES_PER_SECOND = 15
RESOLUTION = (720, 480)
SQUARE_SIDE = 20
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
START_SNAKE_DIRECTION = RIGHT
START_SNAKE_HEAD_POSITION = (120, 240)
START_SNAKE_LENGTH = 3
BACKGROUND_COLOR = (40, 42, 54)
GRID_COLOR = (68, 71, 90)
SNAKE_COLOR = (80, 250, 123)
APPLE_COLOR = (255, 85, 85)
SCORE_COLOR = (248, 248, 242)
SCORE_SIZE = 18
SCORE_PADDING = (4, 1)
SCORE_INCREMENT = 10
GAME_OVER_COLOR = (248, 248, 242)
GAME_OVER_SIZE = 36
FONT_ANTIALIAS = True

if RESOLUTION[0] % SQUARE_SIDE != 0 or RESOLUTION[1] % SQUARE_SIDE != 0:
    raise Exception('Resolution should be a multiple of the square side')

if START_SNAKE_HEAD_POSITION[0] % SQUARE_SIDE != 0 or START_SNAKE_HEAD_POSITION[1] % SQUARE_SIDE != 0:
    raise Exception('Snake position should be a multiple of the square side')


main_dir = os.path.split(os.path.abspath(__file__))[0]


def play_sound(file):
    sound_path = os.path.join(main_dir, 'data', file)
    sound = pg.mixer.Sound(sound_path)
    sound.play()


def generate_random_position():
    return (random.randint(0, RESOLUTION[0]//SQUARE_SIDE - 1) * SQUARE_SIDE,
            random.randint(0, RESOLUTION[1]//SQUARE_SIDE - 1) * SQUARE_SIDE)


class Gameplay():
    def __init__(self):
        self.screen = pg.display.set_mode(RESOLUTION)
        self.clock = pg.time.Clock()
        self.score = 0

    def run(self, snake, apple):
        pg.init()
        pg.display.set_caption(TITLE)
        pg.mouse.set_visible(0)
        self.__set_icon()

        self.__play_music()

        while True:
            self.__limit_frames_per_second()
            self.__handle_input(snake)

            snake.move()

            if snake.detect_bite_itself() or snake.detect_border_collision():
                break

            self.__handle_bite(snake, apple)

            self.__render(snake, apple)

        self.__end_game()

    def __set_icon(self):
        icon_path = os.path.join(main_dir, 'data', 'icon.png')
        icon = pg.image.load(icon_path)
        icon_resized = pg.transform.scale(icon, (32, 32))
        pg.display.set_icon(icon_resized)

    def __play_music(self):
        music_path = os.path.join(main_dir, 'data', 'birds-music.mp3')
        pg.mixer.music.load(music_path)
        pg.mixer.music.play(-1)

    def __limit_frames_per_second(self):
        self.clock.tick(FRAMES_PER_SECOND)

    def __handle_input(self, snake):
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN:
                snake.change_direction(event.key)

    def __handle_bite(self, snake, apple):
        if self.__detect_bite(snake.position[0], apple.position):
            self.__spawn_new_apple(snake.position, apple)
            self.score += SCORE_INCREMENT
            snake.increase_length()
            play_sound('bite-sound.mp3')

    def __detect_bite(self, snake_head_position, apple_position):
        return snake_head_position[0] == apple_position[0] and snake_head_position[1] == apple_position[1]

    def __spawn_new_apple(self, snake_position, apple):
        while True:
            new_apple_position = generate_random_position()
            apple_detection_area = pg.Rect(
                new_apple_position[0], new_apple_position[1], SQUARE_SIDE, SQUARE_SIDE)

            if not any(apple_detection_area.collidepoint(*position) for position in snake_position):
                break

        apple.position = new_apple_position

    def __render_grid(self):
        for x in range(0, RESOLUTION[0], SQUARE_SIDE):
            pg.draw.line(self.screen, GRID_COLOR, (x, 0), (x, RESOLUTION[1]))
        for y in range(0, RESOLUTION[1], SQUARE_SIDE):
            pg.draw.line(self.screen, GRID_COLOR, (0, y), (RESOLUTION[0], y))

    def __render_score(self):
        score_font = pg.font.SysFont('monospace', SCORE_SIZE)

        score_surface = score_font.render(
            'Score: %s' % (self.score), FONT_ANTIALIAS, SCORE_COLOR)

        score_rect = score_surface.get_rect()

        score_rect.topleft = SCORE_PADDING

        self.screen.blit(score_surface, score_rect)

    def __render(self, snake, apple):
        self.screen.fill(BACKGROUND_COLOR)

        self.__render_grid()

        self.__render_score()

        for position in snake.position:
            self.screen.blit(snake.skin, position)

        self.screen.blit(apple.peel, apple.position)

        pg.display.update()

    def __render_game_over(self):
        game_over_font = pg.font.SysFont('monospace', GAME_OVER_SIZE)
        game_over_surface = game_over_font.render(
            'Game Over', FONT_ANTIALIAS, GAME_OVER_COLOR)

        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (RESOLUTION[0]/2, RESOLUTION[1]/4)

        self.screen.blit(game_over_surface, game_over_rect)
        pg.display.flip()

    def __end_game(self):
        self.__render_game_over()
        time.sleep(2)

        pg.quit()
        sys.exit()


class Snake():
    def __init__(self):
        self.skin = pg.Surface((SQUARE_SIDE, SQUARE_SIDE))
        self.skin.fill(SNAKE_COLOR)
        self.direction = START_SNAKE_DIRECTION
        self.change_direction_to = START_SNAKE_DIRECTION
        self.position = self.__generate_start_position()

    def __generate_start_position(self):
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
        snake_tail_position = self.position[len(self.position) - 1]
        self.position.append((snake_tail_position[0], snake_tail_position[1]))

    def detect_border_collision(self):
        if self.position[0][0] >= RESOLUTION[0] or self.position[0][1] >= RESOLUTION[1] or self.position[0][0] < 0 or self.position[0][1] < 0:
            play_sound('crash-sound.mp3')
            return True

    def detect_bite_itself(self):
        if self.position[0] in self.position[1:]:
            play_sound('bite-sound.mp3')
            return True


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


if __name__ == '__main__':
    main()
