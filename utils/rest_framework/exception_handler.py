import logging
import traceback

from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as rest_handler

logger = logging.getLogger('log')


def exception_handler(exc, context):
    """全局异常处理器"""
    response = rest_handler(exc, context)
    if not response:
        if settings.DEBUG:
            return response
        traceback.print_exc()
        logger.error(str(traceback.format_exc()))
        data = {"error": "服务器异常"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    code = response.status_code
    if code <= 500 and code >= 599:
        if settings.DEBUG:
            return response
        traceback.print_exc()
        logger.error(str(traceback.format_exc()))
        data = {"error": "服务器异常"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, dict):
            data = exc.detail
            for key, value in data.items():
                if isinstance(value, list):
                    if isinstance(value[0], str):
                        data[key] = ','.join(value)
            response.data = data
        elif isinstance(exc.detail, list):
            data = exc.detail
            response.data = data
        else:
            data = {'error': exc.detail}
            response.data = data
    return response
