from rest_framework import permissions

class IsAuthenticated(permissions.IsAuthenticated):
    message = '未登录'

