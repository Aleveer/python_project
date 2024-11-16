import Screen, pygame
from Button import Button
from utilities import get_font
from Screen import Screen

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
        self.PLAY_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")
        self.QUIT_BUTTON = Button(image=pygame.image.load("resources/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.PLAY_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    pygame.mixer.music.load("resources/bg_music.mp3")
                    pygame.mixer.music.play(loops=-1)
                    pygame.mixer.music.set_volume(0.5)
                    self.game.set_screen(self.game.screen_play)
                if self.QUIT_BUTTON.checkForInput(self.MENU_MOUSE_POS):
                    self.game.running = False
                self.click_change_mode(self.MENU_MOUSE_POS)

    def update(self):
        self.MENU_MOUSE_POS = pygame.mouse.get_pos()
        self.PLAY_BUTTON.changeColor(self.MENU_MOUSE_POS)
        self.QUIT_BUTTON.changeColor(self.MENU_MOUSE_POS)
        self.PLAY_BUTTON.update(self.SCREEN)
        self.QUIT_BUTTON.update(self.SCREEN)
        # self.display_test()
        self.draw_mode() 

    def draw(self):
        # background
        self.SCREEN.blit(self.BG, (0, 0))
        # title
        self.SCREEN.blit(self.MENU_TEXT, self.MENU_RECT)
    
    def display_test(self):
        # mouse position
        mouse_pos = get_font(12).render(f"Mouse Pos: {self.MENU_MOUSE_POS}", True, (255, 255, 255))
        self.SCREEN.blit(mouse_pos,(1000, 40))
        # mode
        mode = get_font(12).render(f"Mode: {self.game.score_and_mode.get_mode()}", True, (255, 255, 255))
        self.SCREEN.blit(mode,(1000, 60))
        # print("drawing_menu")

    def draw_mode(self):
        # Thiết lập màu sắc cho từng mode
        colors = {
            "easy": (0, 255, 0),    # màu xanh lá
            "normal": (255, 255, 0), # màu vàng
            "hard": (255, 0, 0)      # màu đỏ
        }

        modes = ["easy", "normal", "hard"]

        x_position = 450  # Vị trí x ban đầu để bắt đầu vẽ các mode
        for mode in modes:
            color = colors[mode] if self.game.score_and_mode.get_mode() == mode else (255, 255, 255)  # Màu trắng cho mode không được chọn
            mode_text = get_font(15).render(mode.capitalize(), True, color)
            self.SCREEN.blit(mode_text, (x_position, 240))

            self.game.score_and_mode.mode_rects[mode] = mode_text.get_rect(topleft=(x_position, 240))

            x_position += 150  # Tăng vị trí x để các mode không chồng lên nhau

    def click_change_mode(self, mouse_pos):
        for mode, rect in self.game.score_and_mode.mode_rects.items():
            if rect.collidepoint(mouse_pos):
                self.game.score_and_mode.set_mode(mode) 
                print("change mode to: ", mode)
                break
