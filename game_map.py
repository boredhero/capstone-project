import pygame
import puzzle_levels

class GameMap:

    def __init__(self, image_path: str, screen, player):
        """
        Basic Map Class
        """
        self.visibility = True
        self.map_surface = pygame.image.load(image_path)
        self.screen = screen
        self.player = player
        self.hitbox_generator = puzzle_levels.PuzzleHitboxGenerator(self.screen, 10)
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
