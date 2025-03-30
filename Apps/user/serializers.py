from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.conf import settings

from Apps.books.models import User


class UserLolginSerializer(serializers.Serializer):
    """
    后台登录
    """
    name = serializers.CharField(label=u'用户名')
    password = serializers.CharField(label='密码')


    def validate(self, data):
        user = User.objects.filter(name=data['name']).first()
        if user:
            if not check_password(data['password'], user.password):
                raise serializers.ValidationError({"error": "用户名或密码错误!"})
            request = self.context['request']
            request.session['id'] = user.id
        else:
            raise serializers.ValidationError({"error": "用户名或密码错误!"})
        data['user'] = user
        user.save()
        return data