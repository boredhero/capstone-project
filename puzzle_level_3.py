import random
from typing import Set, Tuple, List

import pygame

from game_logger import GameLogger
from config import SettingsConfig

class Maze:

    def __init__(self) -> None:
        """
        Initialize the Maze with a given size
        """
        self.__glogger = GameLogger()
        self.__settings = SettingsConfig()
        self.size = self.__settings.puzzle_3_difficulty_size
        self.maze = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.exit_point = (self.size - 1, self.size - 1)
        self.generate_maze(0, 0)
        #self.print_maze()

    def generate_maze(self, cx: int, cy: int, visited: Set[Tuple[int, int]] = None) -> None:
        """
        Recursively generate the maze starting from (cx, cy)
        """
        self.maze = [[0 for _ in range(self.size)] for _ in range(self.size)]
        stack: List[Tuple[int, int]] = []
        visited: Set[Tuple[int, int]] = set()
        stack.append((cx, cy))
        visited.add((cx, cy))
        while stack:
            cx, cy = stack[-1]
            self.maze[cy][cx] = 1
            neighbors = self.get_unvisited_neighbors(cx, cy, visited)
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.remove_wall(cx, cy, nx, ny)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        self.maze[self.size - 1][self.size - 2] = 1
        self.maze[self.size - 2][self.size - 1] = 1
        self.maze[self.exit_point[1]][self.exit_point[0]] = 1

    def get_unvisited_neighbors(self, x: int, y: int, visited: Set[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Get all unvisited neighbors of a cell
        """
        neighbors = []
        for dx, dy in [(0, -2), (-2, 0), (0, 2), (2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        return neighbors

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Remove the wall between two cells
        """
        wx = (x1 + x2) // 2
        wy = (y1 + y2) // 2
        self.maze[wy][wx] = 1

    def cell_is_valid(self, x: int, y: int, visited: set) -> bool:
        """
        Check if adjacent cells are unvisited to avoid creating loops
        """
        directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        count = 0
        for dx, dy in directions:
            if (x + dx, y + dy) in visited:
                count += 1
        return count == 1

    def print_maze(self):
        """
        Debug Print the maze data
        """
        for row in self.maze:
            self.__glogger.debug(' '.join(str(x) for x in row), name=__name__)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the maze on the Pygame screen
        """
        block_size = min(self.__settings.screen_width // self.size, self.__settings.screen_height // self.size)
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == self.exit_point:
                    color = (0, 255, 0)
                else:
                    color = (255, 255, 255) if self.maze[y][x] == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))

class MazePlayer:

    def __init__(self, start_pos: Tuple[int, int], maze: Maze) -> None:
        """
        Initialize the player for the maze
        """
        self.__glogger = GameLogger()
        self.position = start_pos
        self.maze = maze
        self.speed = 1
        self.__exit_triggered = False

    def has_exit_been_triggered(self) -> bool:
        """
        Check if the player has reached the exit
        """
        return self.__exit_triggered

    def move(self, direction: str) -> None:
        """
        Move the player within the maze checking for wall collisions
        """
        dx, dy = 0, 0
        if direction == "up":
            dy -= self.speed
        elif direction == "down":
            dy += self.speed
        elif direction == "left":
            dx -= self.speed
        elif direction == "right":
            dx += self.speed
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if self.can_move_to(new_x, new_y):
            self.position = (new_x, new_y)
            #self.__glogger.debug(f"Player moved to ({new_x}, {new_y})", name=__name__)
            if self.position == self.maze.exit_point:
                self.__glogger.debug("Player reached the exit!", name=__name__)
                self.__exit_triggered = True

    def can_move_to(self, x: int, y: int) -> bool:
        """
        Check if the new position is within bounds and not a wall
        """
        if 0 <= x < self.maze.size and 0 <= y < self.maze.size:
            if (x, y) == self.maze.exit_point or self.maze.maze[y][x] == 1:
                return True
        return False

    def draw(self, screen: pygame.Surface, block_size: int) -> None:
        """
        Draw the player on the screen
        """
        rect = pygame.Rect(self.position[0] * block_size, self.position[1] * block_size, block_size, block_size)
        pygame.draw.rect(screen, (255, 0, 0), rect)

class MazeGame:

    def __init__(self, screen: pygame.Surface, player: MazePlayer, maze: Maze) -> None:
        """
        Initialize the maze game with player and maze objects
        """
        self.__glogger = GameLogger() # pylint: disable=unused-private-member
        self.__settings = SettingsConfig()
        self.screen = screen
        self.player = player
        self.maze = maze

    def update(self, direction: str) -> None:
        """
        Update the game state by moving the player
        """
        self.player.move(direction)

    def draw(self) -> None:
        """
        Draw the maze and the player.
        """
        self.maze.draw(self.screen)
        block_size = min(self.__settings.screen_width // self.maze.size, self.__settings.screen_height // self.maze.size)
        self.player.draw(self.screen, block_size)
