from rest_framework import pagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.response import Response
from collections import OrderedDict

class CommonPagination(pagination.PageNumberPagination):
    page_query_description = '页码'
    page_size_query_description = '每页数量'
    max_page_size = 1000  # 表示允许的最大请求页面大小
    page_size_query_param = 'size'  # 允许客户端基于每个请求设置页面大小的查询参数的名称
    page_size = 10  # 表示页面大小的数值
    nopage_query_param = 'nopage'


    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.get_full_path()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def paginate_queryset(self, queryset, request, view=None):
        if request.GET.get(self.nopage_query_param, None):
            return None
        return super(CommonPagination, self).paginate_queryset(
            queryset, request, view)
    def get_paginated_response(self, data, display=None):
            return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('display', display),
            ('results', data)
        ]))
