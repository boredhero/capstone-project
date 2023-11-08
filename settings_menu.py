from typing import Any

import pygame_menu as pm

from ui import GameColors
from game_logger import GameLogger
from config import SettingsConfig
class SettingsMenu:

    def __init__(self, screen: Any):
        """
        SettingsMenu init
        https://www.geeksforgeeks.org/create-settings-menu-in-python-pygame/
        """
        self.__screen = screen
        self.__glogger = GameLogger()
        self.__settingsconfig = SettingsConfig()
        try:
            self.__settings_state = self.__get_settings_state_from_disk() # pylint: disable=unused-private-member
            self.__glogger.debug(f"Loaded settings from disk: {self.__settings_state}", name=__name__)
        except Exception as e:
            self.__settings_state = {} #pylint: disable=unused-private-member
            self.__glogger.error(f"Failed to load settings from disk: {e}", name=__name__)
        self.resolution = [
            ("3840x2160", "3840x2160"),
            ("2650x1440", "2650x1440"),
            ("1920x1200", "1920x1200"),
            ("1920x1080", "1920x1080"),
            ("1280x720", "1280x720"),
            ("800x600", "800x600")
        ]
        self.settings = pm.Menu(title="Settings",
                                width=self.__settingsconfig.screen_width,
                                height=self.__settingsconfig.screen_height,
                                theme=pm.themes.THEME_DARK)
        self.settings._theme.widget_font_size = 25
        self.settings._theme.widget_font_color = GameColors.WHITE.value
        self.settings._theme.widget_alignment = pm.locals.ALIGN_LEFT
        self.settings.add.dropselect(title="BSR: ", items=self.resolution, default=3, dropselect_id="screen_resolution2", selection_box_height=6, open_middle=True)
        self.settings.add.dropselect_multiple(title="Screen Resolution: ", items=self.resolution, open_middle=True, max_selected=1, selection_box_height=6, default=[3], dropselect_multiple_id="screen_resolution")
        self.settings.add.toggle_switch(title="Subtitles", default=False, toggleswitch_id="subtitles")
        self.settings.add.button(title="Print Settings", action=self.write_game_settings, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Restore Defaults", action=self.__settingsconfig.write_settings_yml_file, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Restart Game to Save/Apply", action=self.settings._exit, align=pm.locals.ALIGN_CENTER)
        self.settings.mainloop(self.__screen)

    def get_current_resolution_index(self) -> int:
        """
        Get the current resolution index
        """
        match self.__settingsconfig.screen_height:
            case 2160:
                return 0
            case 1440:
                return 1
            case 1200:
                return 2
            case 1080:
                return 3
            case 720:
                return 4
            case 600:
                return 5
            case _:
                return 3

    def write_game_settings(self):
        """
        Log the game settings
        """
        # getting the data using "get_input_data" method of the Menu class
        screen_width = None
        screen_height = None
        max_fps = None
        settings_data = self.settings.get_input_data()
        for key, value in settings_data.items():
            match key:
                case "screen_resolution":
                    screen_width = value[0][0][0]
                    self.__glogger.debug(f"screen_width_write: {screen_width}", name=__name__)
                    screen_height = value[0][0][1]
                    self.__glogger.debug(f"screen_height_write: {screen_height}", name=__name__)
                case "max_fps":
                    max_fps = value
                    if max_fps is None:
                        max_fps = self.__settingsconfig.max_fps
            self.__glogger.info(f"{key}\t:\t{value}", name=__name__)

    def __get_settings_state_from_disk(self) -> dict:
        """
        Try and load the settings from the disk
        """
        return {
            "screen_width": self.__settingsconfig.screen_width,
            "screen_height": self.__settingsconfig.screen_height,
            "max_fps": self.__settingsconfig.max_fps
        }

    def __get_default_setting_for(self, setting_name: str) -> Any | None:
        """
        Get the default settings
        """
        defaults = self.__settingsconfig.get_default_settings()
        if setting_name in defaults:
            return defaults[setting_name]
        return None
