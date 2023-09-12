from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from staff_manage import models
from staff_manage.utils.forms import LoginForm
from staff_manage.utils.code import check_code


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        # 验证码校验
        user_input_code = form.cleaned_data.pop('code')
        code = request.session.get('image_code', '')
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {"form": form})

        # 网站生成随机字符串;写入到用户浏览器的cookie中;写入到session中;
        request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.username}
        # 设置session可保存1天
        request.session.set_expiry(60 * 60 * 24)

        return redirect("/admin/list/")

    return render(request, 'login.html', {"form": form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect("/login/")


def image_code(request):
    """生成图片验证码"""
    img, code = check_code()

    # 写入session
    request.session['image_code'] = code
    # 设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
