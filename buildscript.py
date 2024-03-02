import os, platform, subprocess # pylint: disable=unused-import
from pathlib import Path

class PackageBuilder:

    def __init__(self):
        """
        Automated build script to build a package for your current platform
        NOTE: It is technologically impossible to build for windows from linux, or vice versa
        """
        self.__linux_build_path = "dist/instance"
        self.__platform = self.__get_platform()
        match self.__platform:
            case "Linux":
                self.__linux_distribution = self.__get_linux_distribution()
                self.handle_linux()
            case "Windows":
                self.handle_windows()
            case "Darwin":
                self.handle_mac_os()
            case _:
                print(f"Unsupported platform: {self.__platform}")
                exit(1)

    def handle_mac_os(self):
        """
        Handle Mac OS
        NOTE: Not supported yet because I don't have a Mac to test with
        """
        print("Mac OS is not supported yet; I lack a system to test with")

    def handle_windows(self):
        """
        Handle Windows
        NOTE: Not supported yet because I don't have a Windows system to test with
        """
        print("Windows is not supported yet; I lack a system to test with")

    def handle_linux(self):
        """
        Handle Linux
        """
        supported_distributions = ["Arch"]
        if self.__linux_distribution not in supported_distributions:
            print(f"Unsupported distribution: {self.__linux_distribution}")
            print(f"Supported distributions at this time are: {supported_distributions}")
            exit(1)
        print(f"Building package for {self.__linux_distribution}")
        match self.__linux_distribution:
            case "Arch":
                self.__build_package_arch_linux()
            case _:
                print(f"Unsupported distribution: {self.__linux_distribution}")
                exit(1)

    def __build_package_arch_linux(self):
        """
        Build the package for arch linux
        """
        answer = input(f"Would you like to build Instance for {self.__linux_distribution} (make sure you have read the README.md and ran pipenv install on your system first!) [yes/no]: ")
        if answer.lower() == "yes":
            self.__run_pyinstaller()
            instance_exists = self.__check_file_exists(self.__linux_build_path)
            if instance_exists:
                subprocess.run(["cp" f"{self.__linux_build_path}", "build_assets/arch_linux/"], check=True)
                subprocess.run(["cp", "-r", "assets", "build_assets/arch_linux/"], check=True)
                subprocess.run(["cp", ".env", "build_assets/arch_linux/"], check=True)
                subprocess.run(["cp", "README.md", "build_assets/arch_linux/"], check=True)
                subprocess.run(["cp", "LICENSE", "build_assets/arch_linux/"], check=True)
                subprocess.run(["makepkg"], check=True)
                print("Package built successfully")
        else:
            print("Aborted")
            exit(0)

    def __run_pyinstaller(self):
        """
        Call pyinstaller to build the package
        """
        subprocess.run(["pyinstaller", "--onefile", "instance.py"], check=False)

    def __get_platform(self):
        """
        Get the platform string of the person running our script
        """
        return platform.system()

    def __check_file_exists(self, file_path: str) -> bool:
        """
        Returns true if a file exists, false otherwise
        """
        file_path = Path(file_path)
        if file_path.exists():
            return True
        return False

    def __get_linux_distribution(self):
        """
        Get the linux distribution name
        """
        try:
            with open("/etc/os-release") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("PRETTY_NAME"):
                        return line.split("=")[1].strip().strip('"')
        except FileNotFoundError:
            return "Unknown"

if __name__ == "__main__":
    PackageBuilder()
