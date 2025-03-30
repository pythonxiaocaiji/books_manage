"""
URL configuration for safetymanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve


urlpatterns = [
    # --------------------------Apps----------------------------
    # 图书管理
    path('api/books/', include(('Apps.books.urls', 'Apps.books'), namespace='图书管理')),
    # 基础功能
    path('api/user/', include(('Apps.user.urls', 'Apps.user'), namespace='基础功能')),
]

if settings.DEBUG:
    import debug_toolbar
    from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # 静态文件托管
        re_path(r'^media/(.*$)', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(.*$)', serve, {'document_root': settings.STATIC_ROOT}),
        # 接口文档
        path('schema.yaml', SpectacularAPIView.as_view(), name='schema'),
        path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
