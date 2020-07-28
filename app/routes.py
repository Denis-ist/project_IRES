# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, redirect, url_for, jsonify
from app.models import User, Post, Category
from app.forms import RegistrationForm, LoginForm, PostForm
from datetime import datetime, timedelta
from app import login
from flask_login import login_user, logout_user, current_user, login_required
from bs4 import BeautifulSoup


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts/<int:id_post>')
def view_post(id_post):
    post = Post.query.get(id_post)
    return render_template('view_post.html', post=post)


@app.route('/category/<string:alias>')
def view_category(alias):
    category = Category.query.filter_by(alias=alias).one()
    posts = Post.query.filter(Post.category == category).all()
    return render_template('posts.html', posts=posts, category=category)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == current_user.email).one()
        preview_text, word_count, is_sliced = '', 0, False
        text = form.text.data
        words = BeautifulSoup(text, 'html.parser').text.split()
        for word in words:
            preview_text += word + ' '
            word_count += 1
            if word_count == app.config['INTRO_WORDS_COUNT']:
                break
        if word_count < len(words):
            intro_text = preview_text.rstrip() + '...'
        else:
            intro_text = preview_text.rstrip()
        new_post = Post(
            heading=form.heading.data,
            text=text,
            intro_text=intro_text,
            date_created=datetime.now() - timedelta(hours=3),
            author_id=user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        register_data = {
            'name': form.name.data,
            'email': form.email.data,
            'age': form.age.data,
            'sex': form.sex.data,
            'password': form.password.data,
            'about_me': form.about_me.data,
        }
        if User.query.filter(User.email == register_data['email']).one_or_none() is not None:
            return render_template('registration.html', form=form, error="Такой пользователь уже существует!")
        new_user = User(
            email=register_data['email'],
            name=register_data['name'],
            age=register_data['age'],
            sex=register_data['sex'],
            about_me=register_data['about_me'],
        )
        new_user.set_password(register_data['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        login_data = {
            'email': form.email.data,
            'password': form.password.data,
            'remember_me': form.remember_me.data
        }
        user_db = User.query.filter(User.email == login_data['email']).one_or_none()
        if user_db is not None and user_db.check_password(login_data['password']):
            login_user(user_db)
            app.logger.info(f'Пользователь [{user_db.name}] успешно вошел на сайт')
            return redirect(url_for('index'))
        error = "Неправильный логин или пароль!"
        app.logger.error(error)
    return render_template('login.html', title='Войти на сайт', form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


