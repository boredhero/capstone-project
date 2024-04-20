import time
from typing import Tuple

import pygame
from pygame.locals import * # pylint: disable=wildcard-import,unused-wildcard-import
from PIL import Image

from game_logger import GameLogger
from config import SettingsConfig
from lore_objects import Prescription_1

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
        self.text_screen = None
        self.__cb = "color" # pylint: disable=unused-private-member
        if self.__settings.grayscale_mode:
            self.__cb = "bw" # pylint: disable=unused-private-member
        self.image_path = map_image_path
        self.image = pygame.image.load(self.image_path)
        self.map_surface = pygame.Surface(self.image.get_size(), flags=pygame.HWSURFACE)
        self.map_surface.blit(self.image, (0, 0))
        self.screen_rect = self.screen.get_rect()
        self.camera_rect = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
        self.curr_lore = 0
        self.last_lore_found = self.get_unix_timestamp()
        self.has_player_collided_with_lore = False
        self.current_circle_coords = Prescription_1().get_location()
        self.circle_color = (255, 255, 0)  # Yellow
        self.circle_diameter = 20
        self.dynamic_surface = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA)

    def draw_circle(self):
        """
        Draw the circle on the map at its current coordinates
        """
        circle_radius = self.circle_diameter // 2
        adjusted_x = self.current_circle_coords[0] - self.camera_rect.x
        adjusted_y = self.current_circle_coords[1] - self.camera_rect.y
        if 0 <= adjusted_x <= self.camera_rect.width and 0 <= adjusted_y <= self.camera_rect.height:
            pygame.draw.circle(self.dynamic_surface, self.circle_color, (adjusted_x, adjusted_y), circle_radius)

    def move_circle(self, new_coords: Tuple[int, int]):
        """
        Update the circle's position
        """
        self.current_circle_coords = new_coords

    def get_current_circle_coords (self) -> Tuple[int, int]:
        """
        Get the current circle coordinates
        """
        return self.current_circle_coords

    def set_current_circle_coords (self, coords: Tuple[int, int]):
        """
        Set the current circle coordinates
        """
        self.current_circle_coords = coords

    def check_collision(self):
        """
        Check if the player has collided with the circle
        """
        player_pos = self.player.position
        circle_radius = self.circle_diameter // 2
        circle_rect = pygame.Rect(self.current_circle_coords[0] - circle_radius,
                                  self.current_circle_coords[1] - circle_radius,
                                  self.circle_diameter, self.circle_diameter)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], 40, 40)
        if player_rect.colliderect(circle_rect):
            self.has_player_collided_with_lore = True


    def get_has_player_collided_with_lore(self) -> bool:
        """
        Get whether the player has collided with a lore object
        """
        return self.has_player_collided_with_lore

    def set_has_player_collided_with_lore(self, collided: bool):
        """
        Set whether the player has collided with a lore object
        """
        self.has_player_collided_with_lore = collided

    def handle_event(self, event):
        """
        Close the text screen ONLY if appropriate
        """
        if self.text_screen and self.text_screen.visible:
            if self.text_screen.handle_event(event):
                self.hide_text_screen()
                pygame.display.flip()

    def show_text_screen(self, text: str):
        """
        Show an arbitrary text screen
        """
        if not self.text_screen:
            self.text_screen = TextScreen(self.screen, text)
        else:
            self.text_screen.text = text
        self.text_screen.show()

    def hide_text_screen(self):
        """
        Hide the text screen.
        """
        if self.text_screen:
            self.text_screen.hide()
        self.text_screen = None

    def get_curr_lore(self) -> int:
        """
        Get the current lore object
        """
        return self.curr_lore

    def set_curr_lore(self, lore: int):
        """
        Set the current lore object
        """
        self.curr_lore = lore

    def get_unix_timestamp(self) -> int:
        """
        Get the current Unix timestamp
        """
        return int(time.time())

    def get_last_lore_found(self) -> int:
        """
        Get the last time a lore object was found
        """
        return self.last_lore_found

    def set_last_lore_found(self):
        """
        Set the last time a lore object was found
        """
        self.last_lore_found = self.get_unix_timestamp()

    def draw_map(self):
        """
        Draw map surface on screen
        """
        camera_x = max(0, min(self.player.position[0] - self.screen.get_width() / 2, self.map_surface.get_width() - self.screen.get_width()))
        camera_y = max(0, min(self.player.position[1] - self.screen.get_height() / 2, self.map_surface.get_height() - self.screen.get_height()))
        self.camera_rect = pygame.Rect(camera_x, camera_y, self.screen.get_width(), self.screen.get_height())
        self.screen.blit(self.map_surface, (0, 0), self.camera_rect)
        self.dynamic_surface.fill((0, 0, 0, 0))
        self.draw_circle()
        self.screen.blit(self.dynamic_surface, (0, 0))
        #pygame.display.flip()
        if self.text_screen and self.text_screen.visible:
            self.text_screen.draw()
        if self.has_player_collided_with_lore:
            self.__glogger.info("Collision Detected!", name=__name__)

    def get_pixel_color(self, position: Tuple[int, int]) -> pygame.Color:
        """
        Get the color of the pixel at the given position on the map surface
        """
        return self.map_surface.get_at(position)

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

    def is_move_hitting_color(self, position: Tuple[int, int], game_map: MainGameMap) -> bool:
        """
        Check if the move to the new position is allowed based on the pixel color.
        """
        restricted_color = (255, 255, 255)
        if 0 <= position[0] < game_map.map_surface.get_width() and 0 <= position[1] < game_map.map_surface.get_height():
            pixel_color = game_map.get_pixel_color(position)[:3]  # Get RGB components only
            return pixel_color == restricted_color
        return False

    def move(self, direction, camera_rect, game_map):
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
        color_check_position = (new_position[0] + 30, new_position[1] + 30)
        if self.is_move_hitting_color(color_check_position, game_map):
            return
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

