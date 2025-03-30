# utils/middleware.py
import json
import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('log')


class ApiLoggingMiddleware(MiddlewareMixin):
    """记录 API 请求参数和耗时"""

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.get_response = get_response

    def process_request(self, request):
        """请求开始时记录时间"""
        request.start_time = time.time()  # 记录请求开始时间
        request.api_data = None
        if request.body:
            request.api_data = json.loads(request.body.decode("utf-8"))
        return None

    def process_response(self, request, response):
        """请求结束时记录日志"""
        try:
            # 计算耗时（毫秒）
            duration = (time.time() - request.start_time) * 1000

            # 获取请求参数（兼容 GET/POST/JSON）
            request_data = {}
            if request.GET:
                request_data["GET"] = dict(request.GET)
            if request.POST:
                request_data["POST"] = dict(request.POST)
            if request.api_data and request.headers.get("Content-Type") == "application/json":
                try:
                    request_data["JSON"] = request.api_data
                except json.JSONDecodeError:
                    import traceback
                    traceback.print_exc()

            # 日志内容
            log_data = {
                "path": request.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": round(duration, 2),  # 保留2位小数
                "request_data": request_data,
                "client_ip": request.META.get("REMOTE_ADDR"),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
            }
            # 记录日志（INFO 级别）
            logger.info(
                f"API Request: {request.method} {request.path} \n "
                f"Status: {response.status_code} \n "
                f"Duration: {duration:.2f}ms\n"
                f"Data:{log_data}",  # 结构化日志（方便日志系统解析）
            )
        except Exception as e:
            logger.error(f"API Logging Error: {e}", exc_info=True)

        return response
