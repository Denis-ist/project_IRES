# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, IntegerField, SelectField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, DataRequired, EqualTo, Length, NumberRange
from flask_ckeditor import CKEditorField


class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя:', validators=[DataRequired()])
    email = EmailField('Ваш email:', validators=[DataRequired(), Email()])
    password = PasswordField('Ваш пароль:', validators=[DataRequired(),
                                                        EqualTo('repeat_password', message='Пароли не совпадают!'),
                                                        Length(min=6, message='Минимальная длина пароля: 6 символов')])
    repeat_password = PasswordField('Ваш пароль:')
    age = IntegerField('Ваш возраст', validators=[DataRequired(), NumberRange(min=1, max=99,
                                                                              message='Неправильный возраст!')])
    sex = SelectField('Выберите пол', choices=[('male', 'Мужской'), ('female', 'Женский')], validators=[DataRequired()])
    about_me = TextAreaField('О себе (не обязательно):')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message="Вы не ввели email!")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Вы не ввели пароль!"),
                                                   Length(min=6, message="Минимальная длина пароля %(min)d символов!")])
    remember_me = BooleanField('Запомнить меня', default='checked')
    submit = SubmitField('Войти')


class PostForm(FlaskForm):
    heading = StringField('Название статьи', validators=[DataRequired(message="Заголовок обязателен!"),
                                                         Length(min=3, message="Минимум три символа в заголовке")])
    text = CKEditorField('Текст публикации', validators=[DataRequired(message="Поле обязательно для ввода!"),
                                                         Length(min=10, message='Введите больше текста...')])
    submit = SubmitField('Сохранить')
