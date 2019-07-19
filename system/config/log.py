class config_log:

    def __init__(self, default):
        self.runtime_error_path = default.path + "/system/storage/log/runtime_error.txt"


    def get(self):
        return self