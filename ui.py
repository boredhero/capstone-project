from typing import Tuple, Any
from enum import Enum

import pygame
import pygame.font
from pygame.sprite import Sprite
from pygame.rect import Rect # pylint: disable=unused-import

from misc import GameColors

class GameState(Enum):
    EXIT = -1
    SETTINGS = 0
    PLAY = 1

def create_surface_with_text(text: str, font_size: int, text_rgb: Tuple, bg_rgb: Tuple):
    """
    Create a surface with text on it
    """
    # https://programmingpixels.com/handling-a-title-screen-game-flow-and-buttons-in-pygame.html
    pygame.font.init()
    font = pygame.font.Font('fonts/porter-sans/porter-sans-inline-block.ttf', font_size)
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
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """
        Draw a surface element
        """
        surface.blit(self.image, self.rect)

class TitleScreenUIElements():
    """
    Title Screen UI Elements
    """

    def __init__(self):
        """
        Title Screen UI Elements init
        """
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
        self.__load_button = UIElement(
            center_position=(500, 450),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Load Saved Game"
        )
        self.__settings_button = UIElement(
            center_position=(500, 500),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Settings",
            action=GameState.SETTINGS
        )
        self.__quit_button = UIElement(
            center_position=(500, 550),
            font_size=30,
            bg_rgb=GameColors.BLACK.value,
            text_rgb=GameColors.WHITE.value,
            text="Exit",
            action=GameState.EXIT
        )
        self.__buttons = [self.__start_button, self.__load_button, self.__settings_button, self.__quit_button]

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
