from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os
from flask_mail import Mail

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password
from flask_security.models import fsqla_v2 as fsqla


app = Flask(__name__, template_folder = "../templates", static_folder="../static")
app.config.from_object(Config)
db=SQLAlchemy(app)

fsqla.FsModels.set_db_info(db)
migrate = Migrate(app, db)
mail = Mail(app)

from homeschool import models


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)


from homeschool import routes
from homeschool.utils import convert_links

app.jinja_env.filters["convert_links"] = convert_links

log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]' )

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Homeschool startup')
