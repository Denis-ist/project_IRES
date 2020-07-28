# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'abcdef1234567890!@#$%^000!!!'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'Lumen'
    ADMIN_EMAIL = 'istomin.mr2011@yandex.ru'
    INTRO_WORDS_COUNT = 20
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT') or False