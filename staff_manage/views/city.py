from django.shortcuts import render, redirect
from staff_manage import models


def city_list(request):
    """城市列表"""
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {"queryset": queryset})
