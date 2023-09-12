from django.shortcuts import render, redirect
from staff_manage import models
from staff_manage.utils.pagination import Pagination
from staff_manage.utils.forms import UserModelForm


# 用户管理
def user_list(request):
    """用户列表"""
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html()  # 分页组件html
    }
    return render(request, 'user_list.html', context)


def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)

    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")
    ac = request.POST.get("ac")
    ctime = request.POST.get("ctime")
    gd = request.POST.get("gd")
    dp = request.POST.get("dp")
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=ac, create_time=ctime,
                                   gender=gd, depart_id=dp)
    return redirect("/user/list/")


def user_model_form_add(request):
    """添加用户(ModelForm)"""
    title = "新建用户"

    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'change.html', {"form": form, "title": title})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    # 校验失败(显示错误信息)
    return render(request, 'change.html', {"form": form, "title": title})


def user_delete(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_edit(request, nid):
    """修改用户"""
    title = "编辑用户"

    row_object = models.UserInfo.objects.filter(id=nid).first()
    row_object.create_time = row_object.create_time.strftime('%Y-%m-%d')
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.instance.字段名 = 值
        form.save()
        return redirect("/user/list/")

    # 校验失败(显示错误信息)
    return render(request, 'change.html', {"form": form, "title": title})
