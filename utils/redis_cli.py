from redis import StrictRedis

from django.conf import settings


def conn_redis(database=10):
    """
    redis 连接
    """
    cli = StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=database,
                      socket_connect_timeout=2,
                      charset='utf-8')
    return cli
