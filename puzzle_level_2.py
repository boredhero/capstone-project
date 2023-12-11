import random
from typing import Tuple

import pygame

from game_logger import GameLogger
from config import SettingsConfig

class GameMapPuzzle2:

    def __init__(self, image_path: str, screen, player):
        """
        Map class for Game 1
        """
        self.__settings = SettingsConfig()
        self.visibility = True
        self.map_surface = pygame.image.load(image_path)
        self.screen = screen
        self.player = player
        self.hitbox_generator = PuzzleHitboxGenerator2(self.screen, self.__settings.puzzle_1_difficulty)
        self.draw_hitboxes()

    def draw_map(self):
        """
        Draw map surface on screen
        """
        if self.visibility:
            self.screen.blit(self.map_surface, (0, 0))

    def all_hitboxes_collided(self):
        """
        Check if all hitboxes are currently collided
        """
        return self.hitbox_generator.check_all_collided()

    def draw_hitboxes(self):
        """
        Draw hitboxes on screen
        """
        self.hitbox_generator.check_collision(self.player)
        self.hitbox_generator.draw()

    def set_visibility(self, visibility: bool):
        """
        Set map visibility
        """
        self.visibility = visibility

class PlayerPuzzle2:

    def __init__(self, start_pos):
        """
        Basic Player Class
        """
        self.visibility = True
        self.position = start_pos
        self.speed = 7

    def move(self, direction):
        """
        Move the Player
        """
        match direction:
            case "up":
                self.position[1] -= self.speed
            case "down":
                self.position[1] += self.speed
            case "left":
                self.position[0] -= self.speed
            case "right":
                self.position[0] += self.speed

    def draw(self, screen):
        """
        Draw the Player
        """
        if self.visibility:
            pygame.draw.rect(screen, (255, 255, 255), (*self.position, 40, 40)) # Placeholder for a sprite

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

class PuzzleHitbox2:

    def __init__(self, pos, text):
        """
        Puzzle Hitbox
        """
        self.__settings = SettingsConfig()
        self.visibility = True
        self.position = pos
        self.color = (252, 0, 0)
        self.original_color = (252, 0, 0)
        self.collision_time = None
        self.collision_duration= 870*self.__settings.puzzle_1_difficulty # milliseconds
        self.is_currently_collided = False
        self.text = text
        self.rect_size = (80, 40)
        self.__logger = GameLogger()

    def update_color(self, screen, color: Tuple[int, int, int]):
        """
        Update the color of the hitbox
        """
        self.color = color
        self.draw(screen, self.color)
        pygame.display.flip()

    def check_collision(self, screen, player: PlayerPuzzle2):
        """
        Check if player collides with hitbox
        """
        if self.visibility:
            # Check for collision with the player
            if (player.position[0] >= self.position[0] - 40 and
                player.position[0] <= self.position[0] + 40 and
                player.position[1] >= self.position[1] - 40 and
                player.position[1] <= self.position[1] + 40):

                # Collision detected, update color and record collision time
                self.collision_time = pygame.time.get_ticks()
                self.update_color(screen, (0, 252, 0))
                if self.is_currently_collided is False:
                    self.__logger.debug("Collision detected", f"PuzzleHitbox[(x: {self.position[0]}, y: {self.position[1]})]")
                self.is_currently_collided = True
                return True
        return False

    def draw(self, screen, color: Tuple[int, int, int] = None):
        """
        Draw the PuzzleHitBox
        """
        if self.visibility:
            current_time = pygame.time.get_ticks()

            # Check if the hitbox needs to revert back to its original color
            if self.collision_time:
                if current_time - self.collision_time > self.collision_duration:
                    self.color = self.original_color  # Revert to original color
                    self.collision_time = None
                    self.is_currently_collided = False
                else:
                    color = (0, 252, 0)  # Keep the color green

            # Use the current color if a specific color is not provided
            final_color = self.color if color is None else color

            # Draw the rectangle
            rect = pygame.Rect(
                self.position[0] - self.rect_size[0] // 2,
                self.position[1] - self.rect_size[1] // 2,
                self.rect_size[0],
                self.rect_size[1]
            )
            pygame.draw.rect(screen, final_color, rect)

            # Draw the text
            font = pygame.font.Font(None, 24)  # Choose an appropriate font size
            text_surface = font.render(self.text, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

class PuzzleHitboxGenerator2:

    def __init__(self, screen, num_hitboxes: int):
        """
        Puzzle Hitbox Generator
        """
        self.__settings = SettingsConfig()
        self.already_drawn = False
        self.visibility = True
        self.hitboxes = []
        self.screen = screen
        self.num_hitboxes = num_hitboxes
        # Keep above
        self.create_hitboxes()
        # Keep below
        self.already_drawn = True
        if self.already_drawn:
            self.draw()
        self.draw()

    def check_collision(self, player: PlayerPuzzle2):
        """
        Check if player collides with hitbox
        """
        for hitbox in self.hitboxes:
            if hitbox.check_collision(self.screen, player):
                hitbox.update_color(self.screen, (0, 252, 0))
                return True
        return False

    def check_all_collided(self):
        """
        Check if all hitboxes are collided
        """
        return all(hitbox.is_currently_collided for hitbox in self.hitboxes)

    def draw(self):
        """
        Draw the PuzzleHitBox
        """
        if self.visibility:
            for hitbox in self.hitboxes:
                hitbox.draw(self.screen)

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

    def create_hitboxes(self):
        """
        Create hitboxes that do not leave bounds of screen!
        """
        screen_width, screen_height = self.__settings.screen_width, self.__settings.screen_height
        hitbox_radius = 40  # Hitboxes are a cicle with r=40
        padding = 100  # Minimum space between hitboxes and screen edge
        for _ in range(self.num_hitboxes):
            while True:
                x = random.randint(hitbox_radius, screen_width - hitbox_radius)
                y = random.randint(hitbox_radius, screen_height - hitbox_radius)
                new_hitbox = PuzzleHitbox2([x, y], "test")
                if not self.hitbox_overlap(new_hitbox, hitbox_radius + padding):
                    self.hitboxes.append(new_hitbox)
                    break

    def hitbox_overlap(self, new_hitbox, min_distance):
        """
        Check if a hitbox overlaps with existing hitboxes 
        """
        for hitbox in self.hitboxes:
            dx = hitbox.position[0] - new_hitbox.position[0]
            dy = hitbox.position[1] - new_hitbox.position[1]
            distance = (dx**2 + dy**2)**0.5
            if distance < min_distance:
                return True
        return False
