from django.db import models
from django.contrib.sessions.models import Session

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=100,verbose_name='密码')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    def is_authenticated(self):
        return True

    class Meta:
        db_table = "user"
        verbose_name = "用户表"

class Books(models.Model):
    name = models.CharField(max_length=100,unique=True,verbose_name='书名')
    desc = models.CharField(max_length=255,verbose_name='简介')
    author = models.CharField(max_length=100,verbose_name='作者')
    status = models.BooleanField(default=False,verbose_name='状态:True 借出 False 未借出')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    lending_time = models.DateTimeField(default=None,null=True,verbose_name='借出时间')
    return_time = models.DateTimeField(default=None,null=True,verbose_name='归还时间')
    lending_user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,verbose_name='借出人')

    class Meta:
        db_table = "books"
        verbose_name = "图书表"


class UserSession(models.Model):
    """用户和session映射表"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="session")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        db_table = "user_session"
        verbose_name = "用户session表"

