from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.排除登录页面
        if request.path_info in ["/login/", "/image/code/"]:
            return

        info_dict = request.session.get("info")
        # 1.已登录，继续前讲
        if info_dict:
            return
        # 2.未登录，重回登录页面
        return redirect('/login/')
