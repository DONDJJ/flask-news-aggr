from app import app
from flask import render_template, flash, redirect, url_for
from flask import url_for
from app import news
from app import course
from app import weather
import requests, base64
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
import _thread as thread
import queue
import threading
from app.que import que
from multiprocessing import Process, Queue
from time import sleep
from app.news_request_forDB import SMI_dict
import random

@app.route('/')
@app.route('/home')
def home():
    req_list = [news.yandex_news_check, news.meduza_check, course.currency_chech,
                weather.get_weather]  # список функций, которые надо вызвать в отдельных процессах

    # thl = []
    # for func in req_list:
    #     thread_ = threading.Thread(target=func, args=[que, ])
    #     thl.append(thread_)
    #     thread_.start()
    #     thread_.join()

    # for thread_ in thl:

    # ps = []
    # for func in req_list:
    #     p = Process(target=func, args=(que,))
    #
    # for p in ps:
    #     p.start()
    #     p.join()

    # yandex_news=news.yandex_news_check()
    # meduza_news=news.meduza_check()
    # currency_info = course.currency_chech()
    # weather_data = weather.get_weather("Kazan")

    # yandex_news = que.get()
    # meduza_news = que.get()
    # currency_info = que.get()
    # weather_data = que.get()

    return render_template('index.html',
                           title='Home',
                           yandex_news=zip([post.title for post in Post.query.filter(Post.user_id == 1)],
                                           [post.href for post in Post.query.filter(Post.user_id == 1)]),
                           meduza_news=zip([post.title for post in Post.query.filter(Post.user_id == 2)],
                                           [post.href for post in Post.query.filter(Post.user_id == 2)]),
                           dollar= Post.query.filter(Post.user_id == 3).first().title,
                           euro=Post.query.filter(Post.user_id == 3).first().href,
                           temp=Post.query.filter(Post.user_id == 4).first().title,
                           weather_desc=Post.query.filter(Post.user_id == 4).first().href)
    # weather_icon=base64.encodebytes(
    #     requests.get('http://openweathermap.org/img/wn/{}.png'.format(weather_data[2]),
    #                  stream=True).raw.read()))


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
                           title = "Мой новости",
                           all_news = my,
                           presses=presses)


@app.route('/sources')
def sources():
    presses = Press.query.all()
    return render_template('sources.html',
                           presses=presses)


@app.route('/subscribtions')
def my_subs():
    # user=User.query.filter_by(email = current_user.email)
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



# !--            <div id="data_all_posts">-->
# <!--                <a class="p-2 btn-link" href="/user/{{post.author.username[0:5]}}">{{post.author.username[0:5]}}</a>-->
# <!--                {{post.timestamp}}-->
# <!--            </div>-->
