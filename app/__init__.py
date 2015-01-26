from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.babel import Babel
from momentjs import momentjs
from flask.ext.babel import gettext
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = gettext('Please log in to access this page.')

app.jinja_env.globals['momentjs'] = momentjs

babel = Babel(app)

from flask.ext.mail import Mail
mail = Mail(app)

from app import viewsBase, viewsLogin, viewsProduct, viewsMaker, viewsCategory, viewsOrder, viewsDelivery, \
    viewsSettings, viewsRequest, viewsSupply, viewsCustomer, viewsContact, viewsShop, imageHelper, scheduled

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled.sheduleLastura, 'cron', hour=3)
scheduler.start()