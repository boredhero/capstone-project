import pygame

from game_logger import GameLogger
from config import GameConfig, SettingsConfig
import ui
from settings_menu import SettingsMenu, GameInNeedOfReload
import puzzle_level_1
import puzzle_level_2
import text_screen

class InstanceMainLoop:

    def __init__(self):
        """
        Main Loop. Must call loop() to run the loop!!!
        """
        self.__ginr = GameInNeedOfReload()
        self.__glogger = GameLogger() # pylint: disable=unused-private-member
        self.__config = GameConfig()
        self.__settings = SettingsConfig()
        self.create_private_static_class_variable_defaults()
        self.pygame_init()
        self.init_ui()
        self.init_puzzles()

    def loop(self):
        """
        Call me to activate the main loop
        """
        while self.__running:
            self.__main_loop()
        self.graceful_exit()

    def __main_loop(self):
        """
        Meaty bit of the main loop
        """
        self.__ml_handle_ginr() # Handle the game needing a reload
        self.__ml_event_handler() # Handle game events
        if not self.check_playing_anything(): # If we're not playing anything, draw the titlescreen
            self.__ml_handle_ui_if_not_playing() # Handle drawing various UI screens
        self.__handle_show_text_screens() # If we need to display a text screen right now, display that
        if self.__playing: # Play button
            self.__puzzle_1_logic()
        if self.__playing_puzzle_1: # Debug Puzzle Menu option 1
            self.__puzzle_1_logic()
        if self.__playing_puzzle_2: # Debug puzzle menu option 2
            self.__puzzle_2_logic()
        pygame.display.flip() # Necessary for UI to update
        self.__clock.tick(self.__settings.max_fps) # Set the FPS and tick the clock at the end of each loop

    def __ml_handle_ginr(self):
        """
        Handle reloading the game if we need to do that
        """
        if self.__ginr.needs_reload:
            self.__settings.refresh_from_disk()
            self.__ginr.set_needs_reload(False)
            self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
            self.__init__() # pylint: disable=non-parent-init-called, unnecessary-dunder-call

    def __ml_event_handler(self):
        """
        Event handler main loop
        """
        self.__mouse_up = False
        for event in pygame.event.get():
            self.__current_event = event
            if event.type == pygame.QUIT:
                self.__running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.__mouse_up = True
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

    def __handle_titlescreen_ui_action(self, ui_action):
        """
        Handle UI action events from the title screen
        """
        match ui_action:
            case ui.GameState.EXIT:
                self.graceful_exit()
            case ui.GameState.SETTINGS:
                self.__gamesettings = SettingsMenu(self.__screen) # pylint: disable=unused-private-member
            case ui.GameState.PLAY:
                self.__titlescreen_ui.set_visibility(False)
                self.__playing = True
                self.__screen.fill((0, 0, 0))
            case ui.GameState.CREDITS:
                self.__titlescreen_ui.set_visibility(False)
                self.__show_credits = True
                self.__credits = text_screen.TextScreen(self.__screen, text_screen.get_credits_and_attributions_text(), "Back")
                self.__credits.draw()
            case ui.GameState.DEBUG_PLAY_PUZZLE:
                self.__titlescreen_ui.set_visibility(False)
                self.__debug_play_puzzles_ui.set_visibility(True)
            case _:
                pass

    def __handle_level_selector_ui_action(self, ui_action):
        """
        Handle UI Action events from the level selector
        """
        match ui_action:
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

    def __handle_show_text_screens(self):
        """
        Display any text screens, if conditions are correct for them to spawn
        """
        if self.__show_text_screen_1:
            self.__text_screen_1.draw()
            if self.__text_screen_1.handle_event(self.__current_event): # pylint: disable=undefined-loop-variable
                self.__show_text_screen_1 = False
                self.__playing_puzzle_1 = True
        if self.__show_text_screen_2:
            self.__text_screen_2.draw()
            if self.__text_screen_2.handle_event(self.__current_event): # pylint: disable=undefined-loop-variable
                self.__show_text_screen_2 = False
                self.__playing_puzzle_2 = True
        if self.__show_credits:
            self.__credits.draw()
            if self.__credits.handle_event(self.__current_event): # pylint: disable=undefined-loop-variable
                self.__titlescreen_ui.set_visibility(True)
                self.__show_credits = False
        self.__mouse_up = False

    def __blackfill_screen(self):
        """
        Hello darkness my old friend, I've come to talk with you again
        """
        self.__screen.fill("black")

    def __handle_game_keyboard_input_puzzle_1(self):
        """
        Handle WASD, Arrow Keys, and N for resetting the hitboxes for Puzzle 1
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.__player_puzzle_1.move("up")
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.__player_puzzle_1.move("down")
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.__player_puzzle_1.move("left")
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.__player_puzzle_1.move("right")
        if keys[pygame.K_n]:
            self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()

    def __puzzle_1_logic(self):
        """
        Logic for puzzle 1
        """
        self.__handle_game_keyboard_input_puzzle_1()
        if self.__game_map_puzzle_1.all_hitboxes_collided():
            self.puzzle_1_return_to_main_menu()
        self.__game_map_puzzle_1.draw_map()
        self.__game_map_puzzle_1.hitbox_generator.set_collidability(True)
        self.__game_map_puzzle_1.draw_hitboxes()
        self.__player_puzzle_1.draw(self.__screen)
        pygame.display.flip()

    def __puzzle_2_logic(self):
        """
        Logic for puzzle 2
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_n]:
            self.__game_map_puzzle_2.hitbox_generator.reset_hitboxes()
        self.__game_map_puzzle_2.hitbox_generator.update_hitbox_positions()
        self.__game_map_puzzle_2.draw_map()
        self.__game_map_puzzle_2.draw_hitboxes()
        self.__game_map_puzzle_2.draw_message_box("What is your doctor's name so I can schedule an appointment?", self.__screen)
        self.__game_map_puzzle_2.hitbox_generator.set_clickability(True)
        if self.__game_map_puzzle_2.hitbox_generator.is_the_one_clicked():
            self.puzzle_2_return_to_main_menu()
        pygame.display.flip()

    def __ml_handle_ui_if_not_playing(self):
        """
        If we aren't playing anything, we wanna do titlescreen stuff
        """
        self.__blackfill_screen()
        if self.__titlescreen_ui.visibility:
            titlescreen_ui_action = self.__titlescreen_ui.update(pygame.mouse.get_pos(), self.__mouse_up)
            if titlescreen_ui_action is not None:
                self.__handle_titlescreen_ui_action(titlescreen_ui_action)
        if self.__debug_play_puzzles_ui.visibility:
            level_selector_ui_action = self.__debug_play_puzzles_ui.update(pygame.mouse.get_pos(), self.__mouse_up)
            if level_selector_ui_action is not None:
                self.__handle_level_selector_ui_action(level_selector_ui_action)
        self.__titlescreen_ui.draw(self.__screen)
        if self.__debug_play_puzzles_ui.visibility:
            self.__debug_play_puzzles_ui.draw(self.__screen)

    def pygame_init(self):
        """
        Screen, caption, clock, and pygame.init()
        """
        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height)) # Set the window dimensions
        pygame.display.set_caption(f"{self.__config.title} v{self.__config.version}")
        self.__clock = pygame.time.Clock()
        pygame.init()

    def init_ui(self):
        """
        Initialize UI
        """
        self.__titlescreen_ui = ui.TitleScreenUIElements()
        self.__debug_play_puzzles_ui = ui.LevelSelectorUIElements()

    def init_puzzles(self):
        """
        Initialize puzzles
        """
        self.__player_puzzle_1 = puzzle_level_1.PlayerPuzzle1([100, 100])  # Player starting position
        self.__game_map_puzzle_1 = puzzle_level_1.GameMapPuzzle1(self.__screen, self.__player_puzzle_1)
        self.__game_map_puzzle_2 = puzzle_level_2.GameMapPuzzle2(self.__screen)

    def create_private_static_class_variable_defaults(self):
        """
        Create private class variable defaults
        """
        self.__mouse_up = False
        self.__current_event = None
        self.__running = True
        self.__playing = False
        self.__playing_puzzle_1 = False
        self.__playing_puzzle_2 = False
        self.__text_screen_1 = None
        self.__text_screen_2 = None
        self.__credits = None
        self.__show_text_screen_1 = False
        self.__show_text_screen_2 = False
        self.__show_credits = False

    def graceful_exit(self):
        """
        Gracefully quit the program
        """
        pygame.quit()
        exit(0)

    def check_playing_anything(self):
        """
        Check if playing anything
        """
        return self.__playing or self.__playing_puzzle_1 or self.__playing_puzzle_2

    def return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_1.hitbox_generator.set_collidability(False)
        self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()
        self.__titlescreen_ui.set_visibility(True)

    def puzzle_1_return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing_puzzle_1 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_1.hitbox_generator.set_collidability(False)
        self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()
        self.__titlescreen_ui.set_visibility(True)

    def puzzle_2_return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing_puzzle_2 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_2.hitbox_generator.set_clickability(False)
        self.__game_map_puzzle_2.hitbox_generator.reset_hitboxes()
        self.__titlescreen_ui.set_visibility(True)

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
