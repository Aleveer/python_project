import pygame
from Leaderboard import LeaderBoard
from Screen import Screen
from GameplayHandling import Score_and_Mode

class GeneralFunctionHandling(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.leaderboard_screen = LeaderBoard(game)
        self.score_and_mode = Score_and_Mode(game)

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Nếu click vào ô nhập liệu, thì đặt active là True
                if self.leaderboard_screen.input_box.collidepoint(event.pos):
                    self.leaderboard_screen.active = not self.leaderboard_screen.active
                    self.leaderboard_screen.show_prompt = False
                else:
                    self.leaderboard_screen.active = False
                    self.leaderboard_screen.show_prompt = True
                self.leaderboard_screen.color = self.leaderboard_screen.color_active if self.leaderboard_screen.active else self.leaderboard_screen.color_inactive

                # Nếu click vào nút SUBMIT
                if self.leaderboard_screen.submit_button.collidepoint(event.pos):
                    print("an nut submit")
                    if self.leaderboard_screen.text:  # Đảm bảo tên không rỗng
                        print("ten khong rong: ", self.leaderboard_screen.text)
                        print("diem so: ", self.score_and_mode.get_score())
                        self.submit_score(self.leaderboard_screen.text, self.score_and_mode.get_score())
                        self.leaderboard_screen.load_leaderboard()
                        self.leaderboard_screen.text = ''  # Xóa tên nhập sau khi gửi
                        self.leaderboard_screen.input_visible = False  # Ẩn khung nhập và nút
                        self.leaderboard_screen.show_leaderboard = True    #Hiển thị bảng xếp hạng
                    self.leaderboard_screen.show_prompt = True  # Hiển thị lại dòng chữ hướng dẫn
                
                if self.leaderboard_screen.show_leaderboard and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.leaderboard_screen.REPLAY_BUTTON.checkForInput(event.pos):
                        self.leaderboard_screen.input_visible = True
                        self.leaderboard_screen.show_leaderboard = False
                        self.game.set_screen(self.game.screen_menu)
                        self.score_and_mode.reset_score()
                    if self.leaderboard_screen.QUIT_BUTTON.checkForInput(event.pos):
                        self.game.running = False  # Dừng trò chơi

            if event.type == pygame.KEYDOWN:
                print("key down")
                if self.leaderboard_screen.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.leaderboard_screen.text = self.leaderboard_screen.text[:-1]
                    else:
                        self.leaderboard_screen.text += event.unicode

    def submit_score(self, name, score):
        print("submit score: ", name, score)
        
        # Thêm điểm số mới vào file
        with open('leaderboard.txt', 'w') as f:
            f.write(f"{name} {score}\n")

        # Xóa ô nhập và ẩn nó
        self.leaderboard_screen.active = False

    def draw(self):
        self.leaderboard_screen.display_test()
         # background
        self.leaderboard_screen.SCREEN.blit(self.leaderboard_screen.BG, (0, 0))
        self.leaderboard_screen.SCREEN.blit(self.leaderboard_screen.GAME_OVER_TEXT, self.leaderboard_screen.GAME_OVER_RECT)

        # Chỉ vẽ ô nhập và nút nếu input_visible là True
        if self.leaderboard_screen.input_visible:
            if self.leaderboard_screen.show_prompt:
                prompt_surface = self.leaderboard_screen.font.render("Enter your name", True, self.leaderboard_screen.color_inactive)
                prompt_y = self.leaderboard_screen.input_box.y + (self.leaderboard_screen.input_box.height - prompt_surface.get_height()) // 2
                self.leaderboard_screen.SCREEN.blit(prompt_surface, (self.leaderboard_screen.input_box.x + 5, prompt_y))

            txt_surface = self.leaderboard_screen.font.render(self.leaderboard_screen.text, True, self.leaderboard_screen.color)
            width = max(430, txt_surface.get_width() + 10)
            self.leaderboard_screen.input_box.w = width
            text_y = self.leaderboard_screen.input_box.y + (self.leaderboard_screen.input_box.height - txt_surface.get_height()) // 2
            self.leaderboard_screen.SCREEN.blit(txt_surface, (self.leaderboard_screen.input_box.x + 5, text_y))
            
            # Vẽ viền ô nhập liệu
            pygame.draw.rect(self.leaderboard_screen.SCREEN, self.leaderboard_screen.color, self.leaderboard_screen.input_box, 2)

            # Vẽ nút SUBMIT
            mouse_pos = pygame.mouse.get_pos()
            if self.leaderboard_screen.submit_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.leaderboard_screen.SCREEN, self.leaderboard_screen.submit_button_hover_color, self.leaderboard_screen.submit_button)
            else:
                pygame.draw.rect(self.leaderboard_screen.SCREEN, self.leaderboard_screen.submit_button_color, self.leaderboard_screen.submit_button)

            # Vẽ chữ "SUBMIT" trên nút
            submit_text = self.leaderboard_screen.font.render("SUBMIT", True, (255, 255, 255))
            submit_text_rect = submit_text.get_rect(center=self.leaderboard_screen.submit_button.center)
            self.leaderboard_screen.SCREEN.blit(submit_text, submit_text_rect)

        # Nếu leaderboard có các mục, hiển thị chúng
        if self.leaderboard_screen.show_leaderboard:
            leaderboard_title = self.leaderboard_screen.font.render("LEADERBOARD", True, (255, 255, 255))
            self.leaderboard_screen.SCREEN.blit(leaderboard_title, (640 - leaderboard_title.get_width() // 2, 200))

            for index, (name, score) in enumerate(self.leaderboard_screen.leaderboard[:5]):
                leaderboard_entry = self.leaderboard_screen.font.render(f"{index + 1}. {name}: {score}", True, (255, 255, 255))
                self.leaderboard_screen.SCREEN.blit(leaderboard_entry, (500, 250 + index * 30))
    
            # Vẽ nút REPLAY và QUIT
            self.leaderboard_screen.REPLAY_BUTTON.update(self.leaderboard_screen.SCREEN)
            self.leaderboard_screen.QUIT_BUTTON.update(self.leaderboard_screen.SCREEN)