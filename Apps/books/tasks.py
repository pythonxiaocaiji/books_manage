import datetime
import json

from celery.schedules import crontab
from datetime import timedelta
from Apps.books.models import Books
from books_manage.celery import app

from utils.redis_cli import conn_redis

app.conf.broker_transport_options = {'visibility_timeout': 86400}

app.conf.beat_schedule = {
    'return_reminder': {  # 图书到期归还提醒
        'task': 'return_reminder',
        'schedule': crontab(hour=8, minute=0),  # 每天8:00执行
        # 'schedule': timedelta(minutes=1), # 用于测试
        'args': ()
    },
}


@app.task(name='return_reminder')
def return_reminder():
    """
    图书到期归还提醒
    :return:
    """
    return_books = Books.objects.filter(status=True, return_time__lte=datetime.datetime.now() + datetime.timedelta(days=7))
    for book in return_books:
        data = {
            'title': '图书到期归还提醒',
            'books_name': book.name,
        }
        conn_redis(11).set(str(book.lending_user.id), json.dumps(data))
        if book.return_time <= datetime.datetime.now():
            book.status = False
            book.return_time = None
            book.lending_time = None
            book.lending_user = None
            book.save()

