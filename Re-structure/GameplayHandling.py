import pygame, random
from utilities import SIZE

class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple1.png").convert_alpha()
        self.x = SIZE * 3
        self.y = SIZE * 3
        # add rect to test
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(1,31)*SIZE # 1280 : 40 = 32
        self.y = random.randint(1,17)*SIZE # 720 : 40 = 18
        # add rect to test
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

class Snake:
    def __init__(self,parent_screen,length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/body.png").convert_alpha()
        # default length
        self.length = length
        # default position
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        # default direction
        self.direction = 'down'
        # flag for direction change
        self.direction_changed = False
        # default speed
        self.speed = 5
        # move counter
        self.move_counter = 0
        # add rect to test
        self.rect = self.block.get_rect(topleft=(self.x[0], self.y[0]))

    # draw the snake
    def draw(self):
        # print("def drawing snake")
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    # move the snake
    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= self.speed
        elif self.direction == 'right':
            self.x[0] += self.speed
        elif self.direction == 'up':
            self.y[0] -= self.speed
        elif self.direction == 'down':
            self.y[0] += self.speed

        self.rect = self.block.get_rect(topleft=(self.x[0], self.y[0]))
        self.move_counter += self.speed

    # change direction
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    # collision check
    def collision_check(self, other):
        return self.rect.colliderect(other.rect)

    # increase length
    def increase_length(self):
        for i in range(7):
            self.x.append(self.x[-1])
            self.y.append(self.y[-1])
            self.length += 1

class Score_and_Mode:
    def __init__(self, game):
        self.score = 0
        self.mode = "easy"
        self.mode_rects = {}
        self.game = game

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def increase_score(self):
        if self.mode == "easy":
            self.score += 1
        elif self.mode == "normal":
            self.score += 2
        elif self.mode == "hard":
            self.score += 3

    def reset_score(self):
        self.score = 0

    def reset_mode(self):
        self.mode = "easy"

    def reset(self):
        self.reset_score()
        self.reset_mode()