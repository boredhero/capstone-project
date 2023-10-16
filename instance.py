## TODO: Rename this file if the working title changes from "Instance"
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
        self.__glogger.info("Test Info", name=__name__)
        self.__glogger.error("Test Error", name=__name__)
        self.__glogger.debug("Test Debug", name=__name__)
        self.__glogger.warning("Test Warning", name=__name__)
        self.__glogger.critical("Test Critical", name=__name__)
        self.graceful_exit()

    def graceful_exit(self):
        """
        Gracefully quit the program
        """
        exit(0)

if __name__ == "__main__":
    InstanceMain()
