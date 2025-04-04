# Generated by Django 3.2.20 on 2025-03-30 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '用户表',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session', verbose_name='session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户session表',
                'db_table': 'user_session',
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='书名')),
                ('desc', models.CharField(max_length=255, verbose_name='简介')),
                ('author', models.CharField(max_length=100, verbose_name='作者')),
                ('status', models.BooleanField(default=False, verbose_name='状态:True 借出 False 未借出')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('lending_time', models.DateTimeField(default=None, verbose_name='借出时间')),
                ('lending_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.user', verbose_name='借出人')),
            ],
            options={
                'verbose_name': '图书表',
                'db_table': 'books',
            },
        ),
    ]
