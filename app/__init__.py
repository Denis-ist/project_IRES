# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_moment import Moment
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
ckeditor = CKEditor(app)
moment = Moment(app)

# print('Секретный ключ: ' + app.config['SECRET_KEY'])

# Настройка логирования
if not os.path.exists('logs'):
    os.mkdir('logs')
if app.config['LOG_TO_STDOUT']:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
else:
    file_handler = RotatingFileHandler('logs/service.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Flask started...')

# Регистрируем Blueprint из файла api.py
from app.api import api
app.register_blueprint(api, url_prefix='/api/v1')

# Создаем в бд модели
db.create_all()

from app import routes, admin
