from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import current_user # потенциальная ошибка!

followers_association = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),  # подписчик (пользователь)
    db.Column('followed_id', db.Integer, db.ForeignKey('press.press_id'))  # на кого подписываются (СМИ)
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Press(db.Model):
    # Child
    press_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    posts = db.relationship('Post', backref='author',
                            lazy='dynamic')  # мы сказали ей указывать на класс Post и загружать их несколько

    followers = db.relationship(
        'User',
        secondary=followers_association,
        backref='users',
        lazy='dynamic'
    )

class User(UserMixin, db.Model):  # Наследование
    # Parent
    id = db.Column(db.Integer, primary_key = True)  # primery_key - уникальное
    email = db.Column(db.String(64), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):  # сообщает Python, как печатать объекты этого класса, что будет полезно для отладки
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, press):
        return self.followed.filter(followers_association.c.followed_id == press.press_id).count() > 0

    def debug(self, press):
        return self.followed.filter(followers_association.c.followed_id == press)

    def follow(self, press):
        if not self.is_following(press):
            self.followed.append(press)

    def unfollow(self, press):
        if self.is_following(press):
            self.followed.remove(press)

    followed = db.relationship(
        "Press",
        secondary = followers_association,
        backref = 'presses',
        lazy='dynamic'
        )

    def followed_posts(self):
        return Post.query.join(
            followers_association, (followers_association.c.followed_id == Post.user_id))

class Post(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('press.press_id'))  # это поле и есть foreign key
    title = db.Column(db.String(140))
    href = db.Column(db.String(340))












# flask db init
# flask db migrate -m "users table"
# flask db upgrade