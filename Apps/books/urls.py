from django.urls import path

from . import views

list_and_create = {'get': 'list', 'post': 'create'}
list_dict = {'get': 'list'}
get_dict = {'get': 'retrieve'}
get_and_update = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}

urlpatterns = [
    # 图书管理
    path('', views.BooksView.as_view(list_and_create), name="图书管理"),
    # 图书管理
    path('<int:pk>/', views.BooksView.as_view(get_and_update), name="图书管理"),
    # 批量操作
    path('batch/', views.BatchView.as_view(), name="批量操作"),
    # 图书归还消息提醒
    path('remind/', views.BooksRemindView.as_view(), name='图书归还消息提醒'),
]
