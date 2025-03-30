from __future__ import absolute_import

import os
from celery import Celery
from django.conf  import settings
import sys

# 设置Django默认的setting模块
if sys.platform == "win32":
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books_manage.settings')

app = Celery('books_manage', broker=settings.BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

# 不需要使用序列化
# namespace='CELERY'，表示所有与celery相关的配置，单个需要设置'CELERY_'的前缀
app.config_from_object('django.conf:settings', namespace='CELERY')

# 从所有已注册的Django应用程序配置中加载任务模块
app.autodiscover_tasks()
