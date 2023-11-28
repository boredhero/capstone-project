import pygame

from game_logger import GameLogger
from config import GameConfig, SettingsConfig
import ui
from settings_menu import SettingsMenu

class InstanceMain():

    def __init__(self):
        """
        Main class
        """
        self.__glogger = GameLogger()
        self.__config = GameConfig()
        self.__settings = SettingsConfig()
        self.__glogger.log_startup(self.__config.version, self.__config.title)
        self.__glogger.info(f"{self.__settings.max_fps} FPS {self.__settings.screen_width} x {self.__settings.screen_height}")
        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height)) # Set the window dimensions
        pygame.display.set_caption(f"{self.__config.title} v{self.__config.version}")
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__pygame_init = pygame.init() #pylint: disable=unused-private-member
        ## Title Screen ##
        self.__titlescreen_ui = ui.TitleScreenUIElements()
        while self.__running:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
            self.__screen.fill("black")
            ui_action = self.__titlescreen_ui.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                match ui_action:
                    case ui.GameState.EXIT:
                        self.graceful_exit()
                    case ui.GameState.SETTINGS:
                        self.__gamesettings = SettingsMenu(self.__screen) # pylint: disable=unused-private-member
                    case _:
                        pass
            self.__titlescreen_ui.draw(self.__screen)
            pygame.display.flip()
            self.__clock.tick(self.__settings.max_fps) # Set the FPS
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
