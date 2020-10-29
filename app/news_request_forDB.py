from app import db
from app.news import *
from app.course import *
from app.weather import *
from time import sleep
from app.models import *

def database_update():
    func_list = [yandex_news_check, meduza_check, currency_chech, get_weather, ria_check, lenta_check,
                 sport_express_check_football,sport_express_check_hockey, sport_express_check_autosport]

    while True:
        for i in range(1, len(func_list)+1):
            data = func_list[i-1]()
            print(type(data[0]) is list or type(data[0]) is tuple)
            if type(data[0]) is list or type(data[0]) is tuple:
                for j in range(min((len(data[0])), (len(data[1])))):
                    p = Post(user_id = i, title =data[0][j].strip(), href = data[1][j].strip())
                    db.session.add(p)
                    db.session.commit()
            else:
                p = Post(user_id = i, title = data[0], href = data[1])
                db.session.add(p)
                db.session.commit()

            sleep(10)
            if i==len(func_list):
                Post.query.filter(Post.user_id==1).delete()
            else:
                Post.query.filter(Post.user_id==i+1).delete()
            db.session.commit()
