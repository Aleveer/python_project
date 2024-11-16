import pygame
from Screen import Screen
from utilities import get_font, SIZE
from GameplayHandling import Food, Snake, Score_and_Mode

class PlayScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        self.BG = pygame.image.load("resources/background.jpg")
        # food
        self.food = Food(self.SCREEN)
        # snake
        self.snake = Snake(self.SCREEN, 2)
        # score and mode
        self.score_and_mode = game.score_and_mode  # Use the existing instance from the game
        # timer for snake movement
        self.snake_move_timer = 0
        self.snake_move_delay = 50  # milliseconds  #the real value handled in class Game

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_screen(self.game.screen_menu)
                if not self.snake.direction_changed and self.snake.move_counter >= SIZE:
                    if event.key == pygame.K_LEFT and self.snake.direction != "right":
                        self.snake.move_left()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    if event.key == pygame.K_RIGHT and self.snake.direction != "left":
                        self.snake.move_right()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    if event.key == pygame.K_UP and self.snake.direction != "down":
                        self.snake.move_up()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    if event.key == pygame.K_DOWN and self.snake.direction != "up":
                        self.snake.move_down()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0

    def update(self):
        self.snake.direction_changed = False
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        self.snake.rect = self.snake.block.get_rect(topleft=(self.snake.x[0], self.snake.y[0]))
        self.snake_move_timer += self.game.clock.get_time()
        if self.snake_move_timer >= self.snake_move_delay:
            self.snake.walk()
            self.snake_move_timer = 0
        if self.snake.collision_check(self.food):
            print("Collision detected with food")
            self.play_sound("90games")
            self.food.move()
            self.snake.increase_length()
            self.score_and_mode.increase_score()  # Ensure this line is present
            print(f"Score after eating food: {self.score_and_mode.get_score()}")
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1280 - SIZE or self.snake.y[0] < 0 or self.snake.y[0] >= 720 - SIZE:
            pygame.mixer.music.stop()
            self.play_sound("gameover")
            self.collision_wall()
        for i in range(2, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                pygame.mixer.music.stop()
                self.play_sound("gameover")
                self.game.set_screen(self.game.screen_gameover)
                self.game.screen_play = PlayScreen(self.game)

    def collision_wall(self):
        self.game.set_screen(self.game.screen_gameover)
        self.game.screen_play = PlayScreen(self.game)

    def draw(self):
        self.SCREEN.blit(self.BG, (0, 0))
        self.food.draw()
        self.snake.draw()
        self.display_score()

    def display_score(self):
        score = get_font(25).render(f"Score: {self.score_and_mode.get_score()}", True, (255, 255, 255))
        self.SCREEN.blit(score, (1000, 10))