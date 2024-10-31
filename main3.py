import pygame
import sys
import random
from button import Button
from abc import ABC, abstractmethod

# Initialize pygame
pygame.init()

def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/font.ttf", size)

class Screen(ABC):
    def __init__(self,game):
        self.game = game
        pygame.display.set_caption("Snake Game")
        self.SCREEN = pygame.display.set_mode((1280, 720))

    @abstractmethod
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

########## MAIN MENU ##########
class MainMenu(Screen):
    def __init__(self,game):
        super().__init__(game)
        # title
        self.MENU_TEXT = get_font(100).render("SNAKE GAME", True, "#b68f40")
        self.MENU_RECT = self.MENU_TEXT.get_rect(center=(640, 100))
        # get mouse position
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        # background
        self.BG = pygame.image.load("resources/Background.png")
        
        # CREATE BUTTONS
        self.PLAY_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")
        self.QUIT_BUTTON = Button(image=pygame.image.load("resources/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.game.set_screen(self.game.screen_play)
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.game.running = False 

    def update(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.PLAY_BUTTON.changeColor(self.MENU_MOUSE_POS)
        self.QUIT_BUTTON.changeColor(self.MENU_MOUSE_POS)
        self.PLAY_BUTTON.update(self.SCREEN)
        self.QUIT_BUTTON.update(self.SCREEN)

    def draw(self):
        # background
        self.SCREEN.blit(self.BG, (0, 0))
        # title
        self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)
        # buttons
        # self.display_test()


####### checkForInput ########
def checkForInput(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
        return True
    return False

########## PLAY SCREEN ##########
class PlayScreen(Screen):
    def __init__(self,game):
        super().__init__(game)
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        self.BG = pygame.image.load("resources/background.jpg")
        # food
        self.food = Food(self.SCREEN)
        # snake
        self.snake = Snake(self.SCREEN, 7)

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            #######
            # test click food
            if event.type == pygame.MOUSEBUTTONDOWN:
                if checkForInput(self.food, self.PLAY_MOUSE_POS):
                    # self.food.move()
                    # self.game.running = False
                    print("clicked")
            #######

            # check for key presses BASE
            '''
            if event.type == pygame.KEYDOWN:
                # press esc
                if event.key == pygame.K_ESCAPE:
                    self.game.set_screen(self.game.screen_menu)
                # press left arrow
                if event.key == pygame.K_LEFT:
                    self.snake.move_left()
                # press right arrow
                if event.key == pygame.K_RIGHT:
                    self.snake.move_right()
                # press up arrow
                if event.key == pygame.K_UP:
                    self.snake.move_up()
                # press down arrow
                if event.key == pygame.K_DOWN:
                    self.snake.move_down()
            ''' 
            # check for key presses TEST
            if event.type == pygame.KEYDOWN:
                # press esc
                if event.key == pygame.K_ESCAPE:
                    self.game.set_screen(self.game.screen_menu)
                if not self.snake.direction_changed:
                    print("direction not changed")
                    # press left arrow
                    if event.key == pygame.K_LEFT and self.snake.direction != "right":
                        self.snake.move_left()
                        self.snake.direction_changed = True
                    # press right arrow
                    if event.key == pygame.K_RIGHT and self.snake.direction != "left":
                        self.snake.move_right()
                        self.snake.direction_changed = True
                    # press up arrow
                    if event.key == pygame.K_UP and self.snake.direction != "down":
                        self.snake.move_up()
                        self.snake.direction_changed = True
                    # press down arrow
                    if event.key == pygame.K_DOWN and self.snake.direction != "up":
                        self.snake.move_down()
                        self.snake.direction_changed = True


    def display_score(self):
        # font = pygame.font.SysFont('arial', 30)
        score = get_font(25).render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.SCREEN.blit(score,(1000, 10))         

    def display_test(self):
        mouse_pos = get_font(12).render(f"Mouse Pos: {self.PLAY_MOUSE_POS}", True, (255, 255, 255))
        self.SCREEN.blit(mouse_pos,(1000, 40))

        snake_pos = get_font(12).render(f"Snake Pos: {self.snake.x[0], self.snake.y[0]}", True, (255, 255, 255))
        self.SCREEN.blit(snake_pos,(1000, 60))

        direction = get_font(12).render(f"Direction: {self.snake.direction}", True, (255, 255, 255))
        self.SCREEN.blit(direction,(1000, 80))

        direction_changed = get_font(12).render(f"Direction Changed: {self.snake.direction_changed}", True, (255, 255, 255))
        self.SCREEN.blit(direction_changed,(1000, 100))

    def update(self):
        # print("updating")
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        self.snake.rect = self.snake.block.get_rect(topleft=(self.snake.x[0], self.snake.y[0]))
        # reset direction change flag
        self.snake.direction_changed = False
        # self.food.draw()
        self.snake.walk()
        # collision check with food
        if self.snake.collision_check(self.food):
            self.food.move()
            self.snake.increase_length()
        # collision check with itself
        for i in range(2, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                self.game.set_screen(self.game.screen_menu)
                # self.game.screen_menu.display_test()

    def draw(self):
        # background
        self.SCREEN.blit(self.BG, (0, 0))
        # food
        self.food.draw()
        # snake
        self.snake.draw()
        # score
        self.display_score()
        # test
        self.display_test()


SIZE = 40

class Food:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg")
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
        self.block = pygame.image.load("resources/block.jpg").convert()
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
        self.speed = SIZE
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
    def collision_check(self,other):
        return self.rect.colliderect(other.rect)

    # increase length
    def increase_length(self):
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        self.length += 1

# test
# font = pygame.font.Font(None, 50)
# text_surface = font.render(self.MENU_MOUSE_POS, True, (0, 0, 0))
# text_rect = text_surface.get_rect(center=(10, 10))

# def display_test (self):
#         score = get_font(25).render(f"Score: {self.screen_play.snake.}", True, (255, 255, 255))
#         self.SCREEN.blit(score,(1000, 10))

########## GAME ##########
class Game:
    def __init__(self):
        self.screen_play = PlayScreen(self)
        self.screen_menu = MainMenu(self)


        self.current_screen = self.screen_menu
        self.recent_screen = self.screen_menu


        self.clock = pygame.time.Clock()
        self.running = True

    def set_screen(self, screen):
        self.recent_screen = self.current_screen
        self.current_screen = screen

    def run(self):
        self.current_screen.draw()
        
        # game loop
        while self.running:
            events = pygame.event.get()

            # draw the screen
            if self.current_screen != self.recent_screen:
                self.current_screen.draw()
            # handle events
            self.current_screen.handle_events(events)
            # update the screen
            self.current_screen.update()

            # test show score snake
            score = get_font(25).render(f"Score: {self.screen_play.snake.length}", True, (255, 255, 255))
            self.current_screen.SCREEN.blit(score,(1000, 10))

            # Reset the screen
            pygame.display.update()

            # Limit to 60 frames per second
            self.clock.tick(7)


        pygame.quit()

Game().run()