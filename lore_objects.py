from save import SaveDataManager

class AbstractLoreObject:

    def __init__(self, name: str | None, lore_text: str | None, location: tuple[int, int] | None, owner: str | None):
        """
        Template for Lore Objects
        """
        self._name = name # Name of the object
        self._lore_text = lore_text # Lore text
        self._location = location # coords
        self._owner = owner # world or player instance

    def get_name(self):
        """Returns the name"""
        return self._name

    def get_lore_text(self):
        """Returns the lore text"""
        return self._lore_text

    def get_location(self):
        """Returns the location"""
        return self._location

    def get_owner(self):
        """Returns the owner"""
        return self._owner

class Prescription_1(AbstractLoreObject):

    def __init__(self):
        """
        Prescription 1
        """
        self.__save_data_manager = SaveDataManager()
        name = "Prescription"
        lore_text = f"""
        CBS PHARMACY
        123 MAIN ST, ANYTOWN USA 12345
        1-800-555-5555

        Patient: {self.__save_data_manager.get_player_name()}
        ESCITALOPRAM 10MG TABLET
        TAKE ONE TABLET BY MOUTH DAILY

        Rx No. 1234567
        Qty. 30
        Dr. Best, MD - 1 Refills
        """
        location = (0, 0)
        owner = "world"
        super().__init__(name, lore_text, location, owner)
