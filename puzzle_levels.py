import random

import pygame

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
        Moev the Player
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

    def draw(self, screen):
        """
        Draw the PuzzleHitBox
        """
        if self.visibility:
            pygame.draw.circle(screen, (0, 0, 0), self.position, 40)
            pygame.draw.circle(screen, (26, 255, 0), self.position, 30)

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

class PuzzleHitboxGenerator:

    def __init__(self, n_hitboxes: int, screen):
        """
        Puzzle Hitbox Generator
        """
        self.already_drawn = False
        self.visibility = True
        self.hitboxes = []
        self.screen = screen
        for _ in range(n_hitboxes):
            x = random.randint(0, 1000)
            y = random.randint(0, 1000)
            self.hitboxes.append(PuzzleHitbox([x, y]))
        self.already_drawn = True
        if self.already_drawn:
            self.draw()
        self.draw()

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
