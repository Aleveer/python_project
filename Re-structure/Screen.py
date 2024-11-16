import pygame
from abc import ABC, abstractmethod

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