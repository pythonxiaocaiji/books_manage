# Generated by Django 3.2.20 on 2025-03-30 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_books_lending_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='return_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='归还时间'),
        ),
    ]
