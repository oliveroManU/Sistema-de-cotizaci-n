from flask import Flask
from flask_login import LoginManager
import os

app = Flask(__name__, template_folder='../../templates', static_folder='../../static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-cambiar-esto')

os.makedirs(app.instance_path, exist_ok=True)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesión para acceder.'
login_manager.login_message_category = 'no'

from . import routes