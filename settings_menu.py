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
            ("1920x1080", "1920x1080"),
            ("1280x720", "1280x720")
        ]
        self.settings = pm.Menu(title="Settings",
                                width=self.__settingsconfig.screen_width,
                                height=self.__settingsconfig.screen_height,
                                theme=pm.themes.THEME_DARK)
        self.settings._theme.widget_font_size = 25
        self.settings._theme.widget_font_color = GameColors.WHITE.value
        self.settings._theme.widget_alignment = pm.locals.ALIGN_LEFT
        current_res = self.__get_current_resolution_index()
        self.settings.add.dropselect(title="Screen Resolution: ", items=self.resolution, default=current_res, dropselect_id="screen_resolution", selection_box_height=6, open_middle=True)
        self.settings.add.toggle_switch(title="Subtitles", default=self.__settingsconfig.subtitles, toggleswitch_id="subtitles")
        self.settings.add.toggle_switch(title="Debug Mode", default=self.__settingsconfig.debug, toggleswitch_id="debug")
        self.settings.add.toggle_switch(title="Fancy Fonts", default=self.__settingsconfig.fancy_fonts, toggleswitch_id="fancy_fonts")
        self.settings.add.toggle_switch(title="Colorblind Mode (B&W)", default=self.__settingsconfig.grayscale_mode, toggleswitch_id="grayscale_mode")
        self.settings.add.text_input(title="Max FPS: ", default=self.__settingsconfig.max_fps, textinput_id="max_fps", input_type=pm.locals.INPUT_INT, range_values=(30, 144))
        self.settings.add.range_slider(title="Puzzle 1 Difficulty: ", default=int(self.__settingsconfig.puzzle_1_difficulty), range_values=(1, 50), increment=1, rangeslider_id="puzzle_one_diff", value_format=lambda x: str(round(x, None)))
        self.settings.add.range_slider(title="Puzzle 1 Difficutly (Hitbox Timeout)", default=int(self.__settingsconfig.puzzle_1_difficulty_mult), range_values=(600, 1200), increment=1, rangeslider_id="puzzle_one_diff_mult", value_format=lambda x: str(round(x, None)))
        self.settings.add.range_slider(title="Puzzle 1 Difficutly (Player Speed)", default=int(self.__settingsconfig.puzzle_1_difficulty_speed), range_values=(5, 20), increment=1, rangeslider_id="puzzle_one_diff_speed", value_format=lambda x: str(round(x, None)))
        self.settings.add.range_slider(title="Puzzle 2 Difficulty (Speed): ", default=int(self.__settingsconfig.puzzle_2_difficulty_speed), range_values=(1, 50), increment=1, rangeslider_id="puzzle_two_diff_speed", value_format=lambda x: str(round(x, None)))
        self.settings.add.range_slider(title="Puzzle 2 Difficulty (Number): ", default=int(self.__settingsconfig.puzzle_2_difficulty_number), range_values=(1, 50), increment=1, rangeslider_id="puzzle_two_diff_number", value_format=lambda x: str(round(x, None)))
        self.settings.add.button(title="Save Settings and Restart to Apply", action=self.write_game_settings_and_quit, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.add.button(title="Restore Defaults", action=self.write_default_settings_and_quit, font_color=GameColors.WHITE.value, background_color=GameColors.BLACK.value)
        self.settings.mainloop(self.__screen)

    def write_default_settings_and_quit(self):
        """
        Write the default settings and quit
        """
        self.__settingsconfig.write_default_settings()
        self.settings._exit() # pylint: disable=protected-access

    def write_game_settings_and_quit(self):
        """
        Log the game settings
        """
        # getting the data using "get_input_data" method of the Menu class
        screen_width = None
        screen_height = None
        max_fps = None
        puzzle_1_difficulty = None
        puzzle_1_difficulty_mult = None
        puzzle_1_difficulty_speed = None
        puzzle_2_difficulty_speed = None
        puzzle_2_difficulty_number = None
        subtitles = None
        debug = None
        fancy_fonts = None
        grayscale_mode = None
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
                case "fancy_fonts":
                    fancy_fonts = value
                    if fancy_fonts is None:
                        fancy_fonts = self.__settingsconfig.fancy_fonts
                case "grayscale_mode":
                    grayscale_mode = value
                    if grayscale_mode is None:
                        grayscale_mode = self.__settingsconfig.grayscale_mode
                case "debug":
                    debug = value
                    if debug is None:
                        debug = self.__settingsconfig.debug
                case "puzzle_one_diff":
                    puzzle_1_difficulty = int(value)
                    if puzzle_1_difficulty is None:
                        puzzle_1_difficulty = int(self.__settingsconfig.puzzle_1_difficulty)
                case "puzzle_one_diff_mult":
                    puzzle_1_difficulty_mult = int(value)
                    if puzzle_1_difficulty_mult is None:
                        puzzle_1_difficulty_mult = int(self.__settingsconfig.puzzle_1_difficulty_mult)
                case "puzzle_one_diff_speed":
                    puzzle_1_difficulty_speed = int(value)
                    if puzzle_1_difficulty_speed is None:
                        puzzle_1_difficulty_speed = int(self.__settingsconfig.puzzle_1_difficulty_speed)
                case "puzzle_two_diff_speed":
                    puzzle_2_difficulty_speed = int(value)
                    if puzzle_2_difficulty_speed is None:
                        puzzle_2_difficulty_speed = int(self.__settingsconfig.puzzle_2_difficulty_speed)
                case "puzzle_two_diff_number":
                    puzzle_2_difficulty_number = int(value)
                    if puzzle_2_difficulty_number is None:
                        puzzle_2_difficulty_number = int(self.__settingsconfig.puzzle_2_difficulty_number)
                case "max_fps":
                    max_fps = value
                    if int(max_fps) < 30:
                        max_fps = 30
                    if int(max_fps) > 144:
                        max_fps = 144
                    if max_fps is None:
                        max_fps = self.__settingsconfig.max_fps
            self.__glogger.info(f"{key}\t:\t{value}", name=__name__)
            wd = {
                "screen_width": screen_width,
                "screen_height": screen_height,
                "max_fps": max_fps,
                "puzzle_1_difficulty": puzzle_1_difficulty,
                "puzzle_1_difficulty_mult": puzzle_1_difficulty_mult,
                "puzzle_1_difficulty_speed": puzzle_1_difficulty_speed,
                "puzzle_2_difficulty_speed": puzzle_2_difficulty_speed,
                "puzzle_2_difficulty_number": puzzle_2_difficulty_number,
                "subtitles": subtitles,
                "debug": debug,
                "fancy_fonts": fancy_fonts,
                "grayscale_mode": grayscale_mode
            }
            try:
                with open(self.__settingsconfig.config_name, 'w') as settings_file:
                    yaml.dump(wd, settings_file)
            except Exception as e:
                print("Settings failed to write to disk", e)
        self.settings._exit() # pylint: disable=protected-access

    def __get_settings_state_from_disk(self) -> dict:
        """
        Try and load the settings from the disk
        """
        return {
            "screen_width": self.__settingsconfig.screen_width,
            "screen_height": self.__settingsconfig.screen_height,
            "max_fps": self.__settingsconfig.max_fps,
            "puzzle_1_difficulty": self.__settingsconfig.puzzle_1_difficulty,
            "puzzle_1_difficulty_mult": self.__settingsconfig.puzzle_1_difficulty_mult,
            "puzzle_1_difficulty_speed": self.__settingsconfig.puzzle_1_difficulty_speed,
            "puzzle_2_difficulty_speed": self.__settingsconfig.puzzle_2_difficulty_speed,
            "puzzle_2_difficulty_number": self.__settingsconfig.puzzle_2_difficulty_number,
            "subtitles": self.__settingsconfig.subtitles,
            "fancy_fonts": self.__settingsconfig.fancy_fonts,
            "grayscale_mode": self.__settingsconfig.grayscale_mode,
            "debug": self.__settingsconfig.debug
        }

    def __get_current_resolution_index(self) -> int:
        """
        Get the current resolution index
        """
        match self.__settingsconfig.screen_height:
            case 2160:
                return 0
            case 1440:
                return 1
            case 1080:
                return 2
            case 720:
                return 3
            case _:
                return 3
