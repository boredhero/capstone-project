import random
from typing import Tuple

import pygame

from game_logger import GameLogger
from config import SettingsConfig

class GameMap:

    def __init__(self, image_path: str, screen):
        """
        Basic Map Class
        """
        self.visibility = True
        self.map_surface = pygame.image.load(image_path)
        self.screen = screen

    def draw_map(self):
        """
        Draw map surface on screen
        """
        if self.visibility:
            self.screen.blit(self.map_surface, (0, 0))

    def set_visibility(self, visibility: bool):
        """
        Set map visibility
        """
        self.visibility = visibility

class Player:

    def __init__(self, start_pos):
        """
        Basic Player Class
        """
        self.visibility = True
        self.position = start_pos
        self.speed = 1

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

class PuzzleHitbox:

    def __init__(self, pos):
        """
        Puzzle Hitbox
        """
        self.visibility = True
        self.position = pos
        self.color = (252, 0, 0)
        self.original_color = (252, 0, 0)
        self.collision_time = None
        self.collision_duration = 8000 # milliseconds
        self.is_currently_collided = False
        self.__logger = GameLogger()

    def update_color(self, screen, color: Tuple[int, int, int]):
        """
        Update the color of the hitbox
        """
        self.color = color
        self.draw(screen, self.color)
        pygame.display.flip()

    def check_collision(self, screen, player: Player):
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
            pygame.draw.circle(screen, (0, 0, 0), self.position, 40)
            pygame.draw.circle(screen, final_color, self.position, 30)

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

class PuzzleHitboxGenerator:

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

    def check_collision(self, player: Player):
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
        padding = 20  # Minimum space between hitboxes and screen edge
        for _ in range(self.num_hitboxes):
            while True:
                x = random.randint(hitbox_radius, screen_width - hitbox_radius)
                y = random.randint(hitbox_radius, screen_height - hitbox_radius)
                new_hitbox = PuzzleHitbox([x, y])
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
