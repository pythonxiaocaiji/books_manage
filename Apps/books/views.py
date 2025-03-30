import datetime

from django.utils.timezone import now
from django_filters import rest_framework
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

#
from Apps.books.models import Books
from Apps.books.serializers import BooksSerializer
from utils.all_enum import ResponseStatus
from utils.paginations import CommonPagination
from utils.permissions import IsAuthenticated
from utils.redis_cli import conn_redis

class BooksView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['name', 'desc', 'author', ]
    filterset_fields = ("status",)
    pagination_class = CommonPagination

    # def get_serializer(self, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs['context'] = self.get_serializer_context()
    #     print(kwargs,'kwargs')
    #     if self.action == "list":
    #         kwargs["fields"] = ('id', 'name', 'status','desc','author',)
    #     # elif self.action == "retrieve":
    #     #     kwargs["fields"] = "__all__"
    #     return serializer_class(*args, **kwargs)


class BatchView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        types = request.data.get("types")
        ids = request.data.get("ids")
        if not ids:
            return Response({"status": ResponseStatus.ERROR.value, "msg": "请选择要操作的数据"})
        if types not in [1, 2, 3]:
            return Response({"status": ResponseStatus.ERROR.value, "msg": "请选择正确的操作类型"})
        books = Books.objects.filter(id__in=ids)
        msg = ""
        if types == 1:  # 删除
            books.delete()
            msg = "删除成功"
        elif types == 2:  # 借出
            books.filter(status=False).update(status=True, lending_time=now(), lending_user=request.user, return_time=datetime.datetime.now() + datetime.timedelta(days=30))
            msg = "借出成功"
        elif types == 3:  # 归还
            books.filter(status=True).update(status=False, lending_time=None, lending_user=None,return_time=None)
            msg = "归还成功"
        return Response({"status": 1, "msg": msg})


class BooksRemindView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user = request.user
        remind_list = conn_redis(11).get(str(user.id))
        if remind_list:
            conn_redis(11).delete(str(user.id))
            remind_list = eval(remind_list)
        else:
            remind_list = dict()
        return Response(remind_list)
