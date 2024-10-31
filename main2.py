import pygame
import sys
import time
from button import Button

SIZE = 40

def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/font.ttf", size)

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()

        self.length = length

        self.x = [SIZE] * length
        self.y = [SIZE] * length

        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

        pygame.display.flip()

class Screen:
    def __init__(self):
        pygame.display.set_caption("Snake Game")
        self.SCREEN = pygame.display.set_mode((1280, 720))

    
    def main_menu(self):
        # VARIABLES
        MENU_TEXT = get_font(100).render("SNAKE GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.BG = pygame.image.load("resources/Background.png")

        # DRAWING SOMTHING ONTO THE SCREEN
        self.SCREEN.blit(self.BG, (0, 0))
        self.SCREEN.blit(MENU_TEXT, MENU_RECT)

        # CREATE BUTTONS
        PLAY_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("resources/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        # UPDATE BUTTONS
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.SCREEN)

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()              
        # UPDATE SCREEN
        # pygame.display.update()
    
    def play(self):
        # pass
        running = True
        BG = pygame.image.load("resources/background.jpg")
        self.SCREEN.fill("white")
        self.SCREEN.blit(BG, (0, 0))
        
        snake = Snake(self.SCREEN, 1)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = Screen()
        

    def run(self):
        running = True
        # self.screen.main_menu()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.main_menu()
            pygame.display.flip() 

game = Game()
game.run()