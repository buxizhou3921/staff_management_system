from django.shortcuts import render, redirect
from staff_manage import models
from staff_manage.utils.pagination import Pagination
from staff_manage.utils.forms import PrettyAddModelForm, PrettyEditModelForm


# 靓号管理
def pretty_list(request):
    """靓号列表"""

    # 条件搜索
    data_dict = {}
    search_data = request.GET.get('q', '')  # 默认空字符串
    if search_data:
        data_dict["mobile__contains"] = search_data
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 分页查询
    page_object = Pagination(request, queryset)

    context = {
        'search_data': search_data,  # 搜索条件回显
        'queryset': page_object.page_queryset,  # 分页后的数据
        'page_string': page_object.html()  # 分页组件html
    }
    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """添加靓号"""
    title = "新建靓号"

    if request.method == "GET":
        form = PrettyAddModelForm()
        return render(request, 'change.html', {"form": form, "title": title})

    form = PrettyAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    # 校验失败(显示错误信息)
    return render(request, 'change.html', {"form": form, "title": title})


def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")


def pretty_edit(request, nid):
    """修改靓号"""
    title = "编辑靓号"

    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # form.instance.字段名 = 值
        form.save()
        return redirect("/pretty/list/")

    # 校验失败(显示错误信息)
    return render(request, 'change.html', {"form": form, "title": title})
