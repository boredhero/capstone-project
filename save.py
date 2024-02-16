import os

import yaml

from misc import Singleton

class SaveDataManager(metaclass=Singleton):

    def __init__(self):
        """
        SaveFile Manager
        """
        self.save_name = "save.yml"
        self.__save_contents = {}
        self.__load_save()
        self.__player_name = self.__save_contents.get("player_name")
        if self.__player_name == "None":
            self.__player_name = None
        self.__player_x = self.__save_contents.get("player_x")
        self.__player_y = self.__save_contents.get("player_y")

    def get_player_name(self):
        """
        Get the player name
        """
        return self.__player_name

    def set_player_name(self, name: str):
        """
        Set the player name
        """
        self.__save_contents["player_name"] = name
        self.__write_save_yml_file(self.__save_contents)
        self.__player_name = name

    def get_player_x(self):
        """
        Get the player x coordinate
        """
        return self.__player_x

    def set_player_x(self, x: int):
        """
        Set the player x coordinate
        """
        self.__save_contents["player_x"] = x
        self.__write_save_yml_file(self.__save_contents)
        self.__player_x = x

    def get_player_y(self):
        """
        Get the player y coordinate
        """
        return self.__player_y

    def set_player_y(self, y: int):
        """
        Set the player y coordinate
        """
        self.__save_contents["player_y"] = y
        self.__write_save_yml_file(self.__save_contents)
        self.__player_y = y

    def __load_save(self):
        """
        Load save file from disk, create if it does not exist
        """
        exists = os.path.isfile(self.save_name)
        if exists is True:
            try:
                with open(self.save_name, 'r') as save_file:
                    self.__save_contents = yaml.unsafe_load(save_file) # pylint: disable=no-value-for-parameter
            except Exception as e:
                print("Save file failed to load initially, creating a new one", e)
                self.__save_contents = self.get_default_save()
        else:
            try:
                with open(self.save_name, 'w') as save_file:
                    yaml.dump(self.get_default_save(), save_file)
                    self.__save_contents = self.get_default_save()
            except Exception as e:
                print("Save file failed to load on write, using defaults", e)
                self.__save_contents = self.get_default_save()

    def get_save_refresh(self):
        """
        Get the save after reloading the file from disk (slower)
        """
        self.__load_save()
        return self.__save_contents

    def get_save_no_refresh(self):
        """
        Get the save immediately without reloading the file from disk (faster)
        """
        return self.__save_contents

    def get_default_save(self):
        """
        Default save to write if no config exists somehow
        """
        return {
            "player_name": "None",
            "player_x": 0,
            "player_y": 0
        }

    def __write_save_yml_file(self, contents: dict | None = None):
        """
        Write save file to disc
        NOTE: If contents are None, the default save will be written to disk
        """
        if contents is None:
            contents = self.get_default_save()
        try:
            with open(self.save_name, 'w') as save_file:
                yaml.dump(contents, save_file)
        except Exception as e:
            print("Save file failed to write to disk", e)
        self.refresh_from_disk()

    def write_default_save(self):
        """
        Write default save file to disk
        """
        self.__write_save_yml_file()

    def refresh_from_disk(self):
        """
        Re-Run __init__ on this Singleton class, thus changing the values to match those on disk
        """
        self.__init__() # pylint: disable=unnecessary-dunder-call
