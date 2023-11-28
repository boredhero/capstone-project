from typing import Any

import yaml
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
        self.settings.add.dropselect(title="Screen Resolution: ", items=self.resolution, default=3, dropselect_id="screen_resolution", selection_box_height=6, open_middle=True)
        self.settings.add.toggle_switch(title="Subtitles", default=False, toggleswitch_id="subtitles")
        self.settings.add.text_input(title="Max FPS: ", default=60, textinput_id="max_fps", input_type=pm.locals.INPUT_INT, range_values=(30, 144), font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Save Settings", action=self.write_game_settings, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Restore Defaults", action=self.__settingsconfig.write_settings_yml_file, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Restart Game to Apply Settings", action=self.settings._exit, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.mainloop(self.__screen)

    def write_game_settings(self):
        """
        Log the game settings
        """
        # getting the data using "get_input_data" method of the Menu class
        screen_width = None
        screen_height = None
        max_fps = None
        subtitles = None
        settings_data = self.settings.get_input_data()
        for key, value in settings_data.items():
            match key:
                case "screen_resolution":
                    screen_res = value[0][0]
                    if screen_res is not None:
                        screen_width, screen_height = [int(value) for value in screen_res.split('x')]
                    else:
                        screen_width = self.__settingsconfig.screen_width
                        screen_height = self.__settingsconfig.screen_height
                case "subtitles":
                    subtitles = value
                    if subtitles is None:
                        subtitles = self.__settingsconfig.subtitles
                case "max_fps":
                    max_fps = value
                    if max_fps is None:
                        max_fps = self.__settingsconfig.max_fps
            self.__glogger.info(f"{key}\t:\t{value}", name=__name__)
            wd = {
                "screen_width": screen_width,
                "screen_height": screen_height,
                "max_fps": max_fps,
                "subtitles": subtitles
            }
            try:
                with open(self.__settingsconfig.config_name, 'w') as settings_file:
                    yaml.dump(wd, settings_file)
            except Exception as e:
                print("Settings failed to write to disk", e)

    def __get_settings_state_from_disk(self) -> dict:
        """
        Try and load the settings from the disk
        """
        return {
            "screen_width": self.__settingsconfig.screen_width,
            "screen_height": self.__settingsconfig.screen_height,
            "max_fps": self.__settingsconfig.max_fps
        }
