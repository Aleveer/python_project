from Screen import Screen
from Button import Button
from PlayScreen import PlayScreen
from utilities import get_font
import pygame

class GameOverScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        # Dừng nhạc nền khi vào màn hình Game Over
        pygame.mixer.music.stop()
        # Lấy vị trí chuột
        #self.GAMEOVER_MOUSE_POS = pygame.mouse.get_pos()
        # Background
        self.BG = pygame.image.load("resources/Background.png")
        # Điểm số
        # self.score = self.game.score_and_mode.get_score()
        self.SCORE_TEXT = get_font(30).render(f"You lose", True, "#FFFFFF")
        self.SCORE_RECT = self.SCORE_TEXT.get_rect(center=(640, 280))

        # Text Game Over
        self.GAMEOVER_TEXT = get_font(100).render("GAME OVER", True, "#FF0000")
        self.GAMEOVER_RECT = self.GAMEOVER_TEXT.get_rect(center=(640, 150))
        
        # Tạo các nút
        self.SAVE_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 500), 
                            text_input="SAVE", font=get_font(70), base_color="#d7fcd4", hovering_color="Yellow")
        self.RETRY_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 650), 
                            text_input="RETRY", font=get_font(70), base_color="#d7fcd4", hovering_color="Yellow")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.SAVE_BUTTON.checkForInput(self.GAMEOVER_MOUSE_POS):
                    self.game.screen_play = PlayScreen(self.game)  # Tạo màn chơi mới
                    self.game.set_screen(self.game.leaderboard_screen)
                
                if self.RETRY_BUTTON.checkForInput(self.GAMEOVER_MOUSE_POS):
                    self.game.screen_play = PlayScreen(self.game)
                    self.game.set_screen(self.game.screen_menu)

    def update(self):
        self.GAMEOVER_MOUSE_POS = pygame.mouse.get_pos()
        self.SAVE_BUTTON.changeColor(self.GAMEOVER_MOUSE_POS)
        self.SAVE_BUTTON.update(self.SCREEN)
        self.RETRY_BUTTON.changeColor(self.GAMEOVER_MOUSE_POS)
        self.RETRY_BUTTON.update(self.SCREEN)

    def draw(self):
        self.SCREEN.blit(self.BG, (0, 0))
        self.SCREEN.blit(self.GAMEOVER_TEXT, self.GAMEOVER_RECT)
        self.SCREEN.blit(self.SCORE_TEXT, self.SCORE_RECT)
        self.SAVE_BUTTON.update(self.SCREEN)
        self.RETRY_BUTTON.update(self.SCREEN)