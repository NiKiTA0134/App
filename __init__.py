from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "SoMeThInG"
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from . import routes