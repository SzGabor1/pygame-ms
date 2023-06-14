import pygame
import sys
from pygameZoom import *
from debug import *
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), flags=pygame.SCALED, vsync=1)  # vsync solves the screen tearing issue
        pygame.display.set_caption("Marooned Sailor")
        self.clock = pygame.time.Clock()
        self.level = Level()

        # sound

        # main_sound = pygame.mixer.Sound('audio/main.ogg')
        # main_sound.set_volume(0.1)
        # main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.level.toggle_menu('talents')
            self.screen.fill('#71DDEE')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
