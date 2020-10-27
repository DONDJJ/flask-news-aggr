import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # откл ф-ю,которая сигнализирует приложению,когда в базе данных вносится изменение

    MAIL_SERVER='smtp.yandex.ru'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='DONDJJ11@yandex.ru'
    MAIL_PASSWORD='Oleglolcsgo2001'
    ADMINS = 'DONDJJ11@yandex.ru'
