
import os, traceback
from dotenv import load_dotenv

class GameConfig():

    def __init__(self):
        """
        Static config, loaded once on game boot
        """
        load_dotenv()
        self.__env = os.environ
        try:
            self.version = self.__env.get("version")
            self.title = self.__env.get("title")
        except Exception:
            print("Keys missing in .env config file", traceback.format_exc())
