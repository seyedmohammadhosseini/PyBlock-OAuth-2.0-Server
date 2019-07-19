import os


# default class of OAuth 2.0 Server
# :param register: access to PyBlock configuration and class
# :param libraries: access to all PyBlock libraries
# :param settings: access to setup.ini parameters
class controller:
    iota = None

    def __init__(self, register, libraries, settings):
        print("Start OAuth 2.0 Server")
