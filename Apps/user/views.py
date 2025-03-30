from rest_framework import generics, filters, serializers
from rest_framework.response import Response

from Apps.books.models import UserSession
from Apps.user.serializers import UserLolginSerializer
from utils.all_enum import ResponseStatus
from utils.redis_cli import conn_redis


class BooksView(generics.GenericAPIView):
    """后台登录"""
    serializer_class = UserLolginSerializer

    def post(self, request):
        # 如果已经登录了，先退出
        if request.user.is_authenticated:
            request.session.flush()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = dict()
        ret = {'status': ResponseStatus.SUCCESS.value, 'message': '登录成功', 'data': data}
        # 先删除旧的session数据
        user_sessions = UserSession.objects.filter(user=user)
        for user_session in user_sessions:
            key = "cache_:1:django.contrib.sessions.cached_db" + user_session.session.session_key
            conn_redis(12).delete(key)
            user_session.session.delete()
        # 生成新的session数据
        request.session.save()
        UserSession.objects.create(user=user, session_id=request.session.session_key)
        return Response(ret)


class UserLogoutView(generics.GenericAPIView):
    """
    用户退出
    """

    def get(self, request):
        request.session.flush()
        ret = {'status': ResponseStatus.SUCCESS.value, 'message': '退出成功', 'data': {}}
        return Response(ret)