class TextScreen:

    def __init__(self, screen, text, font_size=32, background_color=(0, 0, 0), text_color=(255, 255, 255), text_width=400):
        """
        Minimal text screen for this
        """
        self.__glogger = GameLogger()
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.background_color = background_color
        self.text_color = text_color
        self.text_width = text_width
        self.visible = False
        self.button_text = "Dismiss"
        self.button_font = pygame.font.Font(None, 24)
        self.button = pygame.Rect(0, 0, 100, 40)
        self.button.center = (self.screen.get_width() // 2, self.screen.get_height() - 50)

    def draw(self):
        """
        draw it, wrap the text
        """
        if not self.visible:
            return
        self.screen.fill(self.background_color)
        words = [word.split(' ') for word in self.text.splitlines()]
        space = self.font.size(' ')[0]
        max_width = self.text_width
        x, y = 10, 10
        for line in words:
            for word in line:
                word_surface = self.font.render(word, True, self.text_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = 10
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = 10
            y += word_height
        pygame.draw.rect(self.screen, (200, 200, 200), self.button)  # Draw button rectangle
        button_text_surface = self.button_font.render(self.button_text, True, (0, 0, 0))
        button_text_rect = button_text_surface.get_rect(center=self.button.center)
        self.screen.blit(button_text_surface, button_text_rect)

    def handle_event(self, event):
        """
        handle events
        """
        #self.__glogger.debug(f"Event type: {event.type}", name=__name__)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos):
                self.__glogger.info("Button clicked", name=__name__)
                self.hide()
                return True
        return False

    def show(self):
        """
        show it
        """
        self.visible = True

    def hide(self):
        """
        hide it
        """
        self.__glogger.info("Hiding text screen", name=__name__)
        self.visible = False
        self.__glogger.info(f"Text screen visibility: {self.visible}", name=__name__)
