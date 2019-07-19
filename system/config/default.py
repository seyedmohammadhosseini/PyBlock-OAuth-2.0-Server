import os
from system.config import log, module, library


class default_config:
    def __init__(self):
        self.config_ = {}
        self.log = None
        self.network = None
        self.module = None
        self.library = None
        self.path = os.getcwd()
        self.author = "Seyed Mohammad Hosseini"
        self.version = "1.5.9.1"
        self.startTime = "02.12.2019"

        self.get_other_configs()

        pass

    def get(self, key):
        if key in self.config_:
            return self.config_[key]
        else:
            return False

    def set(self, key, value):
        if key not in self.config_:
            self.config_[key] = value
        else:
            return False

    def update(self, key, value):
        if key in self.config_:
            self.config_[key] = value
        else:
            return False
        pass

    def get_other_configs(self):
        self.log = log.config_log(self).get()
        self.module = module.config_module(self).get()
        self.library = library.config_library(self).get()
