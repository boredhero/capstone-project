
import os, traceback

import yaml
from dotenv import load_dotenv

from misc import Singleton

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

class SettingsConfig(metaclass=Singleton):

    def __init__(self):
        """
        Modifiable config
        """
        self.config_name = "settings.yml"
        self.__settings = {}
        self.__load_settings()
        self.screen_width = self.__settings.get("screen_width")
        self.screen_height = self.__settings.get("screen_height")
        self.window_mode = self.__settings.get("window_mode")
        self.max_fps = self.__settings.get("max_fps")
        self.puzzle_1_difficulty = self.__settings.get("puzzle_1_difficulty")
        self.puzzle_1_difficulty_mult = self.__settings.get("puzzle_1_difficulty_mult")
        self.puzzle_1_difficulty_speed = self.__settings.get("puzzle_1_difficulty_speed")
        self.puzzle_1_difficulty_fitts = self.__settings.get("puzzle_1_difficulty_fitts")
        self.puzzle_2_difficulty_speed = self.__settings.get("puzzle_2_difficulty_speed")
        self.puzzle_2_difficulty_number = self.__settings.get("puzzle_2_difficulty_number")
        self.subtitles = self.__settings.get("subtitles")
        self.debug = self.__settings.get("debug")
        self.fancy_fonts = self.__settings.get("fancy_fonts")
        self.grayscale_mode = self.__settings.get("grayscale_mode")
        self.keybind_up = self.__settings.get("keybind_up")
        self.keybind_down = self.__settings.get("keybind_down")
        self.keybind_right = self.__settings.get("keybind_right")
        self.keybind_left = self.__settings.get("keybind_left")
        self.keybind_interact = self.__settings.get("keybind_interact")
        # Artificially constructed helpers
        match self.screen_height:
            case 2160:
                self.screen_size_speed_multiplier = 2
            case 1440:
                self.screen_size_speed_multiplier = 1.5
            case 1080:
                self.screen_size_speed_multiplier = 1
            case 720:
                self.screen_size_speed_multiplier = 0.8
            case _:
                self.screen_size_speed_multipliere = 1

    def __load_settings(self):
        """
        Load settings
        """
        exists = os.path.isfile(self.config_name)
        if exists is True:
            try:
                with open(self.config_name, 'r') as settings_file:
                    self.__settings = yaml.unsafe_load(settings_file) # pylint: disable=no-value-for-parameter
            except Exception as e:
                print("Settings failed to load initially, using defaults", e)
                self.__settings = self.get_default_settings()
        else:
            try:
                with open(self.config_name, 'w') as settings_file:
                    yaml.dump(self.get_default_settings(), settings_file)
                    self.__settings = self.get_default_settings()
            except Exception as e:
                print("Settings failed to load on write, using defaults", e)
                self.__settings = self.get_default_settings()

    def get_settings_refresh(self):
        """
        Get the settings after reloading the config from disk (slower)
        """
        self.__load_settings()
        return self.__settings

    def get_settings_no_refresh(self):
        """
        Get the settings immediately without reloading the config from disk (faster)
        """
        return self.__settings

    def get_default_settings(self):
        """
        Default config to write if no config exists somehow
        """
        return {
            "screen_width": 1920,
            "screen_height": 1080,
            "window_mode": "windowed",
            "max_fps": 60,
            "puzzle_1_difficulty": 10,
            "puzzle_1_difficulty_mult": 870,
            "puzzle_1_difficulty_speed": 7,
            "puzzle_1_difficulty_fitts": 1.5,
            "puzzle_2_difficulty_speed": 10,
            "puzzle_2_difficulty_number": 20,
            "subtitles": True,
            "debug": False,
            "fancy_fonts": True,
            "grayscale_mode": False,
            "keybind_up": "w",
            "keybind_down": "s",
            "keybind_right": "d",
            "keybind_left": "a",
            "keybind_interact": "e"
        }

    def __write_settings_yml_file(self, contents: dict | None = None):
        """
        Write settings file to disc
        NOTE: If contents are None, the default settings will be written to disk
        """
        if contents is None:
            contents = self.get_default_settings()
        try:
            with open(self.config_name, 'w') as settings_file:
                yaml.dump(contents, settings_file)
        except Exception as e:
            print("Settings failed to write to disk", e)
        self.refresh_from_disk()

    def write_default_settings(self):
        """
        Write default settings to disk
        """
        self.__write_settings_yml_file()

    def refresh_from_disk(self):
        """
        Re-Run __init__ on this Singleton class, thus changing the values to match those on disk
        """
        self.__init__() # pylint: disable=unnecessary-dunder-call
