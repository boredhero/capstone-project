import os, sys, subprocess, time #pylint: disable=unused-import

def main():
    """
    Had to run it somehow lol
    """
    BuildManager()

class BuildManager:

    def __init__(self):
        """
        Class to automatically detect our platform and build the appropriate executable
        """
        self.system = "Unknown"
        if sys.platform.startswith("win"):
            self.system = "Windows"
        elif sys.platform.startswith("darwin"):
            self.system = "Mac OS"
        elif sys.platform.startswith("linux"):
            self.system = "Linux"
        print(f"Detected platform: {self.system}")
        print("NOTE: Due to limitations with cross-platform compilation in python (not at all supported),\n you can only build for the platform you are currently on.\n If you want to build for another platform, you will need to do so on that platform.")
        print(f"Proceeding with {self.system} build in 5 seconds...")
        time.sleep(5)
        self.build()

    def get_user_input(self, prompt: str) -> str:
        """
        Get user input
        """
        return input(prompt)

    def build(self):
        """
        Build the game executable
        """
        assets_path = 'assets' + (';' if self.system == 'Windows' else ':') + '.'
        match self.system:
            case "Windows":
                subprocess.run(["pyinstaller", "--onefile", "--windowed", "--add-data", assets_path, "instance.py"], check=True)
            case "Mac OS":
                subprocess.run(["pyinstaller", "--onefile", "--windowed", "--add-data", assets_path, "instance.py"], check=True)
            case "Linux":
                subprocess.run(["pyinstaller", "--onefile", "--add-data", assets_path, "instance.py"], check=True)
            case _:
                print(f"Unknown platform: {self.system}")
                sys.exit(1)
        print("Build complete. Find your build in the 'dist' folder.")
        time.sleep(5)
        sys.exit(0)

if __name__ == "__main__":
    main()
