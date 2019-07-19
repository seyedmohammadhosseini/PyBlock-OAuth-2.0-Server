class config_library:

    def __init__(self, default):
        self.path = default.path + "/system/library/"
        self.ignore = ['__pycache__', '__init__.py']

    def get(self):
        return self