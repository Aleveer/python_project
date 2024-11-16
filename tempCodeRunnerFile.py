   def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)