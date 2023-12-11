from typing import Tuple, Any
from enum import Enum

import pygame
import pygame.font
from pygame.sprite import Sprite
from pygame.rect import Rect # pylint: disable=unused-import

from config import SettingsConfig
from misc import GameColors, Singleton

class GameState(Enum):
    EXIT = -1
    SETTINGS = 0
    PLAY = 1
    LOAD_SAVE = 2
    CREDITS = 3
    DEBUG_PLAY_PUZZLE = 4
    PLAY_PUZZLE_1 = 5
    PLAY_PUZZLE_2 = 6

class CurrentGameState(metaclass=Singleton):
    """
    Current Game State
    """

    def __init__(self):
        """
        Current Game State constructor
        """
        self.__game_state = GameState.SETTINGS

    @property
    def game_state(self):
        """
        Game State Property
        """
        return self.__game_state

    @game_state.setter
    def game_state(self, game_state: GameState):
        """
        Game State Setter
        """
        self.__game_state = game_state

def create_surface_with_text(text: str, font_size: int, text_rgb: Tuple, bg_rgb: Tuple):
    """
    Create a surface with text on it
    """
    # https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    settings = SettingsConfig()
    pygame.font.init()
    if settings.fancy_fonts:
        font = pygame.font.Font('fonts/porter-sans/porter-sans-inline-block.ttf', font_size)
    else:
        font = pygame.font.SysFont("Arial", font_size)
    surface = font.render(text, True, text_rgb, bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """
    User Interface Element that can be added to a surface
    """

    def __init__(self, center_position: Tuple, text: str, font_size: int, bg_rgb: Tuple, text_rgb: Tuple, action: Any = None):
        """
        UIElement init
        """
        self.visible = True
        self.mouse_over = False
        default_img = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_img = create_surface_with_text(text, font_size+2, text_rgb, bg_rgb)
        self.images = [default_img, highlighted_img]
        self.rects = [default_img.get_rect(center=center_position), highlighted_img.get_rect(center=center_position)]
        self.action = action
        super().__init__()

    @property
    def image(self):
        """
        Image Property
        """
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        """
        Rect Property
        """
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos: Tuple, mouse_up: bool): # pylint: disable=arguments-differ
        """
        Update the mouse position mouse_over variable
        """
        if self.visible:
            if self.rect.collidepoint(mouse_pos):
                self.mouse_over = True
                if mouse_up:
                    return self.action
            else:
                self.mouse_over = False
        else:
            self.mouse_over = False

    def set_visibility(self, visibility: bool):
        """
        Toggle visibility of the UIElement
        """
        self.visible = visibility

    def draw(self, surface):
        """
        Draw a surface element
        """
        if self.visible:
            surface.blit(self.image, self.rect)

class LevelSelectorUIElements():
    """
    Level Selector UI Elements
    """

    def __init__(self):
        """
        Level selector UI elements constructor
        """
        self.__settings = SettingsConfig()
        screen_height = self.__settings.screen_height
        screen_width = self.__settings.screen_width
        title_y = screen_height // 3
        puzzle_1_y = title_y + 100  # Adjust as needed
        puzzle_2_y = puzzle_1_y + 50  # Adjust as needed
        self.visibility = None
        self.__title = UIElement(
            center_position=(screen_width // 2, title_y),
            font_size=60,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Select a Level"
        )
        self.__puzzle_1 = UIElement(
            center_position=(screen_width // 2, puzzle_1_y),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Puzzle 1 (Depression - Motivation)",
            action=GameState.PLAY_PUZZLE_1
        )
        self.__puzzle_2 = UIElement(
            center_position=(screen_width // 2, puzzle_2_y),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Puzzle 2 (Social Anxiety - Intrusive Thoughts)",
            action=GameState.PLAY_PUZZLE_2
        )
        self.__buttons = [self.__puzzle_1, self.__puzzle_2]

    @property
    def buttons(self):
        """
        Buttons Property
        """
        return self.__buttons

    @property
    def title(self):
        """
        Title Property
        """
        return self.__title

    def update(self, mouse_pos: Tuple, mouse_up: bool):
        """
        Update the mouse position mouse_over variable
        """
        for button in self.__buttons:
            action = button.update(mouse_pos, mouse_up)
            if action is not None:
                return action
        return None

    def draw(self, surface):
        """
        Draw a surface element
        """
        for button in self.__buttons:
            button.draw(surface)
        self.__title.draw(surface)

    def set_visibility(self, visibility: bool):
        """
        Toggle visibility of the UIElement
        """
        self.visibility = visibility
        for button in self.__buttons:
            button.set_visibility(visibility)
        self.__title.set_visibility(visibility)

class TitleScreenUIElements():
    """
    Title Screen UI Elements
    """

    def __init__(self):
        """
        Title Screen UI Elements constructor
        """
        self.visibility = True
        self.__settings = SettingsConfig()
        self.__quit_button_y_pos = 550
        if self.__settings.debug:
            self.__quit_button_y_pos = 600
        self.__title = UIElement(
            center_position=(500, 300),
            font_size=60,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Instance"
        )
        self.__start_button = UIElement(
            center_position=(500, 400),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Play",
            action=GameState.PLAY
        )
        #self.__load_button = UIElement(
        #    center_position=(500, 450),
        #    font_size=30,
        #    bg_rgb=GameColors.BLACK.value,
        #    text_rgb=GameColors.WHITE.value,
        #    text="Load Saved Game",
        #    action=GameState.LOAD_SAVE
        #)
        self.__settings_button = UIElement(
            center_position=(500, 450),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Settings",
            action=GameState.SETTINGS
        )
        self.__credits_button = UIElement(
            center_position=(500, 500),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Credits & Attributions",
            action=GameState.CREDITS
        )
        if self.__settings.debug:
            self.__debug_play_puzzle_button = UIElement(
                center_position=(500, 550),
                font_size=30,
                bg_rgb=GameColors.BLACK.value,
                text_rgb=GameColors.WHITE.value,
                text="Debug Play Puzzle",
                action=GameState.DEBUG_PLAY_PUZZLE
            )
        self.__quit_button = UIElement(
            center_position=(500, self.__quit_button_y_pos),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Exit",
            action=GameState.EXIT
        )
        if self.__settings.debug:
            self.__buttons = [self.__start_button, self.__settings_button, self.__credits_button, self.__debug_play_puzzle_button, self.__quit_button]
        else:
            self.__buttons = [self.__start_button, self.__settings_button, self.__credits_button, self.__quit_button]

    @property
    def buttons(self):
        """
        Buttons Property
        """
        return self.__buttons

    @property
    def title(self):
        """
        Title Property
        """
        return self.__title

    def update(self, mouse_pos: Tuple, mouse_up: bool):
        """
        Update the mouse position mouse_over variable
        """
        for button in self.__buttons:
            action = button.update(mouse_pos, mouse_up)
            if action is not None:
                return action
        return None

    def draw(self, surface):
        """
        Draw a surface element
        """
        for button in self.__buttons:
            button.draw(surface)
        self.__title.draw(surface)

    def set_visibility(self, visibility: bool):
        """
        Toggle visibility of the UIElement
        """
        self.visibility = visibility
        for button in self.__buttons:
            button.set_visibility(visibility)
        self.__title.set_visibility(visibility)
