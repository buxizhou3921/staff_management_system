"""
URL configuration for staff_management_system project.

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
from django.urls import path, re_path
from django.views.static import serve
from staff_manage.views import depart, user, pretty, admin, account, order, chart, upload, city

urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 管理员
    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/reset/", admin.admin_reset),

    # 部门管理
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),
    path("depart/multi/", depart.depart_multi),

    # 用户管理
    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/model/form/add/", user.user_model_form_add),
    path("user/<int:nid>/delete/", user.user_delete),
    path("user/<int:nid>/edit/", user.user_edit),

    # 靓号管理
    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit),

    # 登录
    path("login/", account.login),
    path("logout/", account.logout),
    path("image/code/", account.image_code),

    # 订单管理
    path("order/list/", order.order_list),
    path("order/add/", order.order_add),
    path("order/delete/", order.order_delete),
    path("order/detail/", order.order_detail),
    path("order/edit/", order.order_edit),

    # 数据统计
    path("chart/list/", chart.chart_list),
    path("chart/line/", chart.chart_line),
    path("chart/bar/", chart.chart_bar),
    path("chart/pie/", chart.chart_pie),

    # 文件上传
    path("upload/form/", upload.upload_form),
    path("upload/modelform/", upload.upload_modelform),

    # 城市管理
    path("city/list/", city.city_list),

]
