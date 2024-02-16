import pygame

from game_logger import GameLogger
from config import GameConfig, SettingsConfig
import ui
from settings_menu import SettingsMenu, GameInNeedOfReload
from save import SaveDataManager
import puzzle_level_1
import puzzle_level_2
import text_screen

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
        self.init_ui()
        self.init_puzzles()
        self.main_game_loop()

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
        self.__player_puzzle_1 = puzzle_level_1.PlayerPuzzle1([100, 100])  # Player starting position
        self.__game_map_puzzle_1 = puzzle_level_1.GameMapPuzzle1(self.__screen, self.__player_puzzle_1)
        self.__game_map_puzzle_2 = puzzle_level_2.GameMapPuzzle2(self.__screen)

    def create_private_static_class_variable_defaults(self):
        """
        Create private class variable defaults
        """
        self.__running = True
        self.__playing = False
        self.__playing_puzzle_1 = False
        self.__playing_puzzle_2 = False
        self.__text_screen_1 = None
        self.__text_screen_2 = None
        self.__credits = None
        self.__mla_works_cited = None
        self.__show_text_screen_1 = False
        self.__show_text_screen_2 = False
        self.__show_credits = False
        self.__show_mla_works_cited = False

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
                                if self.__save_data.get_player_name() is None:
                                    self.show_name_input_screen()
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
            if self.__playing:
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
                    self.return_to_main_menu()
                self.__game_map_puzzle_1.draw_map()
                self.__game_map_puzzle_1.hitbox_generator.set_collidability(True)
                self.__game_map_puzzle_1.draw_hitboxes()
                self.__player_puzzle_1.draw(self.__screen)
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
                    self.puzzle_1_return_to_main_menu()
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
                    self.puzzle_2_return_to_main_menu()
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
