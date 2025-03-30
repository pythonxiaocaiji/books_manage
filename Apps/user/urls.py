from django.urls import path

from . import views

list_and_create = {'get': 'list', 'post': 'create'}
list_dict = {'get': 'list'}
get_dict = {'get': 'retrieve'}
get_and_update = {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}

urlpatterns = [
    # ----------------------基础功能--------------------------------
    # 用户登录
    path('login/', views.BooksView.as_view(), name="用户登录"),
    # 用户退出
    path('logout/', views.UserLogoutView.as_view(), name='用户退出'),

]
