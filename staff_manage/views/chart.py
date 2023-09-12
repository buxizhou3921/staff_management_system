from django.http import JsonResponse
from django.shortcuts import render


def chart_list(request):
    """数据统计页面"""

    return render(request, 'chart_list.html')


def chart_bar(request):
    """构造柱状图的数据"""
    legend = ['员工1', '员工2']
    series_list = [
        {
            "name": '员工1',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": '员工2',
            "type": 'bar',
            "data": [34, 12, 78, 12, 23, 56]
        }
    ]
    x_axis = ['1月', '2月', '3月', '4月', '5月', '6月']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """构造柱状图的数据"""
    series_list = [
        {"value": 1048, "name": 'IT部门'},
        {"value": 735, "name": '运营部门'},
        {"value": 580, "name": '新媒体部门'}
    ]

    result = {
        "status": True,
        "data": {
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


def chart_line(request):
    """构造折线图的数据"""

    legend = ['Email', 'Union Ads']
    series_list = [
        {
            "name": 'Email',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
        },
        {
            "name": 'Union Ads',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        }
    ]
    x_axis = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)
