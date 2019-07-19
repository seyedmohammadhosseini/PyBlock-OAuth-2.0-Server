from flask import Flask
from authlib.flask.client import OAuth
# use loginpass to make OAuth connection simpler
from loginpass import create_flask_blueprint, GitHub

# default class of OAuth 2.0 Server
# :param register: access to PyBlock configuration and class
# :param libraries: access to all PyBlock libraries
# :param settings: access to setup.ini parameters



class controller:
    iota = None

    def __init__(self, register, libraries, settings):
        print("Start OAuth 2.0 Server")
        app = Flask(__name__)
        oauth = OAuth(app)
        github_bp = create_flask_blueprint(GitHub, oauth, self.handle_authorize)
        app.register_blueprint(github_bp, url_prefix='/github')

    def handle_authorize(self, remote, token, user_info):
        print("Here")

