import random
from typing import Tuple

import pygame

from game_logger import GameLogger
from config import SettingsConfig

def get_intrusive_thoughts_list():
    """
    Get a list of intrusive thoughts
    """
    return [
        "I'm a failure",
        "I can't remember the Doctor's Name",
        "The receptionist will think I'm stupid",
        "I'm not good enough",
        "I didn't go to class yesterday",
        "I bet they think I sound weird",
        "I'm ugly",
        "What will they think of me?",
        "What if my blood test results are bad?",
        "The receptionist will tell the doctor I'm stupid",
        "What if my health insurance doesn't cover this?",
        "I'm afraid of the doctor",
        "Why did I forget to take out the trash yesterday?"
    ]

def get_intrusive_thoughts():
    """
    Get a random intrusive thought
    """
    return random.choice(get_intrusive_thoughts_list())

class GameMapPuzzle2:

    def __init__(self, screen):
        """
        Map class for Game 1
        """
        self.__settings = SettingsConfig()
        self.__cb = "color"
        if self.__settings.grayscale_mode:
            self.__cb = "bw"
        self.visibility = True
        self.image_path = f"assets/backgrounds/puzzle_2/pz2_{self.__cb}_{self.__settings.screen_height}p.png"
        self.map_surface = pygame.image.load(self.image_path)
        self.screen = screen
        self.hitbox_generator = PuzzleHitboxGenerator2(self.screen, self.__settings.puzzle_2_difficulty_number)
        self.draw_hitboxes()

    def draw_map(self):
        """
        Draw map surface on screen
        """
        if self.visibility:
            self.screen.blit(self.map_surface, (0, 0))

    def draw_message_box(self, text: str, screen):
        """
        Draw a static box in the top left corner with text
        """
        box_margin = 20  # Margin from the screen edge
        box_padding = 10  # Padding around the text

        # Render the text
        font = pygame.font.Font(None, 50)  # Choose an appropriate font size
        text_surface = font.render(text, True, (255, 255, 255))  # White text
        text_width, text_height = text_surface.get_size()

        # Calculate box size based on text dimensions
        box_width = text_width + (box_padding * 2)
        box_height = text_height + (box_padding * 2)

        # Create the box rect
        box_rect = pygame.Rect(box_margin, box_margin, box_width, box_height)

        # Draw the box
        pygame.draw.rect(screen, (0, 0, 0), box_rect)  # Black box

        # Calculate text position
        text_rect = text_surface.get_rect(center=box_rect.center)

        # Blit the text onto the screen
        screen.blit(text_surface, text_rect)

    def draw_hitboxes(self):
        """
        Draw hitboxes on screen
        """
        self.hitbox_generator.draw()

    def set_visibility(self, visibility: bool):
        """
        Set map visibility
        """
        self.visibility = visibility

class PuzzleHitbox2:

    def __init__(self, pos, text):
        """
        Puzzle Hitbox
        """
        self.__settings = SettingsConfig()
        self.visibility = True
        self.clickability = False
        self.position = pos
        self.color = (191, 71, 119)
        self.original_color = (191, 71, 119)
        if self.__settings.grayscale_mode:
            self.color = (0, 0, 0)
            self.original_color = (0, 0, 0)
        self.click_time = None
        self.click_duration= 870*self.__settings.puzzle_1_difficulty # milliseconds
        self.is_currently_clicked = False
        self.text = text
        self.rect_size = (160, 80)
        self.velocity = [2, 2]
        self.font_size= 40
        self.am_the_one = False
        self.screen_width = self.__settings.screen_width
        self.screen_height = self.__settings.screen_height
        self.__logger = GameLogger()

    def update_position(self):
        """
        Update the position of the hitbox and bounce off screen edges
        """
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Bounce off left/right edges
        if self.position[0] <= 0 or self.position[0] >= self.screen_width:
            self.velocity[0] *= -1

        # Bounce off top/bottom edges
        if self.position[1] <= 0 or self.position[1] >= self.screen_height:
            self.velocity[1] *= -1

    def update_color(self, screen, color: Tuple[int, int, int]):
        """
        Update the color of the hitbox
        """
        self.color = color
        self.draw(screen, self.color)
        pygame.display.flip()

    def check_click(self, screen, mouse_pos: Tuple[int, int]):
        """
        Check if the hitbox is clicked
        """
        if self.visibility and self.clickability:
            rect = pygame.Rect(
                self.position[0] - self.rect_size[0] // 2,
                self.position[1] - self.rect_size[1] // 2,
                self.rect_size[0],
                self.rect_size[1]
            )
            if rect.collidepoint(mouse_pos):
                current_time = pygame.time.get_ticks()
                self.click_time = current_time
                if not self.am_the_one:  # Only change color if it's not "the one"
                    if self.__settings.grayscale_mode:
                        self.update_color(screen, (255, 255, 255))
                    else:
                        self.update_color(screen, (116, 56, 156))
                self.is_currently_clicked = True
                self.__logger.debug("Click detected", f"PuzzleHitbox2[(x: {self.position[0]}, y: {self.position[1]})]")
                return True
        return False

    def draw(self, screen, color: Tuple[int, int, int] = None):
        """
        Draw the PuzzleHitBox
        """
        if self.visibility:
            current_time = pygame.time.get_ticks()
            if self.click_time:
                if current_time - self.click_time > self.click_duration:
                    self.color = self.original_color
                    self.click_time = None
                    self.is_currently_clicked = False
                else:
                    if self.__settings.grayscale_mode:
                        color = (255, 255, 255)
                    else:
                        color = (116, 56, 156)
            font = pygame.font.Font(None, self.font_size)
            if color is (255, 255, 255):
                text_surface = font.render(self.text, True, (0, 0, 0))
            else:
                text_surface = font.render(self.text, True, (255, 255, 255))
            text_width, text_height = text_surface.get_size()
            padding = 10
            rect_width = max(text_width + padding, self.rect_size[0])
            rect_height = max(text_height + padding, self.rect_size[1])
            rect = pygame.Rect(
                self.position[0] - rect_width // 2,
                self.position[1] - rect_height // 2,
                rect_width,
                rect_height
            )
            pygame.draw.rect(screen, self.color if color is None else color, rect)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def set_visibility(self, visibility: bool):
        """
        Set Hitbox visibility
        """
        self.visibility = visibility

    def set_clickability(self, clickability: bool):
        """
        Set Hitbox clickability
        """
        self.clickability = clickability

