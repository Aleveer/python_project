import pygame
import sys
import random
from button import Button
from abc import ABC, abstractmethod

# Initialize pygame
pygame.init()

def get_font(size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/font.ttf", size)

def save_leaderboard(leaderboard):
    print("lưu: ",leaderboard," vào file")
    with open('leaderboard.txt', 'w') as f:
        for name, score in leaderboard:
            f.write(f"{name} {score}\n")
    print("Leaderboard saved.")


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
        self.PLAY_BUTTON = Button(image=pygame.image.load("resources/Play Rect.png"), pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")
        self.QUIT_BUTTON = Button(image=pygame.image.load("resources/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Yellow")
        
        # show leaderboard

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

########## GAME OVER SCREEN ##########
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

####### checkForInput ########
def checkForInput(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
        return True
    return False

######LEADERBOARD######
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


    def display_test(self):
        # score = get_font(25).render(f"Score: {self.game.score_and_mode.get_score()}", True, (255, 255, 255))
        # self.SCREEN.blit(score,(1000, 10))
        pass

    def load_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as f:
                for line in f:
                    print("line: ", line)
                    name, score = line.strip().split(" ")  # Tách name và score
                    self.leaderboard.append((name, int(score)))

            self.leaderboard = list(set(self.leaderboard)) # Loại bỏ các mục trùng lặp

            # with open("leaderboard.txt", "w") as f:
            #     for name, score in self.leaderboard:
            #         f.write(f"{name} {score}\n")

            self.leaderboard.sort(key=lambda x: x[1], reverse=True)
            print("load leaderboard: ", self.leaderboard)
        except FileNotFoundError:
            print("File leaderboard.txt not found.")

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

            # Ấn Enter
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.text:
                    print("ten khong rong: ", self.text)
                    self.submit_score(self.text, self.game.score_and_mode.get_score())
                    self.load_leaderboard()
                    self.text = ''  # Xóa tên nhập sau khi gửi
                    self.input_visible = False  # Ẩn khung nhập và nút
                    self.show_leaderboard = True    #Hiển thị bảng xếp hạng
                self.show_prompt = True  # Hiển thị lại dòng chữ hướng dẫn

            # Nếu active là True, thì cho phép nhập liệu
            if event.type == pygame.KEYDOWN:
                print("key down")
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def submit_score(self, name, score):
        print("submit score: ", name, score)
        
        # Thêm điểm số mới vào file
        with open('leaderboard.txt', 'w') as f:
            f.write(f"{name} {score}\n")

        # Xóa ô nhập và ẩn nó
        self.active = False

    def update(self):
        pass

    def draw(self):
        self.display_test()
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

            

########## PLAY SCREEN ##########
class PlayScreen(Screen):
    def __init__(self,game):
        super().__init__(game)
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        self.BG = pygame.image.load("resources/background.jpg")
        # food
        self.food = Food(self.SCREEN)
        # snake
        self.snake = Snake(self.SCREEN, 2)
        # timer for snake movement
        self.snake_move_timer = 0
        self.snake_move_delay = 50  # milliseconds  #the real value handled in class Game

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)


    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            # test click food
            '''
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if checkForInput(self.food, self.PLAY_MOUSE_POS):
            #         # self.food.move()
            #         # self.game.running = False
            #         print("clicked")
            '''
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
            # check for key presses HANDLED
            if event.type == pygame.KEYDOWN:
                # press esc
                if event.key == pygame.K_ESCAPE:
                    self.game.set_screen(self.game.screen_menu)
                if not self.snake.direction_changed and self.snake.move_counter >= SIZE:
                    # press left arrow
                    if event.key == pygame.K_LEFT and self.snake.direction != "right":
                        self.snake.move_left()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    # press right arrow
                    if event.key == pygame.K_RIGHT and self.snake.direction != "left":
                        self.snake.move_right()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    # press up arrow
                    if event.key == pygame.K_UP and self.snake.direction != "down":
                        self.snake.move_up()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0
                    # press down arrow
                    if event.key == pygame.K_DOWN and self.snake.direction != "up":
                        self.snake.move_down()
                        self.snake.direction_changed = True
                        self.snake.move_counter = 0

    def display_score(self):
        score = get_font(25).render(f"Score: {self.game.score_and_mode.get_score()}", True, (255, 255, 255))
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

        # mode
        mode = get_font(12).render(f"Mode: {self.game.score_and_mode.get_mode()}", True, (255, 255, 255))
        self.SCREEN.blit(mode,(1000, 120))

    def update(self):
        # print("updating")
        # reset direction change flag
        self.snake.direction_changed = False

        # update mouse position
        self.PLAY_MOUSE_POS = pygame.mouse.get_pos()
        # test ability
        # self.display_test()
        # update snake rect
        self.snake.rect = self.snake.block.get_rect(topleft=(self.snake.x[0], self.snake.y[0]))
        
        # update snake movement based on timer
        self.snake_move_timer += self.game.clock.get_time()
        if self.snake_move_timer >= self.snake_move_delay:
            self.snake.walk()
            self.snake_move_timer = 0

        # collision check with food
        if self.snake.collision_check(self.food):
            self.play_sound("90games")
            self.food.move()
            self.snake.increase_length()
            self.game.score_and_mode.increase_score()

        #collision check with wall
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1280-SIZE or self.snake.y[0] < 0 or self.snake.y[0] >= 720-SIZE:
            pygame.mixer.music.stop()
            self.play_sound("gameover")
            self.collision_wall()

        # collision check with itself
        for i in range(2, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                pygame.mixer.music.stop()
                self.play_sound("gameover")
                self.game.set_screen(self.game.screen_gameover)
                # reset screen play 
                self.game.screen_play = PlayScreen(self.game)

    def collision_wall(self):
        self.game.set_screen(self.game.screen_gameover)
        # reset screen play
        self.game.screen_play = PlayScreen(self.game)

         
    def draw(self):
        # background
        self.SCREEN.blit(self.BG, (0, 0))
        # food
        self.food.draw()
        # snake
        self.snake.draw()
        # score
        self.display_score()

SIZE = 40

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
    def collision_check(self,other):
        return self.rect.colliderect(other.rect)

    # increase length
    def increase_length(self):
        for i in range(7):
            self.x.append(self.x[-1])
            self.y.append(self.y[-1])
            self.length += 1

# SCORE AND MODE
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

# test
'''
# font = pygame.font.Font(None, 50)
# text_surface = font.render(self.MENU_MOUSE_POS, True, (0, 0, 0))
# text_rect = text_surface.get_rect(center=(10, 10))

# def display_test (self):
#         score = get_font(25).render(f"Score: {self.screen_play.snake.}", True, (255, 255, 255))
#         self.SCREEN.blit(score,(1000, 10))
'''
########## GAME ##########
class Game:
    def __init__(self):
        # create screens
        self.screen_menu = MainMenu(self)
        self.screen_play = PlayScreen(self)
        self.screen_gameover = GameOverScreen(self)
        self.leaderboard_screen = LeaderBoard(self)

        # set the current screen
        self.current_screen = self.screen_menu
        # self.recent_screen = self.screen_menu

        # score and mode
        self.score_and_mode = Score_and_Mode(self)

        # create other attributes
        self.clock = pygame.time.Clock()
        self.running = True

    def set_screen(self, screen):
        if self.current_screen != screen:
            self.current_screen = screen
            # self.recent_screen = self.current_screen

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