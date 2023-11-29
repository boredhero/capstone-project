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
        self.speed = 5

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

    def __init__(self, n_hitboxes: int):
        """
        Puzzle Hitbox Generator
        """
        self.visibility = True
        self.hitboxes = []
        for _ in range(n_hitboxes):
            self.hitboxes.append(PuzzleHitbox([100, 100]))
            
