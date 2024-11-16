from MainMenu import MainMenu
from PlayScreen import PlayScreen
from GameOver import GameOverScreen
from Leaderboard import LeaderBoard
from GameplayHandling import Score_and_Mode

import pygame
########## GAME ##########
class Game:
    def __init__(self):
        # Initialize Pygame and font module
        pygame.init()
        pygame.font.init()
        
        # score and mode
        self.score_and_mode = Score_and_Mode(self)

        # create screens
        self.screen_menu = MainMenu(self)
        self.screen_play = PlayScreen(self)
        self.screen_gameover = GameOverScreen(self)
        self.leaderboard_screen = LeaderBoard(self)
        # set the current screen
        self.current_screen = self.screen_menu
        # self.recent_screen = self.screen_menu

        # create other attributes
        self.clock = pygame.time.Clock()
        self.running = True

    def set_screen(self, screen):
        if self.current_screen != screen:
            self.current_screen = screen
            self.current_screen.draw()
            pygame.display.update()

    def run(self):
        self.current_screen.draw()
        
        # game loop
        while self.running:
            events = pygame.event.get()

            # draw the screen
            self.current_screen.draw()
            
            # handle events
            self.current_screen.handle_events(events)

            # update the screen
            self.current_screen.update()

            # Limit to 60 frames per second
            if self.current_screen == self.screen_play:
                if self.score_and_mode.get_mode() == "easy":
                    self.screen_play.snake_move_delay = 50
                elif self.score_and_mode.get_mode() == "normal":
                    self.screen_play.snake_move_delay = 30
                elif self.score_and_mode.get_mode() == "hard":
                    self.screen_play.snake_move_delay = 10
            self.clock.tick(60)
            # Reset the screen
            pygame.display.update()

        pygame.quit()

Game().run()