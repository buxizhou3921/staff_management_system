import json
import random
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from staff_manage import models
from staff_manage.utils.pagination import Pagination
from staff_manage.utils.forms import OrderModelForm


def order_list(request):
    """订单列表"""
    queryset = models.Order.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    form = OrderModelForm()

    context = {
        "queryset": page_object.page_queryset,  # 分页后的数据
        "page_string": page_object.html(),  # 分页组件html
        "form": form,  # 新建订单
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """添加订单 (Ajax request)"""

    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True})
        # return HttpResponse(json.dumps({"status": True}))

    return JsonResponse({"status": False, "errors": form.errors})


def order_delete(request):
    """删除订单"""
    uid = request.GET.get('uid')
    exists = models.Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "数据不存在,删除失败！"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


def order_detail(request):
    """根据ID获取订单详细"""
    """
    # 方式一
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "errors": "数据不存在"})

    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)
    """
    # 方式二
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).values('title', 'price', 'status').first()
    if not row_object:
        return JsonResponse({"status": False, "errors": "数据不存在"})

    return JsonResponse({"status": True, 'data': row_object})


@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "数据不存在"})

    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "errors": form.errors})
