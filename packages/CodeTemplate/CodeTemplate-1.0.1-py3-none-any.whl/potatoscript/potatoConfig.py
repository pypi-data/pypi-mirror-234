import configparser

class Config:
    def __init__(self, config_file):
        self.potato = configparser.ConfigParser()
        self.potato.read(config_file, encoding='utf-8')

    def get(self,section,value):
        potato = self.potato.get(section,value)
        return potato