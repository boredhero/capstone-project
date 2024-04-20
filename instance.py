import time

import pygame

from game_logger import GameLogger
from config import GameConfig, SettingsConfig
import ui
from settings_menu import SettingsMenu, GameInNeedOfReload
from save import SaveDataManager
import main_map
import puzzle_level_1, puzzle_level_2, puzzle_level_3
import text_screen
import lore_objects

class InstanceMain():

    def __init__(self):
        """
        Main class
        """
        self.create_private_static_class_variable_defaults()
        self.__ginr = GameInNeedOfReload()
        self.__config = GameConfig()
        self.__settings = SettingsConfig()
        self.__save_data = SaveDataManager()
        self.init_logger()
        match self.__settings.window_mode:
            case "windowed":
                args = pygame.SCALED | pygame.DOUBLEBUF # pylint: disable=unused-variable
                self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
            case "fullscreen":
                args = pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF # pylint: disable=unused-variable
                self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height), pygame.FULLSCREEN)
            case "borderless":
                args = pygame.SCALED | pygame.NOFRAME | pygame.DOUBLEBUF # pylint: disable=unused-variable
                self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height), pygame.NOFRAME)
            case _:
                args = pygame.SCALED | pygame.DOUBLEBUF # pylint: disable=unused-variable
                self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
        pygame.display.set_caption(f"{self.__config.title} v{self.__config.version}")
        self.__clock = pygame.time.Clock()
        pygame.init()
        pygame.mixer.init()
        self.init_ui()
        self.__glogger.debug(f"PZ3 Diff: {self.__settings.puzzle_3_difficulty_size}")
        self.init_puzzles()
        self.main_game_loop()

    def save_main_game_state(self):
        """
        Save main game state
        """
        self.saved_state = {
            "player_position": self.__player_main_map.position,
            "lore_status": self.__game_map_main.get_curr_lore(),
            "circle_coords": self.__game_map_main.get_current_circle_coords()
        }

    def unload_main_game(self):
        """
        Unload main game
        """
        self.__game_map_main = None
        pygame.mixer.music.stop()

    def load_puzzle(self, puzzle_id):
        """
        Load a puzzle
        """
        if puzzle_id == 1:
            self.__game_map_puzzle_1 = puzzle_level_1.GameMapPuzzle1(self.__screen, self.__player_puzzle_1)
        elif puzzle_id == 2:
            self.__game_map_puzzle_2 = puzzle_level_2.GameMapPuzzle2(self.__screen)
        elif puzzle_id == 3:
            self.__game_map_puzzle_3 = puzzle_level_3.MazeGame(self.__screen, self.__player_puzzle_3, self.__maze)

    def restore_main_game(self):
        """
        Restore main game from freezed state
        """
        main_map_image_path = "assets/backgrounds/main_map.png"
        self.__player_main_map.position = self.saved_state["player_position"]
        self.__game_map_main = main_map.MainGameMap(self.__screen, self.__player_main_map, main_map_image_path)
        self.__game_map_main.set_curr_lore(self.saved_state["lore_status"])
        self.__game_map_main.set_current_circle_coords(self.saved_state["circle_coords"])
        pygame.mixer.music.load("main_theme.mp3")  # Reload main game music
        pygame.mixer.music.play(-1)


    def init_logger(self):
        """
        Initialize Logger
        """
        self.__glogger = GameLogger()
        self.__glogger.log_startup(self.__config.version, self.__config.title)
        self.__glogger.info(f"{self.__settings.max_fps} FPS {self.__settings.screen_width} x {self.__settings.screen_height}", name=__name__)

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
        main_map_image_path = "assets/backgrounds/main_map.png"
        self.__player_puzzle_1 = puzzle_level_1.PlayerPuzzle1([100, 100])  # Player starting position
        self.__player_main_map = main_map.MapPlayer([100, 100], main_map_image_path)
        self.__game_map_puzzle_1 = puzzle_level_1.GameMapPuzzle1(self.__screen, self.__player_puzzle_1)
        self.__game_map_puzzle_2 = puzzle_level_2.GameMapPuzzle2(self.__screen)
        self.__game_map_main = main_map.MainGameMap(self.__screen, self.__player_main_map, main_map_image_path)
        self.__maze = puzzle_level_3.Maze()
        start_pos = (0, 0)
        self.__player_puzzle_3 = puzzle_level_3.MazePlayer(start_pos, self.__maze)
        self.__game_map_puzzle_3 = puzzle_level_3.MazeGame(self.__screen, self.__player_puzzle_3, self.__maze)

    def create_private_static_class_variable_defaults(self):
        """
        Create private class variable defaults
        """
        self.__running = True
        self.__playing = False
        self.__playing_puzzle_1 = False
        self.__playing_puzzle_2 = False
        self.__playing_puzzle_3 = False
        self.__intro_screen = None
        self.__controls_screen = None
        self.__text_screen_1 = None
        self.__text_screen_2 = None
        self.__credits = None
        self.__mla_works_cited = None
        self.__show_intro_screen = False
        self.__show_controls_screen = False
        self.__show_text_screen_1 = False
        self.__show_text_screen_2 = False
        self.__show_text_screen_3 = False
        self.__show_credits = False
        self.__show_mla_works_cited = False
        self.__playing_map_music = False
        self.__playing_puzzle_1_music = False
        self.__playing_puzzle_2_music = False
        self.__playing_puzzle_3_music = False
        self.lore_conditions_init()

    def has_been_x_time_since_utx(self, utx: int, x_mins: int | None = None, x_secs: int | None = None) -> bool:
        """
        Has it been at least X minutes OR X seconds since the given unix timestamp? 
        """
        current_timestamp = time.time()
        if x_mins is None and x_secs is None:
            self.__glogger.warning("No time specified", name=__name__)
            return False
        if x_mins is not None and x_secs is not None:
            self.__glogger.warning("Both minutes and seconds specified, defaulting to minutes", name=__name__)
        if x_mins is not None:
            target_timestamp = utx + x_mins * 60
            ret = current_timestamp >= target_timestamp
            if ret is True:
                self.__glogger.info(f"I was called (mins), returning {ret}", name=__name__)
            return ret
        if x_secs is not None:
            target_timestamp = utx + x_secs
            ret = current_timestamp >= target_timestamp
            if ret is True:
                self.__glogger.info(f"I was called (secs), returning {ret}", name=__name__)
            return ret

    def lore_conditions_init(self):
        """
        Initialize lore conditions
        """
        # This is really ugly, I know, but I'm out of time and I have other classes I need to pass to graduate this semester too :/
        self.lore_1 = lore_objects.Prescription_1()
        self.lore_2 = lore_objects.Journal_Entry_1()
        self.lore_3 = lore_objects.Journal_Entry_2()
        self.lore_4 = lore_objects.Journal_Entry_3()
        self.lore_5 = lore_objects.Journal_Entry_4()
        self.lore_6 = lore_objects.Puzzle_1_Shim()
        self.lore_7 = lore_objects.HospitalWristBand()
        self.lore_8 = lore_objects.Prescription_2()
        self.lore_9 = lore_objects.Journal_Entry_5()
        self.lore_10 = lore_objects.Journal_Entry_6()
        self.lore_11 = lore_objects.Journal_Entry_7()
        self.lore_12 = lore_objects.Journal_Entry_8()
        self.lore_13 = lore_objects.Journal_Entry_9()
        self.lore_14 = lore_objects.Journal_Entry_10()
        self.lore_15 = lore_objects.Journal_Entry_11()
        self.__displayed_all_lore = False

    def handle_display_lore_actually(self, event): # pylint: disable=unused-argument
        """
        Actually handle displaying the lore
        """
        if self.__playing is True:
            curr_lore = self.__game_map_main.get_curr_lore()
            if self.__game_map_main.get_has_player_collided_with_lore():
                match curr_lore:
                    case 0:
                        self.__glogger.info("Lore 1 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_1.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_2.get_location())
                    case 1:
                        self.__glogger.info("Lore 2 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_2.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_3.get_location())
                    case 2:
                        self.__glogger.info("Lore 3 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_3.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_4.get_location())
                    case 3:
                        self.__glogger.info("Lore 4 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_4.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_5.get_location())
                    case 4:
                        self.__glogger.info("Lore 5 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_5.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_6.get_location())
                    case 5:
                        self.__glogger.info("Puzzle 1 shim found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_6.get_lore_text())
                        self.__playing = False # Puzzle 1
                        self.__playing_map_music = False
                        self.__playing_puzzle_1 = True
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_7.get_location())
                    case 5:
                        self.__glogger.info("Lore 7 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_7.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_8.get_location())
                    case 6:
                        self.__glogger.info("Lore 8 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_8.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_9.get_location())
                    case 7:
                        self.__glogger.info("Lore 9 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_9.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_10.get_location())
                    case 8:
                        self.__glogger.info("Lore 10 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_10.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_11.get_location())
                    case 9:
                        self.__glogger.info("Lore 11 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_11.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_12.get_location())
                    case 10:
                        self.__glogger.info("Lore 12 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_12.get_lore_text())
                        # TODO: Start Puzzle 2
                        self.__playing = False
                        self.__playing_map_music = False
                        self.__playing_puzzle_2 = True
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_13.get_location())
                    case 11:
                        self.__glogger.info("Lore 13 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_13.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_14.get_location())
                    case 12:
                        self.__glogger.info("Lore 14 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_14.get_lore_text())
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle(self.lore_15.get_location())
                    case 13:
                        self.__glogger.info("Lore 15 found", name=__name__)
                        self.__game_map_main.show_text_screen(self.lore_15.get_lore_text())
                        # TODO: Start Puzzle 3
                        self.__playing = False
                        self.__playing_map_music = False
                        self.__playing_puzzle_3 = True
                        self.__game_map_main.set_has_player_collided_with_lore(False)
                        self.__game_map_main.move_circle((8000, 8000))
                    case _:
                        if self.__displayed_all_lore is False:
                            self.__displayed_all_lore = True
                            self.__glogger.debug("No more lore to display", name=__name__)
                self.__game_map_main.set_last_lore_found()
                self.__game_map_main.set_curr_lore(curr_lore+1)

    def main_game_loop(self):
        """
        Main game loop
        """
        while self.__running:
            if self.__ginr.needs_reload:
                self.__settings.refresh_from_disk()
                self.__ginr.set_needs_reload(False)
                match self.__settings.window_mode:
                    case "windowed":
                        args = pygame.SCALED | pygame.DOUBLEBUF # pylint: disable=unused-variable
                        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
                    case "fullscreen":
                        args = pygame.SCALED | pygame.FULLSCREEN | pygame.DOUBLEBUF # pylint: disable=unused-variable
                        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height), pygame.FULLSCREEN)
                    case "borderless":
                        args = pygame.SCALED | pygame.NOFRAME | pygame.DOUBLEBUF # pylint: disable=unused-variable
                        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height), pygame.NOFRAME)
                    case _:
                        args = pygame.SCALED | pygame.DOUBLEBUF # pylint: disable=unused-variable
                        self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
                #self.__screen = pygame.display.set_mode((self.__settings.screen_width, self.__settings.screen_height))
                self.__init__() # pylint: disable=non-parent-init-called, unnecessary-dunder-call
            mouse_up = False
            for event in pygame.event.get():
                if self.__playing:
                    #self.__glogger.info("hiiii", name=__name__)
                    #self.__glogger.info(f"event: {event}", name=__name__)
                    self.__game_map_main.handle_event(event)
                    pygame.display.flip()
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
                        if self.__playing_puzzle_3:
                            self.puzzle_3_return_to_main_menu()
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
                                if self.__save_data.get_player_name() is None:
                                    self.show_name_input_screen()
                                    self.__titlescreen_ui.set_visibility(False)
                                    self.__show_intro_screen = True
                                    self.__intro_screen = text_screen.TextScreen(self.__screen, text_screen.get_main_game_intro_text(), "Continue")
                                    self.__intro_screen.draw()
                                    self.__controls_screen = text_screen.TextScreen(self.__screen, text_screen.get_main_game_controls_text(), "Continue")
                                else:
                                    self.__titlescreen_ui.set_visibility(False)
                                    self.__playing = True
                                    self.__screen.fill((0, 0, 0))
                            case ui.GameState.CREDITS:
                                self.__titlescreen_ui.set_visibility(False)
                                self.__show_credits = True
                                self.__credits = text_screen.TextScreen(self.__screen, text_screen.get_credits_and_attributions_text(), "Back")
                                self.__credits.draw()
                            case ui.GameState.MLA_WORKS_CITED:
                                self.__titlescreen_ui.set_visibility(False)
                                self.__show_mla_works_cited = True
                                self.__mla_works_cited = text_screen.TextScreen(self.__screen, text_screen.get_mla_works_cited(), "Back")
                                self.__mla_works_cited.draw()
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
                            case ui.GameState.PLAY_PUZZLE_3:
                                self.__show_text_screen_3 = True
                                self.__debug_play_puzzles_ui.set_visibility(False)
                                self.__text_screen_3 = text_screen.TextScreen(self.__screen, text_screen.get_puzzle_3_intro_text(), "Continue")
                                self.__text_screen_3.draw()
                if self.__show_intro_screen:
                    self.__intro_screen.draw()
                    if self.__intro_screen.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__show_intro_screen = False
                        self.__show_controls_screen = True
                if self.__show_controls_screen:
                    self.__controls_screen.draw()
                    if self.__controls_screen.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__show_controls_screen = False
                        self.__save_data.set_shown_intro_and_controls(True)
                        self.__playing = True
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
                if self.__show_text_screen_3:
                    self.__text_screen_3.draw()
                    if self.__text_screen_3.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__show_text_screen_3 = False
                        self.__playing_puzzle_3 = True
                if self.__show_credits:
                    self.__credits.draw()
                    if self.__credits.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__titlescreen_ui.set_visibility(True)
                        self.__show_credits = False
                if self.__show_mla_works_cited:
                    self.__mla_works_cited.draw()
                    if self.__mla_works_cited.handle_event(event): # pylint: disable=undefined-loop-variable
                        self.__titlescreen_ui.set_visibility(True)
                        self.__show_mla_works_cited = False
                mouse_up = False
            self.handle_display_lore_actually(event) # pylint: disable=undefined-loop-variable
            if self.__playing and not self.__playing_map_music:
                pygame.mixer.music.load("assets/music/gymnopedie_no_1.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.__playing_map_music = True
            if self.__playing_puzzle_1 and not self.__playing_puzzle_1_music:
                pygame.mixer.music.load("assets/music/chopin_prelude_op_28_no_4.ogg")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.__playing_puzzle_1_music = True
            if self.__playing_puzzle_2 and not self.__playing_puzzle_2_music:
                pygame.mixer.music.load("assets/music/violin_partita_no_2_in_d_minor_bwv_1004.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.__playing_puzzle_2_music = True
            if self.__playing_puzzle_3 and not self.__playing_puzzle_3_music:
                pygame.mixer.music.load("assets/music/IMSLP77318-PMLP07506-gnossiennes_1.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
                self.__playing_puzzle_3_music = True
            if self.__playing:
                keys = pygame.key.get_pressed()
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_up)]:
                    self.__player_main_map.move("up", self.__game_map_main.camera_rect, self.__game_map_main)
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_down)]:
                    self.__player_main_map.move("down", self.__game_map_main.camera_rect, self.__game_map_main)
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_left)]:
                    self.__player_main_map.move("left", self.__game_map_main.camera_rect, self.__game_map_main)
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_right)]:
                    self.__player_main_map.move("right", self.__game_map_main.camera_rect, self.__game_map_main)
                self.__game_map_main.draw_map()
                self.__game_map_main.check_collision()
                self.__player_main_map.draw(self.__screen, self.__game_map_main.camera_rect)
                pygame.display.flip()
            if self.__playing_puzzle_1:
                keys = pygame.key.get_pressed()
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_up)]:
                    self.__player_puzzle_1.move("up")
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_down)]:
                    self.__player_puzzle_1.move("down")
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_left)]:
                    self.__player_puzzle_1.move("left")
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_right)]:
                    self.__player_puzzle_1.move("right")
                if keys[pygame.K_n]:
                    self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()
                if self.__game_map_puzzle_1.all_hitboxes_collided():
                    #self.puzzle_1_return_to_main_menu()
                    self.puzzle_1_return_to_main_map()
                self.__game_map_puzzle_1.draw_map()
                self.__game_map_puzzle_1.hitbox_generator.set_collidability(True)
                self.__game_map_puzzle_1.draw_hitboxes()
                self.__player_puzzle_1.draw(self.__screen)
                pygame.display.flip()
            if self.__playing_puzzle_2:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_n]:
                    self.__game_map_puzzle_2.hitbox_generator.reset_hitboxes()
                self.__game_map_puzzle_2.hitbox_generator.update_hitbox_positions()
                self.__game_map_puzzle_2.draw_map()
                self.__game_map_puzzle_2.draw_hitboxes()
                self.__game_map_puzzle_2.draw_message_box("What is your doctor's name so I can schedule an appointment?", self.__screen)
                self.__game_map_puzzle_2.hitbox_generator.set_clickability(True)
                if self.__game_map_puzzle_2.hitbox_generator.is_the_one_clicked():
                    self.puzzle_2_return_to_main_map()
                pygame.display.flip()
            if self.__playing_puzzle_3:
                keys = pygame.key.get_pressed()
                if keys[self.get_pygame_key_for_key(self.__settings.keybind_up)]:
                    self.__game_map_puzzle_3.update("up")
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_down)]:
                    self.__game_map_puzzle_3.update("down")
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_left)]:
                    self.__game_map_puzzle_3.update("left")
                elif keys[self.get_pygame_key_for_key(self.__settings.keybind_right)]:
                    self.__game_map_puzzle_3.update("right")
                self.__screen.fill((0, 0, 0))
                self.__game_map_puzzle_3.draw()
                if self.__player_puzzle_3.has_exit_been_triggered():
                    self.puzzle_3_return_to_main_menu()
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
        self.__playing = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_main.set_visibility(False)
        self.__titlescreen_ui.set_visibility(True)
        self.__playing_map_music = False # pylint: disable=attribute-defined-outside-init
        pygame.mixer.music.stop()

    def puzzle_1_return_to_main_menu(self):
        """
        Return to the main menu
        """# pylint: disable=attribute-defined-outside-init
        self.__playing_puzzle_1 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_1.hitbox_generator.set_collidability(False)
        self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()
        self.__titlescreen_ui.set_visibility(True)
        self.__playing_puzzle_1_music = False # pylint: disable=attribute-defined-outside-init
        pygame.mixer.music.stop()

    def puzzle_1_return_to_main_map(self):
        """
        Return to the main map from puzzle 1
        """# pylint: disable=attribute-defined-outside-init
        self.__playing_puzzle_1 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_1.hitbox_generator.set_collidability(False)
        self.__game_map_puzzle_1.hitbox_generator.reset_hitboxes()
        self.__playing_puzzle_1_music = False # pylint: disable=attribute-defined-outside-init
        pygame.mixer.music.stop()
        self.__playing = True

    def puzzle_2_return_to_main_menu(self):
        """
        Return to the main menu
        """
        self.__playing_puzzle_2 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_2.hitbox_generator.set_clickability(False)
        self.__game_map_puzzle_2.hitbox_generator.reset_hitboxes()
        self.__titlescreen_ui.set_visibility(True)
        self.__playing_puzzle_2_music = False # pylint: disable=attribute-defined-outside-init
        pygame.mixer.music.stop()

    def puzzle_2_return_to_main_map(self):
        """
        Return to the main map from puzzle 2
        """
        self.__playing_puzzle_2 = False # pylint: disable=attribute-defined-outside-init
        self.__game_map_puzzle_2.hitbox_generator.set_clickability(False)
        self.__game_map_puzzle_2.hitbox_generator.reset_hitboxes()
        self.__playing_puzzle_2_music = False # pylint: disable=attribute-defined-outside-init
        pygame.mixer.music.stop()
        self.__playing = True

    def puzzle_3_return_to_main_menu(self):
        """
        Return to the main menu from puzzle 3
        """
        self.__playing_puzzle_3 = False # pylint: disable=attribute-defined-outside-init
        self.__titlescreen_ui.set_visibility(True)
        self.__playing_puzzle_3_music = False # pylint: disable=attribute-defined-outside-init
        self.__maze = puzzle_level_3.Maze()
        start_pos = (0, 0)
        self.__player_puzzle_3 = puzzle_level_3.MazePlayer(start_pos, self.__maze)
        self.__game_map_puzzle_3 = puzzle_level_3.MazeGame(self.__screen, self.__player_puzzle_3, self.__maze)
        pygame.mixer.music.stop()

    def puzzle_3_return_to_main_map(self):
        """
        Return to the main map from puzzle 3
        """
        self.__playing_puzzle_3 = False # pylint: disable=attribute-defined-outside-init
        self.__playing_puzzle_3_music = False # pylint: disable=attribute-defined-outside-init
        self.__maze = puzzle_level_3.Maze()
        start_pos = (0, 0)
        self.__player_puzzle_3 = puzzle_level_3.MazePlayer(start_pos, self.__maze)
        self.__game_map_puzzle_3 = puzzle_level_3.MazeGame(self.__screen, self.__player_puzzle_3, self.__maze)
        pygame.mixer.music.stop()
        self.__playing = True

    def check_playing_anything(self):
        """
        Check if playing anything
        """
        return self.__playing or self.__playing_puzzle_1 or self.__playing_puzzle_2

    def show_name_input_screen(self):
        """
        Show the name input
        """
        input_active = True
        player_name = ""
        input_box = pygame.Rect(100, 150, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        font = pygame.font.Font(None, 32)
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = not input_active
                    else:
                        input_active = False
                    color = color_active if input_active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            self.__save_data.set_player_name(player_name)
                            return
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        else:
                            player_name += event.unicode
            self.__screen.fill((30, 30, 30))
            instruction_text = "Please enter a player name and press Enter to continue"
            txt_instruction = font.render(instruction_text, True, pygame.Color('white'))
            self.__screen.blit(txt_instruction, (100, 100))  # Adjust position as needed
            txt_surface = font.render(player_name, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.__screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.__screen, color, input_box, 2)
            pygame.display.flip()
            self.__clock.tick(30)
        self.__show_intro_screen = True # pylint: disable=attribute-defined-outside-init
        self.__titlescreen_ui.set_visibility(False)

    def get_pygame_key_for_key(self, key: str):
        """
        Match the string name of a key with pygame's key constants
        """
        key_map = {
            "space": pygame.K_SPACE,
            "q": pygame.K_q,
            "w": pygame.K_w,
            "e": pygame.K_e,
            "r": pygame.K_r,
            "t": pygame.K_t,
            "y": pygame.K_y,
            "u": pygame.K_u,
            "i": pygame.K_i,
            "o": pygame.K_o,
            "p": pygame.K_p,
            "a": pygame.K_a,
            "s": pygame.K_s,
            "d": pygame.K_d,
            "f": pygame.K_f,
            "g": pygame.K_g,
            "h": pygame.K_h,
            "j": pygame.K_j,
            "k": pygame.K_k,
            "l": pygame.K_l,
            "z": pygame.K_z,
            "x": pygame.K_x,
            "c": pygame.K_c,
            "v": pygame.K_v,
            "b": pygame.K_b,
            "n": pygame.K_n,
            "m": pygame.K_m,
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "left shift": pygame.K_LSHIFT,
            "right shift": pygame.K_RSHIFT,
            "left ctrl": pygame.K_LCTRL,
            "right ctrl": pygame.K_RCTRL,
            "left alt": pygame.K_LALT,
            "right alt": pygame.K_RALT,
            "tab": pygame.K_TAB,
            "backspace": pygame.K_BACKSPACE,
            "return": pygame.K_RETURN,
            "escape": pygame.K_ESCAPE,
            "insert": pygame.K_INSERT,
            "delete": pygame.K_DELETE,
            "home": pygame.K_HOME,
            "end": pygame.K_END,
            "page up": pygame.K_PAGEUP,
            "page down": pygame.K_PAGEDOWN,
            "print screen": pygame.K_PRINTSCREEN,
            "scroll lock": pygame.K_SCROLLLOCK,
            "pause": pygame.K_PAUSE,
            "f1": pygame.K_F1,
            "f2": pygame.K_F2,
            "f3": pygame.K_F3,
            "f4": pygame.K_F4,
            "f5": pygame.K_F5,
            "f6": pygame.K_F6,
            "f7": pygame.K_F7,
            "f8": pygame.K_F8,
            "f9": pygame.K_F9,
            "f10": pygame.K_F10,
            "f11": pygame.K_F11,
            "f12": pygame.K_F12,
            "f13": pygame.K_F13,
            "f14": pygame.K_F14,
            "f15": pygame.K_F15,
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3,
            "4": pygame.K_4,
            "5": pygame.K_5,
            "6": pygame.K_6,
            "7": pygame.K_7,
            "8": pygame.K_8,
            "9": pygame.K_9,
            "0": pygame.K_0,
            "-": pygame.K_MINUS,
            "=": pygame.K_EQUALS,
            "[": pygame.K_LEFTBRACKET,
            "]": pygame.K_RIGHTBRACKET,
            ";": pygame.K_SEMICOLON,
            "'": pygame.K_QUOTE,
            "/": pygame.K_SLASH,
            "\\": pygame.K_BACKSLASH,
            ",": pygame.K_COMMA,
            ".": pygame.K_PERIOD,
            "`": pygame.K_BACKQUOTE
        }
        return key_map.get(key.lower(), None)

    def graceful_exit(self):
        """
        Gracefully quit the program
        """
        pygame.quit()
        exit(0)

if __name__ == "__main__":
    InstanceMain()
