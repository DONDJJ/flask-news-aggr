from app import app
from app import routes,models
from app import news_request_forDB
from flask import Flask
from multiprocessing import Process

if __name__ == '__main__':
    func_list = [news_request_forDB.database_update, Flask.run]
    proc_list = []
    for i in func_list:
        if i is Flask.run:
            p = Process(target=app.run())
        else:
            p = Process(target=i)
        p.start()
        proc_list.append(p)

    for i in proc_list:
        i.join()

