from app import app
from flask import render_template, flash, redirect, url_for
from flask import url_for
from app import news
from app import course
from app import weather
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *



@app.route('/')
@app.route('/home')
def home():
    req_list = [news.yandex_news_check, news.meduza_check, course.currency_chech,
                weather.get_weather]  # список функций, которые надо вызвать в отдельных процессах

    return render_template('index.html',
                           title='Home',
                           yandex_news=zip([post.title for post in Post.query.filter(Post.user_id == 1)],
                                           [post.href for post in Post.query.filter(Post.user_id == 1)]),
                           meduza_news=zip([post.title for post in Post.query.filter(Post.user_id == 2)],
                                           [post.href for post in Post.query.filter(Post.user_id == 2)]),
                           dollar=Post.query.filter(Post.user_id == 3).first().title,
                           euro=Post.query.filter(Post.user_id == 3).first().href,
                           temp=Post.query.filter(Post.user_id == 4).first().title,
                           weather_desc=Post.query.filter(Post.user_id == 4).first().href)


@app.route('/login', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('sign_in'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    else:
        return render_template('login.html',
                               title="Login",
                               form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route('/news')
def my_news():
    my = list(current_user.followed_posts().all())
    presses = Press.query.all()
    return render_template('my_news.html',
                           title="Мой новости",
                           all_news=my,
                           presses=presses)


@app.route('/sources')
def sources():
    presses = Press.query.all()
    return render_template('sources.html',
                           presses=presses)


@app.route('/subscribtions')
def my_subs():
    presses = Press.query.all()
    return render_template('subscribtions.html',
                           presses=presses,
                           current_user=current_user)


@app.route('/follow/<user_id>')
@login_required
def follow(user_id):
    press = Press.query.filter_by(press_id=user_id).first()
    current_user.follow(press)
    db.session.commit()
    return redirect(url_for('my_subs', username=user_id))


@app.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    press = Press.query.filter_by(press_id=user_id).first()
    current_user.unfollow(press)
    db.session.commit()
    return redirect(url_for('my_subs', username=user_id))


@app.route('/debug')
@login_required
def degub():
    return current_user.debug(1)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
