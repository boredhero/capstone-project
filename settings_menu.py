import pygame_menu as pm

from ui import GameColors
from game_logger import GameLogger

class SettingsMenu:

    def __init__(self):
        """
        SettingsMenu init
        """
        self.__glogger = GameLogger()
        self.resolution = [
            ("3840x2160", "3840x2160"),
            ("2650x1440", "2650x1440"),
            ("1920x1200", "1920x1200"),
            ("1920x1080", "1920x1080"),
            ("1280x720", "1280x720"),
            ("800x600", "800x600")
        ]
        self.settings = pm.Menu(title="Settings",
                                width=700,
                                height=600,
                                theme=pm.themes.THEME_DARK)
        self.settings._theme.widget_font_size = 25
        self.settings._theme.widget_font_color = GameColors.WHITE
        self.settings._theme.widget_alignment = pm.locals.ALIGN_LEFT
        self.settings.add.dropselect_multiple(title="Screen Resolution: ", items=self.resolution, dropselect_id="screen_resolution", open_middle=True, max_selected=1, selection_box_height=6)
        self.settings.add.toggle_switch(title="Subtitles", default=False, toggleswitch_id="subtitles")
        self.settings.add.button(title="Print Settings", action=self.printSettings, font_color=GameColors.WHITE, background_color=GameColors.BLACK)
        self.settings.add.button(title="Restore Defaults", action=self.settings.reset_value, font_color=GameColors.WHITE, background_color=GameColors.BLACK)
        self.settings.add.button(title="Return to Main Menu", action=pm.events.BACK, align=pm.locals.ALIGN_CENTER)

    def printSettings(self):
        """
        Print the settings
        """
        print("\n\n")
        # getting the data using "get_input_data" method of the Menu class
        settingsData = self.settings.get_input_data()
        for key in settingsData.keys():
            self.__glogger(f"{key}\t:\t{settingsData[key]}", name=__name__)
