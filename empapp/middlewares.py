from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin


class MyMiddlewares(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        print("init1")

    # view处理请求前执行
    def process_request(self, request):
        if "userapp" not in request.path:
            status=request.session.get("login")
            if status:
                pass
            else:
                return redirect("userapp:login")
        print("request:", request)

    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        print("view:", request, view_func, view_args, view_kwargs)

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        print("response:", request, response)
        return response  # 必须返回response

    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        print("exception:", request, ex)