from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

import config

app = Flask(__name__)

app.config.update(config.ENV_VAR)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

logger = app.logger


################ ASSETS MANAGEMENT ################
# right now just minification and concatenation

assets = Environment(app)
assets.url = app.static_url_path

css_all = Bundle(
    'css/*.css',
    filters='cssmin',
    output='dist/css_all.css'
)

js_all = Bundle(
    'js/vendor/jquery-1.11.0.min.js',  # order matters
    'js/vendor/*.js', 'js/*.js',
    filters='jsmin',
    output='dist/js_all.js'
)

assets.register('js_all', js_all)
assets.register('css_all', css_all)

assets.add(js_all)
assets.add(css_all)

js_all.build()
css_all.build()


from views import *

if __name__ == '__main__':
    app.run()
