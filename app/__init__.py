from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.babel import Babel
from flask.ext.babel import lazy_gettext
from momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

app.jinja_env.globals['momentjs'] = momentjs

babel = Babel(app)

from app import viewsBase, viewsLogin, viewsProduct, viewsMaker, viewsCategory, viewsOrder, viewsDelivery, viewsSettings
