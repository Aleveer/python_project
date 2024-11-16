import pygame
from Screen import Screen
from utilities import get_font, SIZE
from Button import Button

########## LEADERBOARD SCREEN ##########
class LeaderBoard(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.GAME_OVER_TEXT = get_font(60).render("SNAKE GAME", True, "#b68f40")
        self.GAME_OVER_RECT = self.GAME_OVER_TEXT.get_rect(center=(640, 100))
        # background
        self.BG = pygame.image.load("resources/Background.png")
        # Thêm thuộc tính để lưu tên
        # Đặt kích thước ô nhập liệu
        self.input_box_width = 400
        self.input_box_height = 60
        
        # Tính toán vị trí x để đặt ô nhập liệu ở giữa
        self.input_box_x = (1280 - self.input_box_width) // 2  # 1280 là chiều rộng màn hình
        self.input_box = pygame.Rect(self.input_box_x, 250, self.input_box_width, self.input_box_height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.active = False
        self.font = get_font(24)
        # Thêm thuộc tính để lưu trạng thái hiển thị dòng chữ hướng dẫn
        self.show_prompt = True  # Biến này sẽ xác định xem có hiển thị dòng chữ hay không
        # Tạo nút SUBMIT
        self.submit_button = pygame.Rect(self.input_box_x, self.input_box.y + self.input_box_height + 10, 430, self.input_box_height)  # Vị trí bên dưới ô nhập liệu
        self.submit_button_color = pygame.Color('dodgerblue2')
        self.submit_button_hover_color = pygame.Color('lightskyblue3')
        # Dữ liệu leaderboard
        self.leaderboard = []  # Danh sách các tuple (tên, điểm)
        self.max_leaderboard_size = 5  # Số lượng tối đa trong leaderboard
        # Biến để xác định xem khung nhập liệu có hiển thị hay không
        self.input_visible = True
        # Thay đổi kích thước
        quit_image = pygame.image.load("resources/Quit Rect.png").convert_alpha()
        quit_image = pygame.transform.scale(quit_image, (250, 80))
        self.REPLAY_BUTTON = Button(image=quit_image, pos=(640, 500),
                                    text_input="REPLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="Yellow")
        self.QUIT_BUTTON = Button(image=quit_image, pos=(640, 600), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="Yellow")
        
        self.show_leaderboard = False  # Biến này xác định xem có hiển thị bảng xếp hạng hay không

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Nếu click vào ô nhập liệu, thì đặt active là True
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                    self.show_prompt = False
                else:
                    self.active = False
                    self.show_prompt = True
                self.color = self.color_active if self.active else self.color_inactive
                # Nếu click vào nút SUBMIT
                if self.submit_button.collidepoint(event.pos):
                    print("an nut submit")
                    if self.text:  # Đảm bảo tên không rỗng
                        print("ten khong rong: ", self.text)
                        self.submit_score(self.text, self.game.score_and_mode.get_score())
                        self.load_leaderboard()
                        self.text = ''  # Xóa tên nhập sau khi gửi
                        self.input_visible = False  # Ẩn khung nhập và nút
                        self.show_leaderboard = True    #Hiển thị bảng xếp hạng
                    self.show_prompt = True  # Hiển thị lại dòng chữ hướng dẫn
                
                if self.show_leaderboard and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.REPLAY_BUTTON.checkForInput(event.pos):
                        self.input_visible = True
                        self.show_leaderboard = False
                        self.game.set_screen(self.game.screen_menu)
                        self.game.score_and_mode.reset_score()
                    if self.QUIT_BUTTON.checkForInput(event.pos):
                        self.game.running = False  # Dừng trò chơi
            if event.type == pygame.KEYDOWN:
                print("key down")
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def update(self):
        self.REPLAY_BUTTON.changeColor(pygame.mouse.get_pos())
        self.QUIT_BUTTON.changeColor(pygame.mouse.get_pos())

    def draw(self):
        # background
        self.SCREEN.blit(self.BG, (0, 0))
        self.SCREEN.blit(self.GAME_OVER_TEXT, self.GAME_OVER_RECT)
        # Chỉ vẽ ô nhập và nút nếu input_visible là True
        if self.input_visible:
            if self.show_prompt:
                prompt_surface = self.font.render("Enter your name", True, self.color_inactive)
                prompt_y = self.input_box.y + (self.input_box.height - prompt_surface.get_height()) // 2
                self.SCREEN.blit(prompt_surface, (self.input_box.x + 5, prompt_y))
            txt_surface = self.font.render(self.text, True, self.color)
            width = max(430, txt_surface.get_width() + 10)
            self.input_box.w = width
            text_y = self.input_box.y + (self.input_box.height - txt_surface.get_height()) // 2
            self.SCREEN.blit(txt_surface, (self.input_box.x + 5, text_y))
            
            # Vẽ viền ô nhập liệu
            pygame.draw.rect(self.SCREEN, self.color, self.input_box, 2)
            # Vẽ nút SUBMIT
            mouse_pos = pygame.mouse.get_pos()
            if self.submit_button.collidepoint(mouse_pos):
                pygame.draw.rect(self.SCREEN, self.submit_button_hover_color, self.submit_button)
            else:
                pygame.draw.rect(self.SCREEN, self.submit_button_color, self.submit_button)
            # Vẽ chữ "SUBMIT" trên nút
            submit_text = self.font.render("SUBMIT", True, (255, 255, 255))
            submit_text_rect = submit_text.get_rect(center=self.submit_button.center)
            self.SCREEN.blit(submit_text, submit_text_rect)
        # Nếu leaderboard có các mục, hiển thị chúng
        if self.show_leaderboard:
            leaderboard_title = self.font.render("LEADERBOARD", True, (255, 255, 255))
            self.SCREEN.blit(leaderboard_title, (640 - leaderboard_title.get_width() // 2, 200))
            for index, (name, score) in enumerate(self.leaderboard[:5]):
                leaderboard_entry = self.font.render(f"{index + 1}. {name}: {score}", True, (255, 255, 255))
                self.SCREEN.blit(leaderboard_entry, (500, 250 + index * 30))
    
            # Vẽ nút REPLAY và QUIT
            self.REPLAY_BUTTON.update(self.SCREEN)
            self.QUIT_BUTTON.update(self.SCREEN)
            
    def submit_score(self, name, score):
        print("submit score: ", name, score)
        
        # Thêm điểm số mới vào file
        with open('leaderboard.txt', 'w') as f:
            f.write(f"{name} {score}\n")

        # Xóa ô nhập và ẩn nó
        self.active = False

    def load_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    print("line: ", line)
                    parts = line.strip().split()  # Split by any whitespace
                    if len(parts) >= 2:
                        name = " ".join(parts[:-1])  # Join all parts except the last one as the name
                        score = int(parts[-1])  # The last part is the score
                        self.leaderboard.append((name, score))

            self.leaderboard = list(set(self.leaderboard))  # Loại bỏ các mục trùng lặp

            self.leaderboard.sort(key=lambda x: x[1], reverse=True)
            print("load leaderboard: ", self.leaderboard)
        except FileNotFoundError:
            print("File leaderboard.txt not found.")