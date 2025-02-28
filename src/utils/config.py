import configparser


class Config:
    def __init__(self, file_path: str) -> None:
        self.config = configparser.ConfigParser()
        self.file_path = file_path

        self.config.read(file_path)

    def get(self, section: str, option: str) -> str:
        return self.config.get(section, option)

    def getint(self, section: str, option: str) -> int:
        return self.config.getint(section, option)