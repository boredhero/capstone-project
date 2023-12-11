import pygame

from game_logger import GameLogger
from config import GameConfig, SettingsConfig
import ui
from settings_menu import SettingsMenu
import puzzle_level_1
import puzzle_level_2
import text_screen

class InstanceMain():

    def __init__(self):
        """
        Main class
        """
        self.__glogger = GameLogger()
        self.__config = GameConfig()
        self.__settings = SettingsConfig()
        self.__glogger.log_startup(self.__config.version, self.__config.title)
        self.__glogger.info(f"{self.__settings.max_fps} FPS {self.__settings.screen_width} x {self.__settings.screen_height}", name=__name__)
        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height)) # Set the window dimensions
        pygame.display.set_caption(f"{self.__config.title} v{self.__config.version}")
        self.__clock = pygame.time.Clock()
        self.__running = True
        self.__playing = False
        self.__playing_puzzle_1 = False
        self.__playing_puzzle_2 = False
        self.__text_screen_1 = None
        self.__text_screen_1 = None
        self.__show_text_screen_1 = False
        self.__show_text_screen_2 = False
        pygame.init()
        self.__titlescreen_ui = ui.TitleScreenUIElements()
        self.__debug_play_puzzles_ui = ui.LevelSelectorUIElements()
        self.__player_puzzle_1 = puzzle_level_1.PlayerPuzzle1([100, 100])  # Player starting position
        self.__player_puzzle_2 = puzzle_level_2.PlayerPuzzle2([100, 100])  # Player starting position
        self.__game_map_puzzle_1 = puzzle_level_1.GameMapPuzzle1("assets/backgrounds/missing_texture.png", self.__screen, self.__player_puzzle_1)
        self.__game_map_puzzle_2 = puzzle_level_2.GameMapPuzzle2("assets/backgrounds/missing_texture.png", self.__screen, self.__player_puzzle_2)
        while self.__running:
            mouse_up = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_up = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.__playing:
                            self.return_to_main_menu()
                        if self.__playing_puzzle_1:
                            self.puzzle_1_return_to_main_menu()
                        if self.__playing_puzzle_2:
                            self.puzzle_2_return_to_main_menu()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    self.__game_map_puzzle_2.hitbox_generator.check_click(mouse_pos)
            if not self.check_playing_anything():
                self.__screen.fill("black")
                if self.__titlescreen_ui.visibility:
                    ui_action = self.__titlescreen_ui.update(pygame.mouse.get_pos(), mouse_up)
                    if ui_action is not None:
                        match ui_action:
                            case ui.GameState.EXIT:
                                self.graceful_exit()
                            case ui.GameState.SETTINGS:
                                self.__gamesettings = SettingsMenu(self.__screen) # pylint: disable=unused-private-member
                            case ui.GameState.PLAY:
                                self.__titlescreen_ui.set_visibility(False)
                                self.__playing = True
                                self.__screen.fill((0, 0, 0))
                            case ui.GameState.DEBUG_PLAY_PUZZLE:
                                self.__titlescreen_ui.set_visibility(False)
                                self.__debug_play_puzzles_ui.set_visibility(True)
                            case _:
                                pass
                if self.__debug_play_puzzles_ui.visibility:
                    ui_action_levels = self.__debug_play_puzzles_ui.update(pygame.mouse.get_pos(), mouse_up)
                    if ui_action_levels is not None:
                        match ui_action_levels:
                            case ui.GameState.PLAY_PUZZLE_1:
                                self.__show_text_screen_1 = True
                                self.__debug_play_puzzles_ui.set_visibility(False)
                                self.__text_screen_1 = text_screen.TextScreen(self.__screen, text_screen.get_puzzle_1_intro_text(), "Continue")
                                self.__text_screen_1.draw()
                            case ui.GameState.PLAY_PUZZLE_2:
                                self.__show_text_screen_2 = True
                                self.__debug_play_puzzles_ui.set_visibility(False)
                                self.__text_screen_2 = text_screen.TextScreen(self.__screen, text_screen.get_puzzle_2_intro_text(), "Continue")
                                self.__text_screen_2.draw()
                if self.__show_text_screen_1:
                    self.__text_screen_1.draw()
                    if self.__text_screen_1.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__show_text_screen_1 = False
                        self.__playing_puzzle_1 = True
                if self.__show_text_screen_2:
                    self.__text_screen_2.draw()
                    if self.__text_screen_2.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__show_text_screen_2 = False
                        self.__playing_puzzle_2 = True
                mouse_up = False
            if self.__playing:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.__player_puzzle_1.move("up")
                if keys[pygame.K_s]:
                    self.__player_puzzle_1.move("down")
                if keys[pygame.K_a]:
                    self.__player_puzzle_1.move("left")
                if keys[pygame.K_d]:
                    self.__player_puzzle_1.move("right")
                if self.__game_map_puzzle_1.all_hitboxes_collided():
                    self.return_to_main_menu()
                self.__game_map_puzzle_1.draw_map()
                self.__game_map_puzzle_1.draw_hitboxes()
                self.__player_puzzle_1.draw(self.__screen)
                pygame.display.flip()
            if self.__playing_puzzle_1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.__player_puzzle_1.move("up")
                if keys[pygame.K_s]:
                    self.__player_puzzle_1.move("down")
                if keys[pygame.K_a]:
                    self.__player_puzzle_1.move("left")
                if keys[pygame.K_d]:
                    self.__player_puzzle_1.move("right")
                if self.__game_map_puzzle_1.all_hitboxes_collided():
                    self.puzzle_1_return_to_main_menu()
                self.__game_map_puzzle_1.draw_map()
                self.__game_map_puzzle_1.draw_hitboxes()
                self.__player_puzzle_1.draw(self.__screen)
                pygame.display.flip()
            if self.__playing_puzzle_2:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    self.__player_puzzle_2.move("up")
                if keys[pygame.K_s]:
                    self.__player_puzzle_2.move("down")
                if keys[pygame.K_a]:
                    self.__player_puzzle_2.move("left")
                if keys[pygame.K_d]:
                    self.__player_puzzle_2.move("right")
                if self.__game_map_puzzle_2.all_hitboxes_collided():
                    self.puzzle_2_return_to_main_menu()
                self.__game_map_puzzle_2.hitbox_generator.update_hitbox_positions()
                self.__game_map_puzzle_2.draw_map()
                self.__game_map_puzzle_2.draw_hitboxes()
                self.__player_puzzle_2.draw(self.__screen)
                pygame.display.flip()
            self.__titlescreen_ui.draw(self.__screen)
            if self.__debug_play_puzzles_ui.visibility:
                self.__debug_play_puzzles_ui.draw(self.__screen)
            pygame.display.flip()
            self.__clock.tick(self.__settings.max_fps) # Set the FPS
        self.graceful_exit()

    def get_screen(self):
        """
        Get the screen
        """
        return self.__screen

    def get_clock(self):
        """
        Get the clock
        """
        return self.__clock

    def return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing = False
        self.__titlescreen_ui.set_visibility(True)

    def puzzle_1_return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing_puzzle_1 = False
        self.__titlescreen_ui.set_visibility(True)

    def puzzle_2_return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing_puzzle_2 = False
        self.__titlescreen_ui.set_visibility(True)

    def check_playing_anything(self):
        """
        Check if playing anything
        """
        return self.__playing or self.__playing_puzzle_1 or self.__playing_puzzle_2

    def graceful_exit(self):
        """
        Gracefully quit the program
        """
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    InstanceMain()
