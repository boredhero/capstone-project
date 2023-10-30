## TODO: Rename this file if the working title changes from "Instance"
import pygame

from game_logger import GameLogger
from config import GameConfig

class InstanceMain():

    def __init__(self):
        """
        Main class
        """
        self.__glogger = GameLogger()
        self.__config = GameConfig()
        self.__glogger.log_startup(self.__config.version, self.__config.title)
        pygame.init()
        self.__screen = pygame.display.set_mode((1280, 720))
        self.__clock = pygame.time.Clock()
        self.__running = True
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
            self.__screen.fill("black")
            pygame.display.flip()
            self.__clock.tick(60)
        self.graceful_exit()

    def get_screen(self):
        """
        Get the screen
        """
        return self.__screen

    def get_clock(self):
        """
        Get the clock
        """
        return self.__clock

    def graceful_exit(self):
        """
        Gracefully quit the program
        """
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    InstanceMain()
