from typing import Tuple

import pygame
from PIL import Image

from game_logger import GameLogger
from config import SettingsConfig

class MainGameMap:

    def __init__(self, screen, player, map_image_path: str):
        """
        Main Game Map Class
        """
        self.__settings = SettingsConfig()
        self.__glogger = GameLogger() # pylint: disable=unused-private-member
        self.visibility = True
        self.screen = screen
        self.player = player
        self.__cb = "color" # pylint: disable=unused-private-member
        if self.__settings.grayscale_mode:
            self.__cb = "bw" # pylint: disable=unused-private-member
        # TODO: Add the full map image
        self.image_path = map_image_path
        self.image = pygame.image.load(self.image_path)
        self.map_surface = pygame.Surface(self.image.get_size(), flags=pygame.HWSURFACE)
        self.map_surface.blit(self.image, (0, 0))
        self.screen_rect = self.screen.get_rect()
        self.camera_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())

    def draw_map(self):
        """
        Draw map surface on screen
        """
        camera_x = max(0, min(self.player.position[0] - self.screen.get_width() / 2, self.map_surface.get_width() - self.screen.get_width()))
        camera_y = max(0, min(self.player.position[1] - self.screen.get_height() / 2, self.map_surface.get_height() - self.screen.get_height()))
        self.camera_rect = pygame.Rect(camera_x, camera_y, self.screen.get_width(), self.screen.get_height())
        self.screen.blit(self.map_surface, (0, 0), self.camera_rect)

    def set_visibility(self, visibility: bool):
        """
        Set map visibility
        """
        self.visibility = visibility

class MapPlayer:


    def __init__(self, start_pos: Tuple, map_image_path: str):
        """
        Player class for the main map
        """
        self.__settings = SettingsConfig()
        self.__glogger = GameLogger()
        self.visibility = True
        self.position = start_pos
        self.map_size = self.get_image_dimensions(map_image_path)
        self.__glogger.info(f"Map size: {self.map_size}", name=__name__)
        self.speed = self.__settings.puzzle_1_difficulty_speed*self.__settings.screen_size_speed_multiplier

    def get_image_dimensions(self, image_path: str):
        """
        Get the dimensions of an image
        """
        with Image.open(image_path) as img:
            width, height = img.size
        return (width, height)

    def move(self, direction, camera_rect):
        """
        Move the Player
        """
        new_position = list(self.position)
        if direction == "up":
            new_position[1] -= self.speed
        elif direction == "down":
            new_position[1] += self.speed
        elif direction == "left":
            new_position[0] -= self.speed
        elif direction == "right":
            new_position[0] += self.speed
        new_position[0] = max(0, min(new_position[0], self.map_size[0] - 40))
        new_position[1] = max(0, min(new_position[1], self.map_size[1] - 40))
        within_camera_x_bounds = camera_rect.left <= new_position[0] <= camera_rect.right - 40
        within_camera_y_bounds = camera_rect.top <= new_position[1] <= camera_rect.bottom - 40
        if within_camera_x_bounds and within_camera_y_bounds:
            self.position = tuple(new_position)

    def draw(self, screen, camera_rect):
        """
        Draw the Player
        """
        if self.visibility:
            screen_x = self.position[0] - camera_rect.left
            screen_y = self.position[1] - camera_rect.top
            pygame.draw.rect(screen, (255, 255, 255), (screen_x, screen_y, 40, 40)) # Placeholder for a sprite

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility
