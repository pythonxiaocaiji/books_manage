# 项目部署文档

## 一、前提条件

> Centos 7服务器一台，可连接互联网

### 1. 软件要求

```
python 3.9.16
mysql 5.7.24
redis 5.0.3
```

### 2. 拉取项目相关

```shell script
# 拉取项目
cd /opt
git clone xxx.git # 上传包情况下对应解压相应文件
cd books_manage # 进入根目录

# 创建虚拟环境并拉取依赖
pip3 install virtualenv -i https://mirrors.aliyun.com/pypi/simple/
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirments.txt -i https://mirrors.aliyun.com/pypi/simple/

# 创建配置local_settings.py
cd books_manage
vim local_settings.py
# 内容开始 ->
import redis
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'books_manage',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456',  # 数据库密码
        'HOST': '127.0.0.1',  # 数据库地址
        'PORT': '3306',  # 数据库端口
        'CONN_MAX_AGE': 21600  # 数据库连接超时时间(秒) 建议比数据库默认的超时时间短 查看数据库默认超时时间(show variables like '%max_connections%';)
    }
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/12".format(REDIS_HOST, REDIS_PORT),
        "KEY_PREFIX": 'cache_',  # 前缀
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 128}
            # "PASSWORD": "密码",
        }
    }
}

pool1 = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=10)
REDIS1 = redis.Redis(connection_pool=pool1)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
# redis 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/12".format(REDIS_HOST, REDIS_PORT),
        "KEY_PREFIX": 'cache_',  # 前缀
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 128}
            # "PASSWORD": "密码",
        }
    }
}

# Celery配置
BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/13'

# 迁移表结构
python manage.py migrate

生成基础数据项目根目录下执行 python manage.py init_data
```  

### 3. supervisor 相关进程管理配置

```shell script
cd /opt
mkdir logs

cd /etc/supervisord.d/

# HTTP主服务配置
vim books_manage.ini 
[program:books_manage]
user=root
command=/opt/books_manage/venv/bin/uwsgi --ini books_manage_uwsgi.ini
autorstart=true
directory=/opt/books_manage/
autorestart=true
daemon=true
startsecs=5
stopwaitsecs=1
startretries=100
redirect_stderr=true
stopasgroup=true
killasgroup=true
stdout_logfile=/opt/logs/soc_log.txt
stderr_logfile=/opt/logs/soc_err.txt

vim books_manage_celery.ini 
[program:books_manage_celery]
user=root
command=/opt/books_manage/venv/bin/celery --app=books_manage worker -l info -c 1
autorstart=true
directory=/opt/books_manage/
autorestart=true
daemon=true
startsecs=1
stopwaitsecs=1
startretries=5
redirect_stderr=true
stopasgroup=true
killasgroup=true
stdout_logfile=/opt/logs/celery_soc_log.txt
stderr_logfile=/opt/logs/celery_soc_err.txt

vim books_manage_celery_beat.ini 
[program:books_manage_celery_beat]
user=root
command= /opt/books_manage/venv/bin/celery --app=books_manage beat -l info
autorstart=true
directory=/opt/books_manage/
autorestart=true
daemon=true
startsecs=1
stopwaitsecs=1
startretries=5
redirect_stderr=true
stopasgroup=true
killasgroup=true
stdout_logfile=/opt/logs/celery_beat_soc_log.txt
stderr_logfile=/opt/logs/celery_beat_soc_err.txt

supervisorctl reload
```

### 4. Nginx 相关配置

```shell script
cd /etc/nginx/conf.d
vim books_manage.conf

upstream books_manage {
    server 127.0.0.1:8000;
}
server {
    listen 80;
    server_name 113.201.14.253;  # 替换为你部署服务器的ip
    client_max_body_size 2000m;

    location /static{
        alias /opt/books_manage/static;
    }
    location /media{
        alias /opt/books_manage/media;
    }
    location /ws {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_send_timeout 30;
        proxy_connect_timeout 30;
        proxy_read_timeout 60;
        proxy_pass http://127.0.0.1:8006/ws;
        add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
    }
    location /{
        include uwsgi_params;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_x_real_host;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8000;
        uwsgi_connect_timeout 3600;
        proxy_redirect off;
        proxy_http_version 1.1;
    }
}
supervisorctl reload
```

### 5. uwsgi配置

```shell script
cd /opt/books_manage/
vim books_manage_uwsgi.ini

[uwsgi]
# 指定和nginx通信的端口
socket = 127.0.0.1:8000
# 项目路径
chdir = /opt/books_manage
# wsgi.py路径
wsgi-file = books_manage/wsgi.py
#启用主进程
master = true
# 进程数
processes = 8
# 线程数
thread = 2
#启用线程
enable-threads = True
#缓存大小
buffer-size = 21573
# 自动移除unix Socket和pid文件当服务停止的时候
vacuum = true
# gevent数
gevent=100
uid = root
gid = root
```