class PuzzleHitboxGenerator2:

    def __init__(self, screen, num_hitboxes: int):
        """
        Puzzle Hitbox Generator
        """
        self.__settings = SettingsConfig()
        self.already_drawn = False
        self.visibility = True
        self.clickability = False
        self.hitboxes = []
        self.screen = screen
        self.num_hitboxes = num_hitboxes
        self.create_hitboxes()
        self.already_drawn = True
        if self.already_drawn:
            self.draw()
        self.draw()

    def check_click(self, mouse_pos: Tuple[int, int]):
        """
        Check if any hitbox is clicked
        """
        for hitbox in self.hitboxes:
            if hitbox.check_click(self.screen, mouse_pos):
                hitbox.update_color(self.screen, (0, 252, 0))
                return True
        return False

    def draw(self):
        """
        Draw the PuzzleHitBox
        """
        if self.visibility:
            for hitbox in self.hitboxes:
                hitbox.draw(self.screen)

    def set_clickability(self, clickability: bool):
        """
        Set Hitbox clickability
        """
        self.clickability = clickability
        for hitbox in self.hitboxes:
            hitbox.set_clickability(clickability)

    def set_visibility(self, visibility: bool):
        """
        Set Player visibility
        """
        self.visibility = visibility

    def update_hitbox_positions(self):
        """
        Update the positions of all hitboxes
        """
        for hitbox in self.hitboxes:
            hitbox.update_position()

    def create_hitboxes(self):
        """
        Create hitboxes that do not leave bounds of screen
        """
        screen_width, screen_height = self.__settings.screen_width, self.__settings.screen_height
        hitbox_radius = 40  # Hitboxes are a circle with r=40
        padding = 100  # Minimum space between hitboxes and screen edge
        speed_multiplier = self.__settings.puzzle_2_difficulty_speed

        for _ in range(self.num_hitboxes):
            while True:
                x = random.randint(hitbox_radius, screen_width - hitbox_radius)
                y = random.randint(hitbox_radius, screen_height - hitbox_radius)
                random_thought = get_intrusive_thoughts()
                new_hitbox = PuzzleHitbox2([x, y], random_thought)

                # Randomized velocity with a speed multiplier
                new_hitbox.velocity = [
                    random.choice([-2, -1, 1, 2]) * speed_multiplier,
                    random.choice([-2, -1, 1, 2]) * speed_multiplier
                ]

                if not self.hitbox_overlap(new_hitbox, hitbox_radius + padding):
                    self.hitboxes.append(new_hitbox)
                    break
        if self.hitboxes:
            chosen_one = random.choice(self.hitboxes)
            chosen_one.am_the_one = True
            chosen_one.text = "Dr. Best"

    def is_the_one_clicked(self):
        """
        Check if the hitbox marked as 'the one' is clicked
        """
        for hitbox in self.hitboxes:
            if hitbox.am_the_one and hitbox.is_currently_clicked:
                return True
        return False

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
