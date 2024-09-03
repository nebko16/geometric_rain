import sys
import pygame
from geometric_rain.classes.input import Inputs



class Menu(Inputs):

    def __init__(self, display):
        super().__init__()
        self.display = display
        self.clock = pygame.time.Clock()

    def iteration(self):
        self.event_loop()
        self.key_check()
        return self.render()

    def render(self):
        return pygame.surface.Surface(self.display.content_size)

    def end_game(self):
        self.running = False
        pygame.quit()
        sys.exit()
