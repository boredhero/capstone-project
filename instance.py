from game_logger import GameLogger
from config import GameConfig, SettingsConfig
from main_loop import InstanceMainLoop

class InstanceMain():

    def __init__(self):
        """
        Main class
        """
        self.__config = GameConfig()
        self.__settings = SettingsConfig()
        self.init_logger()
        self.__iml = InstanceMainLoop()
        self.__iml.loop()

    def init_logger(self):
        """
        Initialize Logger
        """
        self.__glogger = GameLogger()
        self.__glogger.log_startup(self.__config.version, self.__config.title)
        self.__glogger.info(f"{self.__settings.max_fps} FPS {self.__settings.screen_width} x {self.__settings.screen_height}", name=__name__)

if __name__ == "__main__":
    InstanceMain()
